# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Trader Frontend is a dashboard application built with Streamlit that visualizes trading account information and positions from Alpaca Trading API. The application displays portfolio value, positions, profit/loss metrics, and trading diary entries.

## Architecture

The project has two main components:

1. **Dashboard (app.py)**: A Streamlit web application that displays portfolio data including:
   - Account metrics (portfolio value, cash balance)
   - Positions with details (symbol, quantity, value, P&L)
   - Trading diary entries

2. **Data Collection (update_jobs/positions_job.py)**: A job that:
   - Connects to Alpaca Trading API
   - Fetches account and position data
   - Saves the data as timestamped JSON snapshots

Data flows:
- Alpaca Trading API → positions_job.py → JSON snapshots → app.py → Dashboard UI

## Commands

### Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
ALPACA_API_KEY=your_api_key
ALPACA_SECRET_KEY=your_secret_key
ALPACA_PAPER=true  # Use paper trading account
```

### Running the Application

```bash
# Run the Streamlit dashboard
cd dashboard
streamlit run app.py

# Update portfolio data
cd dashboard/update_jobs
python positions_job.py
```

## Data Structure

- **Snapshots**: JSON files in `dashboard/data/snapshots/` with naming pattern `{agent_name}_{YYYYMMDD_HHMMSS}.json`
- **Diary Entries**: Markdown files in `dashboard/data/diary/` with naming pattern `{agent_name}_{YYYY-MM-DD}.md`

## Environment Variables

- `ALPACA_API_KEY`: API key for Alpaca
- `ALPACA_SECRET_KEY`: Secret key for Alpaca
- `ALPACA_PAPER`: Whether to use paper trading (default: true)