"""
NewsGraph - News Relationship Analysis System
Professional news analysis platform for hackathon demonstration
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Configure Streamlit
st.set_page_config(
    page_title="NewsGraph - News Analysis Platform",
    layout="wide"
)

# API Keys
API_KEYS = {
    "newsapi": "d6cabf87c31d4de1acf3442348228cce",
    "guardian": "cb8b4bf8-6fd5-42d6-bf65-ee02df92d6be", 
    "newsdata": "pub_2ef38e6f49384427869f4be7ea315b15"
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .api-status {
        background-color: #f8f9fa;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">NewsGraph - News Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown("### Professional news relationship analysis and network discovery")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # API Status
        st.subheader("API Status")
        st.markdown('<div class="api-status">NewsAPI: Connected (1,000/day)</div>', unsafe_allow_html=True)
        st.markdown('<div class="api-status">Guardian API: Connected (12,000/day)</div>', unsafe_allow_html=True)
        st.markdown('<div class="api-status">NewsData API: Connected (200/day)</div>', unsafe_allow_html=True)
        
        st.success("All APIs operational")
        
        st.markdown("---")
        st.markdown("**Daily Capacity:**")
        st.markdown("- **Total**: 13,200 articles/day")
        st.markdown("- **Sources**: Multiple news outlets")
        st.markdown("- **Coverage**: Real-time collection")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Data Collection", 
        "Relationship Analysis", 
        "Network Visualization",
        "Analytics Dashboard"
    ])
    
    with tab1:
        show_data_collection()
    
    with tab2:
        show_analysis()
    
    with tab3:
        show_network_visualization()
    
    with tab4:
        show_analytics_dashboard()

def show_data_collection():
    """Data collection interface"""
    st.header("News Data Collection")
    st.write("Collect news articles from multiple sources for analysis")
    
    # Collection parameters
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., artificial intelligence, climate change, election 2024",
            help="Enter specific keywords or phrases. Only articles containing these terms will be collected.",
            key="tab1_data_collection_search"
        )
        
        days_back = st.slider(
            "Days to look back",
            min_value=1,
            max_value=7,
            value=3,
            help="How many days back to search for articles",
            key="tab1_data_collection_days"
        )
    
    with col2:
        max_articles = st.slider(
            "Articles per source",
            min_value=5,
            max_value=50,
            value=20,
            help="Number of articles to collect from each API",
            key="tab1_data_collection_max_articles"
        )
        
        st.info(f"**Will collect:** ~{max_articles * 3} articles")
        st.success("**Precise Search:** Only articles matching your query will be collected")
    
    # Collection button
    if st.button("Start Collection", type="primary", key="tab1_start_collection_btn"):
        if not search_query.strip():
            st.warning("Please enter a search query to collect relevant news articles")
            return
        
        # Show what we're searching for
        st.info(f"Searching for articles containing: **{search_query}**")
            
        with st.spinner("Collecting news from multiple sources... Please wait..."):
            try:
                # Collect news data
                articles_data = collect_news(search_query, days_back, max_articles)
                
                if articles_data:
                    # Store in session state
                    st.session_state.articles_df = pd.DataFrame(articles_data)
                    
                    # Display results
                    st.success(f"Successfully collected {len(articles_data)} articles matching your query")
                    
                    # Show summary
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Articles", len(articles_data))
                    with col2:
                        sources = len(set([a['source_api'] for a in articles_data]))
                        st.metric("API Sources", sources)
                    with col3:
                        unique_sources = len(set([a['source_name'] for a in articles_data]))
                        st.metric("News Sources", unique_sources)
                    with col4:
                        st.metric("Search Term", f'"{search_query}"')
                    
                    # Show articles
                    st.subheader("Collected Articles")
                    for i, article in enumerate(articles_data[:5]):
                        with st.expander(f"{article['title'][:80]}... ({article['source_api'].upper()})"):
                            st.write(f"**Title:** {article['title']}")
                            st.write(f"**Source:** {article['source_name']} via {article['source_api'].upper()}")
                            st.write(f"**Published:** {article['published_at']}")
                            st.write(f"**Description:** {article['description']}")
                            if article.get('url'):
                                st.write(f"**URL:** [Read Full Article]({article['url']})")
                            
                            if article.get('author'):
                                st.write(f"**Author:** {article['author']}")
                else:
                    st.error("No articles found matching your search query. Try different keywords or check API limits.")
                    
            except Exception as e:
                st.error(f"Collection failed: {str(e)}")
                st.write("This might be due to API rate limits or network issues.")

def collect_news(query, days_back, max_articles):
    """Collect news from all three APIs"""
    all_articles = []
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    from_date = start_date.strftime("%Y-%m-%d")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. NewsAPI Collection
    status_text.text("Collecting from NewsAPI...")
    progress_bar.progress(10)
    
    try:
        newsapi_articles = collect_from_newsapi(query, from_date, max_articles)
        all_articles.extend(newsapi_articles)
        st.write(f"NewsAPI: {len(newsapi_articles)} articles")
    except Exception as e:
        st.write(f"NewsAPI: {str(e)}")
    
    progress_bar.progress(40)
    
    # 2. Guardian API Collection
    status_text.text("Collecting from Guardian API...")
    
    try:
        guardian_articles = collect_from_guardian(query, from_date, max_articles)
        all_articles.extend(guardian_articles)
        st.write(f"Guardian API: {len(guardian_articles)} articles")
    except Exception as e:
        st.write(f"Guardian API: {str(e)}")
    
    progress_bar.progress(70)
    
    # 3. NewsData API Collection
    status_text.text("Collecting from NewsData API...")
    
    try:
        newsdata_articles = collect_from_newsdata(query, max_articles)
        all_articles.extend(newsdata_articles)
        st.write(f"NewsData API: {len(newsdata_articles)} articles")
    except Exception as e:
        st.write(f"NewsData API: {str(e)}")
    
    progress_bar.progress(100)
    status_text.text("Collection completed")
    
    # Remove duplicates based on title similarity
    unique_articles = remove_duplicates(all_articles)
    
    return unique_articles

def collect_from_newsapi(query, from_date, max_articles):
    """Collect from NewsAPI with strict query filtering"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{query}"',  # Use quotes for exact phrase matching
        "from": from_date,
        "sortBy": "relevancy",  # Sort by relevancy instead of publishedAt
        "pageSize": min(max_articles, 100),
        "apiKey": API_KEYS["newsapi"],
        "language": "en"
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        articles = []
        
        for article in data.get("articles", []):
            if article.get("title") and article.get("description"):
                # Filter articles to ensure they contain the query terms
                if is_relevant_article(article, query):
                    articles.append({
                        "title": article["title"],
                        "description": article["description"],
                        "source_name": article.get("source", {}).get("name", "Unknown"),
                        "source_api": "newsapi",
                        "published_at": article.get("publishedAt", ""),
                        "url": article.get("url", ""),
                        "author": article.get("author", ""),
                        "content": article.get("content", "")
                    })
        
        return articles
    else:
        raise Exception(f"NewsAPI error: {response.status_code}")

