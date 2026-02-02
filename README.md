# NewsGraph - AI-Powered News Relationship Analysis System

## Overview
NewsGraph is a comprehensive AI/ML system designed for your hackathon project that analyzes news articles to discover hidden relationships and connections over time. Perfect for news channels, researchers, and journalists who want to understand how stories evolve and connect.

## 🚀 Quick Start

### 1. Installation
```bash
# Clone or download the project
cd NewsGraph

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. API Setup
Get free API keys from these 3 sources:

**NewsAPI.org** (1,000 requests/day)
- Go to: https://newsapi.org/register
- Sign up and get your API key
- Set environment variable: `NEWSAPI_KEY=your_key_here`

**The Guardian API** (12,000 requests/day)  
- Go to: https://bonobo.capi.gutools.co.uk/register/developer
- Register and get your API key
- Set environment variable: `GUARDIAN_API_KEY=your_key_here`

**NewsData.io** (200 requests/day)
- Go to: https://newsdata.io/register
- Create account and get API key
- Set environment variable: `NEWSDATA_API_KEY=your_key_here`

### 3. Run the Application
```bash
streamlit run app/main.py
```

## 🎯 Key Features for Your Hackathon

### 1. Multi-Source News Collection
- Automatically collects from 3 major news APIs
- Deduplicates and cleans data
- Handles rate limits and errors gracefully

### 2. AI-Powered Relationship Detection
- **Entity Recognition**: Finds people, organizations, locations
- **Semantic Similarity**: Uses transformer models to find related content
- **Temporal Analysis**: Tracks story evolution over time
- **Topic Clustering**: Groups related stories automatically

### 3. Network Graph Visualization
- Interactive network showing news connections
- Node-link diagrams like Google's knowledge graph
- Color-coded by topics, entities, and time
- Filterable and explorable interface

### 4. Deep Research Capabilities
- Track how stories develop over months/years
- Find hidden connections between events
- Identify patterns in news coverage
- Export data for further analysis

## 🏗️ Project Structure

```
NewsGraph/
├── app/                    # Streamlit web application
│   ├── main.py            # Main app interface
│   └── pages/             # Additional pages
├── src/                   # Core source code
│   ├── data_collection/   # News API integrations
│   ├── analysis/          # AI/ML analysis modules
│   ├── models/            # ML model training
│   └── visualization/     # Graph visualization
├── config/                # Configuration files
├── data/                  # Data storage
└── notebooks/             # Jupyter notebooks for development
```

## 🤖 AI/ML Components

### Relationship Detection Methods
1. **Entity-based**: Shared people, organizations, locations
2. **Semantic**: Content similarity using sentence transformers
3. **Temporal**: Follow-up stories and updates over time
4. **Clustering**: Topic-based grouping using DBSCAN

### Models Used
- **spaCy**: Named entity recognition
- **Sentence Transformers**: Semantic embeddings
- **scikit-learn**: Clustering and similarity
- **NetworkX**: Graph analysis

## 📊 Hackathon Demo Flow

### 1. Data Collection Demo
```python
# Collect news about a topic
articles = await collect_news("climate change", days_back=30)
print(f"Collected {len(articles)} articles from 3 APIs")
```

### 2. Relationship Analysis Demo
```python
# Analyze relationships
analyzer = RelationshipAnalyzer()
network = analyzer.analyze_news_network(articles)
print(f"Found {network['total_relationships']} relationships")
```

### 3. Visualization Demo
- Show interactive network graph
- Demonstrate filtering by time, entity, topic
- Export analysis reports

## 🎪 Hackathon Presentation Points

### Problem Statement
"News channels need to understand how stories connect and evolve over time, but manual analysis is impossible at scale."

### Solution
"AI-powered system that automatically discovers relationships between news articles using multiple analysis methods."

### Innovation
- **Multi-API Integration**: Comprehensive data collection
- **Advanced NLP**: Entity recognition + semantic analysis
- **Temporal Intelligence**: Tracks story evolution
- **Interactive Visualization**: Google-style knowledge graphs

### Impact
- **For Journalists**: Find story connections faster
- **For Researchers**: Analyze news patterns at scale  
- **For News Channels**: Understand coverage gaps and opportunities

## 🔧 Technical Highlights

### Scalable Architecture
- Async API calls for performance
- Caching for repeated queries
- Modular design for easy extension

### Advanced AI Features
- Transformer-based embeddings
- Multi-method relationship detection
- Confidence scoring for relationships
- Temporal pattern recognition

### Professional UI
- Clean Streamlit interface
- Real-time progress indicators
- Interactive visualizations
- Export capabilities

## 📈 Demo Scenarios

### Scenario 1: Political Coverage
- Collect articles about "election 2024"
- Show how candidate mentions connect
- Track story evolution over time

### Scenario 2: Business News
- Analyze "tech company mergers"
- Find connections between deals
- Identify market patterns

### Scenario 3: Crisis Tracking
- Monitor "natural disaster" coverage
- Track response and recovery stories
- Show government/organization involvement

## 🏆 Winning Features

1. **Real-world Problem**: Addresses actual journalism needs
2. **Technical Depth**: Multiple AI/ML techniques
3. **Practical Implementation**: Working demo with real APIs
4. **Scalable Design**: Can handle large datasets
5. **Visual Impact**: Interactive network graphs
6. **Export Capabilities**: Useful for real research

## 🚀 Future Enhancements

- Real-time news monitoring
- Sentiment analysis over time
- Bias detection across sources
- Mobile app interface
- API for third-party integration

## 📝 Usage Examples

See the `notebooks/` directory for detailed examples:
- `data_exploration.ipynb`: Data collection and cleaning
- `model_training.ipynb`: Relationship detection training
- `visualization_demo.ipynb`: Graph visualization examples

## 🤝 Team Roles Suggestion

- **Data Engineer**: API integration and data pipeline
- **ML Engineer**: Relationship detection algorithms  
- **Frontend Developer**: Streamlit UI and visualization
- **Product Manager**: Demo scenarios and presentation

This system gives you a complete, working AI/ML project that solves a real problem with impressive technical depth - perfect for hackathon success! 🏆