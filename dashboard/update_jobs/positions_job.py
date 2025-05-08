import os
import json
import datetime
import uuid
from pathlib import Path
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus

# Load environment variables
load_dotenv()

# Configure Alpaca client
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_PAPER = os.getenv('ALPACA_PAPER', 'true').lower() == 'true'

# Set up data directory
DATA_DIR = Path(__file__).parent.parent / 'data' / 'snapshots'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def fetch_alpaca_data():
    """
    Fetch account data and positions from Alpaca API and save to JSON file
    """
    # Initialize Alpaca trading client
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=ALPACA_PAPER)
    
    # Get account info
    account = trading_client.get_account()
    account_data = {
        'id': account.id,
        'cash': float(account.cash),
        'portfolio_value': float(account.portfolio_value),
        'buying_power': float(account.buying_power),
        'currency': account.currency,
        'account_status': account.status,
        'trading_blocked': account.trading_blocked,
        'equity': float(account.equity),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    # Get positions
    positions = trading_client.get_all_positions()
    positions_data = []
    
    for position in positions:
        positions_data.append({
            'symbol': position.symbol,
            'qty': float(position.qty),
            'market_value': float(position.market_value),
            'cost_basis': float(position.cost_basis),
            'unrealized_pl': float(position.unrealized_pl),
            'unrealized_plpc': float(position.unrealized_plpc),
            'current_price': float(position.current_price),
            'avg_entry_price': float(position.avg_entry_price),
            'side': position.side,
            'exchange': position.exchange
        })
    
    # Combine account and positions data
    data = {
        'account': account_data,
        'positions': positions_data,
        'cash': float(account.cash),  # Added for compatibility with app.py
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    return data

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle UUID objects"""
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def save_data(data, agent_name='default'):
    """
    Save data to a JSON file with timestamp in filename
    
    Args:
        data (dict): Data to save
        agent_name (str): Name of the agent
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{agent_name}_{timestamp}.json"
    filepath = DATA_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, cls=JSONEncoder)
    
    print(f"Saved data to {filepath}")
    return filepath

def run_job(agent_name='default'):
    """
    Run the job to fetch and save Alpaca positions data
    
    Args:
        agent_name (str): Name of the agent
    """
    try:
        data = fetch_alpaca_data()
        save_data(data, agent_name)
        return True, "Successfully fetched and saved Alpaca data"
    except Exception as e:
        error_msg = f"Error fetching Alpaca data: {str(e)}"
        print(error_msg)
        return False, error_msg

if __name__ == "__main__":
    # Run the job for the default agent
    success, message = run_job()
    print(message)