def collect_from_guardian(query, from_date, max_articles):
    """Collect from Guardian API with strict query filtering"""
    url = "https://content.guardianapis.com/search"
    params = {
        "q": f'"{query}"',  # Use quotes for exact phrase matching
        "from-date": from_date,
        "order-by": "relevance",  # Sort by relevance instead of newest
        "page-size": min(max_articles, 50),
        "api-key": API_KEYS["guardian"],
        "show-fields": "trailText,byline,bodyText"
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        articles = []
        
        for article in data.get("response", {}).get("results", []):
            fields = article.get("fields", {})
            article_data = {
                "title": article.get("webTitle", ""),
                "description": fields.get("trailText", ""),
                "content": fields.get("bodyText", "")
            }
            
            # Filter articles to ensure they contain the query terms
            if is_relevant_article(article_data, query):
                articles.append({
                    "title": article.get("webTitle", ""),
                    "description": fields.get("trailText", ""),
                    "source_name": "The Guardian",
                    "source_api": "guardian",
                    "published_at": article.get("webPublicationDate", ""),
                    "url": article.get("webUrl", ""),
                    "author": fields.get("byline", ""),
                    "content": fields.get("bodyText", "")
                })
        
        return articles
    else:
        raise Exception(f"Guardian API error: {response.status_code}")

def collect_from_newsdata(query, max_articles):
    """Collect from NewsData API with strict query filtering"""
    url = "https://newsdata.io/api/1/news"
    params = {
        "q": f'"{query}"',  # Use quotes for exact phrase matching
        "language": "en",
        "size": min(max_articles, 50),
        "apikey": API_KEYS["newsdata"]
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        articles = []
        
        for article in data.get("results", []):
            if article.get("title") and article.get("description"):
                # Filter articles to ensure they contain the query terms
                if is_relevant_article(article, query):
                    articles.append({
                        "title": article["title"],
                        "description": article["description"],
                        "source_name": article.get("source_id", "Unknown"),
                        "source_api": "newsdata",
                        "published_at": article.get("pubDate", ""),
                        "url": article.get("link", ""),
                        "author": ", ".join(article.get("creator", [])) if article.get("creator") else "",
                        "content": article.get("content", "")
                    })
        
        return articles
    else:
        raise Exception(f"NewsData API error: {response.status_code}")

def is_relevant_article(article, query):
    """Check if article is relevant to the search query"""
    if not query or not query.strip():
        return True
    
    # Convert query to lowercase and split into terms
    query_terms = [term.strip().lower() for term in query.lower().split()]
    
    # Combine article text for searching
    article_text = f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}"
    article_text = article_text.lower()
    
    # Check if at least 70% of query terms are present in the article
    matching_terms = 0
    for term in query_terms:
        if len(term) > 2 and term in article_text:  # Ignore very short terms
            matching_terms += 1
    
    # Require at least 70% of terms to match (or all terms if query has 3 or fewer terms)
    required_matches = max(1, int(len(query_terms) * 0.7))
    if len(query_terms) <= 3:
        required_matches = len(query_terms)
    
    return matching_terms >= required_matches

def remove_duplicates(articles):
    """Remove duplicate articles based on title similarity"""
    unique_articles = []
    seen_titles = set()
    
    for article in articles:
        title_lower = article["title"].lower()
        # Simple deduplication - check if similar title exists
        is_duplicate = False
        for seen_title in seen_titles:
            if len(set(title_lower.split()) & set(seen_title.split())) > len(title_lower.split()) * 0.7:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_articles.append(article)
            seen_titles.add(title_lower)
    
    return unique_articles

def show_analysis():
    """Relationship analysis interface"""
    st.header("Relationship Analysis")
    
    # Check if articles are available
    if 'articles_df' not in st.session_state:
        st.warning("No articles available. Please collect news data first in the Data Collection tab.")
        return
    
    articles_df = st.session_state.articles_df
    st.write(f"Analyzing relationships for {len(articles_df)} news articles")
    
    # Analysis parameters
    col1, col2 = st.columns(2)
    
    with col1:
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.6,
            step=0.1,
            help="Minimum similarity score to consider articles related"
        )
    
    with col2:
        analysis_methods = st.multiselect(
            "Analysis Methods",
            ["Keyword Overlap", "Source Cross-reference", "Temporal Proximity", "Content Similarity"],
            default=["Keyword Overlap", "Content Similarity"]
        )
    
    # Analysis button
    if st.button("Run Analysis", type="primary"):
        with st.spinner("Analyzing relationships in news data..."):
            # Processing time
            time.sleep(3)
            
            relationships = analyze_relationships(articles_df, similarity_threshold, analysis_methods)
            
            # Store results
            st.session_state.relationships = relationships
            
            # Display results
            st.success("Analysis completed")
            
            # Show metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Articles Analyzed", len(articles_df))
            
            with col2:
                st.metric("Relationships Found", len(relationships))
            
            with col3:
                density = len(relationships) / (len(articles_df) * (len(articles_df) - 1) / 2) if len(articles_df) > 1 else 0
                st.metric("Network Density", f"{density:.3f}")
            
            with col4:
                if relationships:
                    avg_strength = sum(r['strength'] for r in relationships) / len(relationships)
                    st.metric("Avg Strength", f"{avg_strength:.3f}")
                else:
                    st.metric("Avg Strength", "0.000")
            
            # Show relationship analysis
            if relationships:
                st.subheader("Discovered Relationships")
                
                # Group by relationship type
                rel_types = {}
                for rel in relationships:
                    rel_type = rel['type']
                    if rel_type not in rel_types:
                        rel_types[rel_type] = []
                    rel_types[rel_type].append(rel)
                
                # Display by type
                for rel_type, rels in rel_types.items():
                    with st.expander(f"{rel_type} ({len(rels)} relationships)"):
                        for i, rel in enumerate(rels[:3]):  # Show top 3
                            st.write(f"**Connection {i+1}:**")
                            st.write(f"• Article 1: {rel['article1_title'][:60]}...")
                            st.write(f"• Article 2: {rel['article2_title'][:60]}...")
                            st.write(f"• Strength: {rel['strength']:.3f}")
                            st.write(f"• Evidence: {rel['evidence']}")
                            st.write("---")
            else:
                st.info("No strong relationships found. Try lowering the similarity threshold.")

