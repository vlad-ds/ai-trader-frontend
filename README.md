# AI Trader Frontend

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.30.0%2B-red.svg)

A Streamlit dashboard application for visualizing trading account information and positions from the Alpaca Trading API. The dashboard displays portfolio value, positions, profit/loss metrics, and trading diary entries.

## 📊 Features

- **Real-time Account Data**: View portfolio value, cash balance, and buying power
- **Positions Tracking**: Monitor your positions with detailed information on current prices, market values, and profit/loss
- **Trading Diary**: Keep track of your trading thoughts and strategies with date-organized diary entries
- **Collapsible Interface**: Clean UI with collapsible diary sections and intuitive navigation

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-trader-frontend.git
   cd ai-trader-frontend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```
   ALPACA_API_KEY=your_api_key
   ALPACA_SECRET_KEY=your_secret_key
   ALPACA_PAPER=true  # Use paper trading account
   ```

## 🚀 Usage

1. Run the Streamlit dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

2. Update portfolio data:
   ```bash
   cd dashboard/update_jobs
   python positions_job.py
   ```

## 📁 Project Structure

- `dashboard/app.py` - Main Streamlit application
- `dashboard/data/snapshots/` - JSON files of account snapshots
- `dashboard/data/diary/` - Markdown files for trading diary entries
- `dashboard/update_jobs/positions_job.py` - Job for fetching data from Alpaca API

## 📝 Data Format

- **Snapshots**: JSON files with naming pattern `{agent_name}_{YYYYMMDD_HHMMSS}.json`
- **Diary Entries**: Markdown files with naming pattern `{agent_name}_{YYYY-MM-DD}.md`

## 🔑 Environment Variables

- `ALPACA_API_KEY`: API key for Alpaca
- `ALPACA_SECRET_KEY`: Secret key for Alpaca
- `ALPACA_PAPER`: Whether to use paper trading (default: true)

## 📸 Screenshots

![Dashboard Overview](https://via.placeholder.com/800x450.png?text=AI+Trader+Dashboard)

## 🔄 Data Flow

```
Alpaca Trading API → positions_job.py → JSON snapshots → app.py → Dashboard UI
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 🙏 Acknowledgements

- [Alpaca API](https://alpaca.markets/) - For providing the trading API
- [Streamlit](https://streamlit.io/) - For the awesome dashboard framework
- [Pandas](https://pandas.pydata.org/) - For data manipulation capabilities