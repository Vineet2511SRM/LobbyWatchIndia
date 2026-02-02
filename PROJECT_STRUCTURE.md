# NewsGraph - Clean Project Structure

## 📁 Project Layout

```
NewsGraph/
├── app/                    # Main application
│   ├── __init__.py
│   └── live_demo.py       # Main Streamlit app
├── config/                # Configuration
│   ├── __init__.py
│   └── api_keys.py        # API keys configuration
├── data/                  # Data directories (ignored by git)
│   ├── models/           # Model files
│   ├── processed/        # Processed data
│   └── raw/              # Raw data
├── newsgraph_env/        # Virtual environment (ignored by git)
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── run.bat             # Application launcher
```

## 🚀 Quick Start

1. **Run the application:**
   ```bash
   ./run.bat
   ```

2. **Manual setup (if needed):**
   ```bash
   # Activate virtual environment
   ./newsgraph_env/Scripts/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run application
   streamlit run app/live_demo.py
   ```

## 📋 Key Files

- **`app/live_demo.py`** - Main Streamlit application with news collection and analysis
- **`config/api_keys.py`** - API keys for NewsAPI, Guardian, and NewsData
- **`requirements.txt`** - All Python dependencies
- **`run.bat`** - Automated setup and launch script
- **`.gitignore`** - Comprehensive ignore rules to minimize commits

## 🔧 Features

- **News Collection** - Real-time data from 3 APIs (13,200+ articles/day capacity)
- **Relationship Analysis** - Multi-factor analysis of news connections
- **Network Visualization** - Interactive relationship mapping
- **Analytics Dashboard** - Comprehensive insights and export capabilities

## 📊 API Configuration

The application uses three news APIs:
- **NewsAPI.org** - 1,000 requests/day
- **Guardian API** - 12,000 requests/day  
- **NewsData.io** - 200 requests/day

API keys are configured in `config/api_keys.py`.

## 🎯 Ready for Demo

This clean structure is optimized for:
- ✅ Minimal git commits
- ✅ Professional presentation
- ✅ Easy deployment
- ✅ Hackathon demonstration