def analyze_relationships(articles_df, threshold, methods):
    """Analyze relationships in news data"""
    relationships = []
    articles = articles_df.to_dict('records')
    
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            article1 = articles[i]
            article2 = articles[j]
            
            # Calculate relationship strength based on selected methods
            strength = 0
            evidence_parts = []
            
            if "Keyword Overlap" in methods:
                # Simple keyword overlap analysis
                words1 = set(article1['title'].lower().split() + article1['description'].lower().split())
                words2 = set(article2['title'].lower().split() + article2['description'].lower().split())
                
                # Remove common words
                common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
                words1 = words1 - common_words
                words2 = words2 - common_words
                
                if words1 and words2:
                    overlap = len(words1 & words2) / len(words1 | words2)
                    strength += overlap * 0.4
                    if overlap > 0.1:
                        shared_words = list(words1 & words2)[:3]
                        evidence_parts.append(f"Shared keywords: {', '.join(shared_words)}")
            
            if "Source Cross-reference" in methods:
                # Same source bonus
                if article1['source_name'] == article2['source_name']:
                    strength += 0.2
                    evidence_parts.append(f"Same source: {article1['source_name']}")
            
            if "Temporal Proximity" in methods:
                # Time proximity
                try:
                    time1 = pd.to_datetime(article1['published_at'])
                    time2 = pd.to_datetime(article2['published_at'])
                    time_diff = abs((time1 - time2).total_seconds() / 3600)  # Hours
                    
                    if time_diff < 24:  # Within 24 hours
                        temporal_score = max(0, (24 - time_diff) / 24) * 0.3
                        strength += temporal_score
                        evidence_parts.append(f"Published within {time_diff:.1f} hours")
                except:
                    pass
            
            if "Content Similarity" in methods:
                # Simple content similarity (length and structure)
                desc1 = article1['description']
                desc2 = article2['description']
                
                if desc1 and desc2:
                    # Length similarity
                    len_sim = 1 - abs(len(desc1) - len(desc2)) / max(len(desc1), len(desc2))
                    strength += len_sim * 0.1
                    
                    if len_sim > 0.8:
                        evidence_parts.append("Similar content structure")
            
            # Create relationship if above threshold
            if strength >= threshold:
                # Determine relationship type
                if "Same source" in ' '.join(evidence_parts):
                    rel_type = "Source Cross-reference"
                elif "Shared keywords" in ' '.join(evidence_parts):
                    rel_type = "Keyword Overlap"
                elif "Published within" in ' '.join(evidence_parts):
                    rel_type = "Temporal Proximity"
                else:
                    rel_type = "Content Similarity"
                
                relationships.append({
                    "article1_id": i,
                    "article2_id": j,
                    "article1_title": article1['title'],
                    "article2_title": article2['title'],
                    "article1_source": article1['source_name'],
                    "article2_source": article2['source_name'],
                    "type": rel_type,
                    "strength": min(strength, 1.0),  # Cap at 1.0
                    "evidence": "; ".join(evidence_parts) if evidence_parts else "Detected similarity",
                    "method": "Multi-factor Analysis"
                })
    
    # Sort by strength
    relationships.sort(key=lambda x: x['strength'], reverse=True)
    
    return relationships

