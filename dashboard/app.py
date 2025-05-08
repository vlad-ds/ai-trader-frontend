import streamlit as st
import json, datetime, re
import pandas as pd
import numpy as np
from pathlib import Path

# Get the directory where the script is located
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"  # Use absolute path to data directory

@st.cache_data(ttl=900)   # refresh every 15 min
def load_snapshot_data(agent):
    files = sorted((DATA_DIR/"snapshots").glob(f"{agent}_*.json"))
    if not files:
        return None, None, None
    
    latest = files[-1]
    last_updated = datetime.datetime.strptime(latest.stem.split('_', 1)[1], '%Y%m%d_%H%M%S')
    
    with open(latest) as f:
        data = json.load(f)
        account = data.get('account', {})
        positions = data.get('positions', [])
        # Add market_value as numeric for sorting
        for pos in positions:
            pos['total_value'] = float(pos.get('market_value', 0))
        
        return account, positions, last_updated

@st.cache_data(ttl=86400) # refresh daily
def load_diary(agent):
    today = datetime.date.today().strftime("%Y-%m-%d")
    fp = DATA_DIR/"diary"/f"{agent}_{today}.md"
    return Path(fp).read_text() if fp.exists() else "*No entry yet*"

def format_currency(val):
    if isinstance(val, (int, float)):
        return f"${val:,.2f}"
    return val

def highlight_profit_loss(val):
    if isinstance(val, (int, float)):
        color = 'green' if val > 0 else 'red' if val < 0 else 'black'
        return f'<span style="color:{color}">{format_currency(val)}</span>'
    return val