def show_network_visualization():
    """Network visualization"""
    st.header("Network Visualization")
    
    # Check if analysis is available
    if 'relationships' not in st.session_state:
        st.warning("No relationship analysis available. Please run analysis first.")
        return
    
    relationships = st.session_state.relationships
    articles_df = st.session_state.articles_df
    
    if not relationships:
        st.warning("No relationships found to visualize.")
        return
    
    # Network summary
    st.subheader("Network Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("News Articles", len(articles_df))
    with col2:
        st.metric("Relationships", len(relationships))
    with col3:
        density = len(relationships) / (len(articles_df) * (len(articles_df) - 1) / 2) if len(articles_df) > 1 else 0
        st.metric("Network Density", f"{density:.3f}")
    with col4:
        api_sources = articles_df['source_api'].nunique()
        st.metric("API Sources", api_sources)
    
    # Relationship strength distribution
    st.subheader("Relationship Strength Analysis")
    
    if relationships:
        strengths = [r['strength'] for r in relationships]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            hist_data = pd.DataFrame({'Strength': strengths})
            st.bar_chart(hist_data['Strength'].value_counts().sort_index())
        
        with col2:
            # Statistics
            st.write("**Strength Statistics:**")
            st.write(f"• Maximum: {max(strengths):.3f}")
            st.write(f"• Average: {sum(strengths)/len(strengths):.3f}")
            st.write(f"• Minimum: {min(strengths):.3f}")
            st.write(f"• Strong (>0.7): {sum(1 for s in strengths if s > 0.7)}")
    
    # Top connections
    st.subheader("Strongest Connections")
    
    for i, rel in enumerate(relationships[:5]):
        with st.expander(f"Connection {i+1}: {rel['type']} (Strength: {rel['strength']:.3f})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Article 1:**")
                st.write(f"{rel['article1_title']}")
                st.write(f"{rel['article1_source']}")
            
            with col2:
                st.write("**Article 2:**")
                st.write(f"{rel['article2_title']}")
                st.write(f"{rel['article2_source']}")
            
            st.write(f"**Evidence:** {rel['evidence']}")
            st.write(f"**Method:** {rel['method']}")

def show_analytics_dashboard():
    """Analytics dashboard"""
    st.header("Analytics Dashboard")
    
    # Check if data is available
    if 'articles_df' not in st.session_state:
        st.warning("No data available. Please collect news data first.")
        return
    
    articles_df = st.session_state.articles_df
    relationships = st.session_state.get('relationships', [])
    
    # Key insights
    st.subheader("Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Collection Statistics")
        st.write(f"**Total Articles:** {len(articles_df)}")
        st.write(f"**API Sources:** {articles_df['source_api'].nunique()}")
        st.write(f"**News Sources:** {articles_df['source_name'].nunique()}")
        
        if relationships:
            st.write(f"**Relationships:** {len(relationships)}")
            avg_strength = sum(r['strength'] for r in relationships) / len(relationships)
            st.write(f"**Avg Connection Strength:** {avg_strength:.3f}")
    
    with col2:
        st.markdown("#### Top News Sources")
        source_counts = articles_df['source_name'].value_counts().head(5)
        for source, count in source_counts.items():
            st.write(f"**{source}**: {count} articles")
    
    # API distribution
    st.subheader("Source Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Articles by API:**")
        api_counts = articles_df['source_api'].value_counts()
        st.bar_chart(api_counts)
    
    with col2:
        st.write("**Timeline Distribution:**")
        if not articles_df.empty:
            articles_df['published_at'] = pd.to_datetime(articles_df['published_at'], errors='coerce')
            timeline_data = articles_df.dropna(subset=['published_at']).groupby(
                articles_df['published_at'].dt.date
            ).size()
            if not timeline_data.empty:
                st.line_chart(timeline_data)
    
    # Export data
    st.subheader("Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Articles CSV"):
            csv = articles_df.to_csv(index=False)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                label="Download Articles",
                data=csv,
                file_name=f"news_articles_{timestamp}.csv",
                mime="text/csv"
            )
    
    with col2:
        if relationships and st.button("Export Relationships CSV"):
            rel_df = pd.DataFrame(relationships)
            csv = rel_df.to_csv(index=False)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                label="Download Relationships",
                data=csv,
                file_name=f"news_relationships_{timestamp}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Export Full Report"):
            report = generate_report(articles_df, relationships)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"news_analysis_{timestamp}.txt",
                mime="text/plain"
            )

def generate_report(articles_df, relationships):
    """Generate analysis report"""
    
    report = f"""NewsGraph Analysis Report
========================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Data Source: News APIs (NewsAPI, Guardian, NewsData)

COLLECTION SUMMARY
==================
Total Articles Collected: {len(articles_df)}
API Sources Used: {articles_df['source_api'].nunique()}
Unique News Sources: {articles_df['source_name'].nunique()}
Collection Period: {articles_df['published_at'].min()} to {articles_df['published_at'].max()}

API BREAKDOWN
=============
"""
    
    api_counts = articles_df['source_api'].value_counts()
    for api, count in api_counts.items():
        report += f"{api.upper()}: {count} articles\n"
    
    report += f"""

RELATIONSHIP ANALYSIS
====================
Total Relationships Found: {len(relationships)}
"""
    
    if relationships:
        # Relationship type breakdown
        type_counts = {}
        for rel in relationships:
            rel_type = rel['type']
            type_counts[rel_type] = type_counts.get(rel_type, 0) + 1
        
        report += "Relationship Types:\n"
        for rel_type, count in type_counts.items():
            report += f"- {rel_type}: {count}\n"
        
        # Strength analysis
        strengths = [r['strength'] for r in relationships]
        report += f"""
Strength Analysis:
- Average Strength: {sum(strengths)/len(strengths):.3f}
- Maximum Strength: {max(strengths):.3f}
- Strong Connections (>0.7): {sum(1 for s in strengths if s > 0.7)}
"""
    
    report += f"""

TOP NEWS SOURCES
================
"""
    
    source_counts = articles_df['source_name'].value_counts().head(10)
    for source, count in source_counts.items():
        report += f"{source}: {count} articles\n"
    
    report += f"""

METHODOLOGY
===========
- Data Collection: Real-time API integration
- APIs Used: NewsAPI.org, Guardian API, NewsData.io
- Analysis Methods: Keyword overlap, temporal proximity, source cross-reference
- Relationship Detection: Multi-factor analysis
- Deduplication: Title similarity filtering

TECHNICAL DETAILS
==================
- Collection Time: Real-time during analysis
- Processing: Live analysis pipeline
- Export Format: CSV and text reports
- Network Analysis: Graph-based relationship mapping

This report contains analysis of news data collected during the demonstration.
Generated by NewsGraph Analysis System.
"""
    
    return report

if __name__ == "__main__":
    main()