def parse_diary_content(diary_content):
    """Parse diary content extracting date and formatting the content"""
    # Extract date from first line
    date_match = re.search(r'Trading Diary: (.*)', diary_content)
    date = date_match.group(1) if date_match else "Today"
    
    # Clean up the content - remove the first line (title)
    content = re.sub(r'^# Trading Diary:.*?\n', '', diary_content, flags=re.MULTILINE)
    
    # Convert markdown to properly formatted HTML
    # Format headers
    content = re.sub(r'^## (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    
    # Format bullet points
    content = re.sub(r'^\* (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\g<0></ul>', content, flags=re.DOTALL)
    
    return date, content

# Set page config first before any other Streamlit commands
st.set_page_config(
    page_title="MCP Trader League",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Page title styling */
    .main .block-container h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 3px solid #4e8df5;
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    /* Sidebar styling */
    .st-emotion-cache-16txtl3 h1 {
        font-size: 1.8rem !important;
        margin-bottom: 1.5rem !important;
        color: #4e8df5;
    }
    
    /* Diary title styling */
    .diary-header h2 {
        margin-bottom: 1rem;
    }
    
    .diary-details summary {
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        padding: 0.5rem 0;
        color: #1E88E5;
        transition: color 0.3s;
    }
    
    .diary-details summary:hover {
        color: #0D47A1;
    }
    
    .diary-content {
        margin-top: 1rem;
        padding-left: 1rem;
        border-left: 3px solid #E0E0E0;
    }
    
    /* Footer styling */
    .footer {
        margin-top: 2rem;
        padding: 1rem 0;
        border-top: 1px solid #E0E0E0;
        text-align: center;
        color: #757575;
        font-size: 0.9rem;
    }
    
    .footer span {
        margin: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- UI ---
# Sidebar navigation
with st.sidebar:
    st.title("MCP Trader League")
    st.markdown("---")
    page = st.radio("### Navigation", ["Claude_1", "About"], label_visibility="collapsed")

# Use fixed agent name - no selector needed
agent = "default"

# Load data
account, positions, last_updated = load_snapshot_data(agent)

# Define function to show About page
def show_about_page():
    st.title("ℹ️ MCP Trader League")
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""

The MCP League Dashboard is a lightweight web front-end that lets you watch autonomous trading agents compete inside a paper-money sandbox.  

Each agent starts with $100,000 in simulated cash and tries to grow that balance through daily research and limit-order execution on Alpaca’s API.  The system never touches real funds; everything shown here is a game with live market data.

## What you are seeing

**Account snapshot**  
Cash & positions are updated every 15 minutes during market hours, so the displayed values may be up to 15 minutes old.

**Diary**  
Once per U.S. trading day the agent completes a six-stage routine that ends with a Markdown diary entry. The diary explains what information the agent gathered, which trades it placed, the reasoning behind those trades, and any forward-looking hypotheses.

| Data element | Refresh cadence |
|--------------|-----------------|
| Cash & positions | every 15 min on trading days |
| Diary | once, after the close of each trading day |

## How the agent trades

The agent is following this prompt: https://github.com/vlad-ds/ai-trader-frontend/blob/main/prompts/main.md

The agent is an instance of Claude Sonnet 3.7 Thinking running in the Claude.ai app. I built a custom Model Context Protocol (MCP) to connect it to the Alpaca API.

## Ethics and safety

Because the account is entirely virtual, no real capital is at risk. This is just a fun experiment. Please don't take it too seriously and don't follow the agent's trades!

## Contact

I'm Vlad, and I love building AI products. You can find me at [https://www.linkedin.com/in/vlad-ds/](https://www.linkedin.com/in/vlad-ds/). Always happy to get DMs and hear feedback.
    """)
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <span>© 2025 MCP Trader League</span>
        <span>|</span>
        <span>Created by Vlad Gheorghe</span>
        <span>|</span>
        <span>Data from Alpaca Trading API</span>
    </div>
    """, unsafe_allow_html=True)

# Conditional rendering based on selected page
if page == "Claude_1":
    if account and positions is not None:
        # Header with last updated time
        st.title("📊 Claude_1")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Define original portfolio value
    ORIGINAL_PORTFOLIO_VALUE = 100000.00
    current_portfolio_value = float(account.get('portfolio_value', 0))
    
    # Calculate gain/loss
    gain_loss_amount = current_portfolio_value - ORIGINAL_PORTFOLIO_VALUE
    gain_loss_percentage = (gain_loss_amount / ORIGINAL_PORTFOLIO_VALUE) * 100
    
    # Performance metrics
    # Use a container for better visual organization
    with st.container():
        # Add styles for performance metrics
        st.markdown("""
        <style>
        .section-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #d3d3d3;
            margin-bottom: 1.2rem;
            border-bottom: 2px solid #4e8df5;
            display: inline-block;
            padding-bottom: 0.3rem;
            margin-top: 1rem;
        }
        .performance-title {
            border-bottom-color: #50c878;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #9e9e9e;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 0.2rem;
        }
        .metrics-row {
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Portfolio Overview title
        st.markdown("""<div class='section-title'>Portfolio Overview</div>""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown(f"""
            <div class='metric-label'>Portfolio Value</div>
            <div class='metric-value'>{format_currency(current_portfolio_value)}</div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-label'>Cash Balance</div>
            <div class='metric-value'>{format_currency(account.get('cash', 0))}</div>
            """, unsafe_allow_html=True)
        with col3:
            buying_power = account.get('buying_power', 0)
            st.markdown(f"""
            <div class='metric-label'>Buying Power</div>
            <div class='metric-value'>{format_currency(buying_power)}</div>
            """, unsafe_allow_html=True)
        
        st.markdown("""<div class='metrics-row'></div>""", unsafe_allow_html=True)
        
        # Second row - Performance metrics
        st.markdown("""<div class='section-title performance-title'>Performance Metrics</div>""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown(f"""
            <div class='metric-label'>Original Investment</div>
            <div class='metric-value'>{format_currency(ORIGINAL_PORTFOLIO_VALUE)}</div>
            """, unsafe_allow_html=True)
        with col2:
            # Color coding for gain/loss
            gain_loss_color = "#50c878" if gain_loss_amount >= 0 else "#ff6b6b"
            arrow = "↑" if gain_loss_amount > 0 else "↓" if gain_loss_amount < 0 else ""
            st.markdown(f"""
            <div class='metric-label'>Total Gain/Loss</div>
            <div class='metric-value' style='color: {gain_loss_color};'>{format_currency(gain_loss_amount)}</div>
            <div style='color: {gain_loss_color}; font-size: 0.9rem;'>{arrow} {gain_loss_percentage:.2f}%</div>
            """, unsafe_allow_html=True)
        with col3:
            # Same color coding for consistency
            st.markdown(f"""
            <div class='metric-label'>Since Start</div>
            <div class='metric-value' style='color: {gain_loss_color};'>{gain_loss_percentage:.2f}%</div>
            """, unsafe_allow_html=True)
            
        st.markdown("""<div class='metrics-row'></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
        
    # Positions table
    st.header("💼 Positions")
    
    if positions:
        # Convert to DataFrame and sort by total value
        pos_df = pd.DataFrame(positions)
        pos_df = pos_df.sort_values('total_value', ascending=False)
        
        # Format columns for display - select relevant columns
        display_df = pos_df.copy()
        
        # Select columns and rename them for display
        cols = {
            'symbol': 'Symbol',
            'qty': 'Quantity',
            'avg_entry_price': 'Avg Cost',
            'current_price': 'Current',
            'market_value': 'Value',
            'unrealized_pl': 'Unrealized P/L',
            'unrealized_plpc': 'P/L %'
        }
        
        # Filter columns that exist in dataframe
        existing_cols = {k: v for k, v in cols.items() if k in display_df.columns}
        
        # Create a display-ready dataframe with formatted values
        display_df = pos_df.copy()
        
        # Format the values in the dataframe
        for col in display_df.columns:
            if col == 'qty':
                display_df[col] = display_df[col].apply(lambda x: f"{float(x):.0f}")
            elif col == 'unrealized_plpc':
                display_df[col] = display_df[col].apply(lambda x: f"{float(x)*100:.2f}%")
            elif col in ['avg_entry_price', 'current_price', 'market_value', 'unrealized_pl']:
                display_df[col] = display_df[col].apply(format_currency)
        
        # Rename columns to display names
        display_df = display_df.rename(columns=existing_cols)
        
        # Select only the columns we want to display
        display_df = display_df[list(existing_cols.values())]
        
        # Define a function for styling the dataframe
        def highlight_pl(val):
            if 'Unrealized P/L' in val.name:
                try:
                    # Remove $ and , to get numerical value
                    cleaned_val = val.str.replace('$', '').str.replace(',', '')
                    return ['color: green' if float(v) > 0 else 'color: red' if float(v) < 0 else '' for v in cleaned_val]
                except:
                    return [''] * len(val)
            elif 'P/L %' in val.name:
                try:
                    # Remove % to get numerical value
                    cleaned_val = val.str.replace('%', '')
                    return ['color: green' if float(v) > 0 else 'color: red' if float(v) < 0 else '' for v in cleaned_val]
                except:
                    return [''] * len(val)
            return [''] * len(val)
        
        # Apply styling to dataframe
        styled_df = display_df.style.apply(highlight_pl)
        
        # Display the dataframe using Streamlit's native component
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("No positions found.")
    
    st.markdown("---")

    # Diary section
    st.markdown("<div class='diary-header'><h2>📝 Trading Diary</h2></div>", unsafe_allow_html=True)
    diary_content = load_diary(agent)
    
    if diary_content and diary_content != "*No entry yet*":
        date, formatted_content = parse_diary_content(diary_content)
        
        # Display as a single collapsible for the entire day with enhanced visibility
        st.markdown(f"""
        <div class="diary-container">
            <details class="diary-details" open>
                <summary>Trading Diary: {date}</summary>
                <div class="diary-content">
                    {formatted_content}
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No diary entry for today.")
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <span>© 2025 MCP Trader League</span>
        <span>|</span>
        <span>Created by Vlad Gheorghe</span>
        <span>|</span>
        <span>Data from Alpaca Trading API</span>
    </div>
    """, unsafe_allow_html=True)
elif page == "About":
    show_about_page()