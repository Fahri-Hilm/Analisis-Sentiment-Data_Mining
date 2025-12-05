"""
🏆 DASHBOARD ANALISIS SENTIMEN TIMNAS INDONESIA - UPGRADED v2
Versi 8.0 - Enhanced Edition dengan Fitur Lengkap
✨ Time-series | Advanced Filtering | Export | Model Performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Sentimen Timnas Indonesia - Enhanced",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM CSS
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Poppins', -apple-system, sans-serif !important; }
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #e8eef7 100%); }
    .block-container { padding: 2rem 3rem; max-width: 1600px; }
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/processed/comments_cleaned.csv')
        df['published_at'] = pd.to_datetime(df.get('published_at', datetime.now()))
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================
st.sidebar.title("🎛️ Filters & Settings")

df = load_data()
if df is not None:
    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(df['published_at'].min().date(), df['published_at'].max().date()),
        key="date_range"
    )
    
    # Sentiment filter
    st.sidebar.subheader("😊 Sentiment Filter")
    sentiments = df['core_sentiment'].unique().tolist()
    selected_sentiments = st.sidebar.multiselect(
        "Select sentiments",
        sentiments,
        default=sentiments
    )
    
    # Keyword filter
    st.sidebar.subheader("🔍 Keyword Filter")
    keyword = st.sidebar.text_input("Search keyword (optional)")
    
    # Apply filters
    filtered_df = df[
        (df['published_at'].dt.date >= date_range[0]) &
        (df['published_at'].dt.date <= date_range[1]) &
        (df['core_sentiment'].isin(selected_sentiments))
    ]
    
    if keyword:
        filtered_df = filtered_df[
            filtered_df['clean_text'].str.contains(keyword, case=False, na=False)
        ]
    
    # Display filter info
    st.sidebar.info(f"📊 Showing {len(filtered_df)} of {len(df)} comments")
    
    # ========================================================================
    # MAIN CONTENT
    # ========================================================================
    st.title("⚽ Analisis Sentimen Timnas Indonesia")
    st.markdown("---")
    
    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📈 Trends",
        "🔍 Details",
        "📋 Samples",
        "⚙️ Export"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Comments",
                len(filtered_df),
                delta=len(filtered_df) - len(df) if len(filtered_df) != len(df) else None
            )
        
        with col2:
            positive_count = len(filtered_df[filtered_df['core_sentiment'].str.contains('positive|Positive', case=False, na=False)])
            st.metric("Positive", positive_count, f"{positive_count/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
        
        with col3:
            negative_count = len(filtered_df[filtered_df['core_sentiment'].str.contains('negative|Negative', case=False, na=False)])
            st.metric("Negative", negative_count, f"{negative_count/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
        
        with col4:
            neutral_count = len(filtered_df) - positive_count - negative_count
            st.metric("Neutral", neutral_count, f"{neutral_count/len(filtered_df)*100:.1f}%" if len(filtered_df) > 0 else "0%")
        
        st.markdown("---")
        
        # Sentiment distribution
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_counts = filtered_df['core_sentiment'].value_counts()
            fig = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Broad sentiment
            def map_sentiment(label):
                if 'positive' in str(label).lower():
                    return 'Positive'
                elif 'negative' in str(label).lower():
                    return 'Negative'
                else:
                    return 'Neutral'
            
            filtered_df['broad_sentiment'] = filtered_df['core_sentiment'].apply(map_sentiment)
            broad_counts = filtered_df['broad_sentiment'].value_counts()
            
            fig = px.bar(
                x=broad_counts.index,
                y=broad_counts.values,
                title="Broad Sentiment",
                labels={'x': 'Sentiment', 'y': 'Count'},
                color=broad_counts.index,
                color_discrete_map={'Positive': '#4CAF50', 'Negative': '#F44336', 'Neutral': '#2196F3'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Sentiment Trends Over Time")
        
        # Time-series data
        daily_sentiment = filtered_df.groupby([filtered_df['published_at'].dt.date, 'broad_sentiment']).size().unstack(fill_value=0)
        
        if len(daily_sentiment) > 0:
            fig = go.Figure()
            for sentiment in daily_sentiment.columns:
                fig.add_trace(go.Scatter(
                    x=daily_sentiment.index,
                    y=daily_sentiment[sentiment],
                    mode='lines+markers',
                    name=sentiment,
                    fill='tozeroy'
                ))
            
            fig.update_layout(
                title="Sentiment Trends",
                xaxis_title="Date",
                yaxis_title="Count",
                hovermode='x unified',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Comparison metrics
        st.subheader("📊 Period Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            period1 = st.date_input("Period 1 Start", value=date_range[0], key="p1_start")
            period1_end = st.date_input("Period 1 End", value=date_range[0] + timedelta(days=7), key="p1_end")
        
        with col2:
            period2 = st.date_input("Period 2 Start", value=date_range[0] + timedelta(days=8), key="p2_start")
            period2_end = st.date_input("Period 2 End", value=date_range[1], key="p2_end")
        
        p1_data = filtered_df[(filtered_df['published_at'].dt.date >= period1) & (filtered_df['published_at'].dt.date <= period1_end)]
        p2_data = filtered_df[(filtered_df['published_at'].dt.date >= period2) & (filtered_df['published_at'].dt.date <= period2_end)]
        
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.metric("Period 1 Comments", len(p1_data), delta=len(p1_data) - len(p2_data))
        
        with comp_col2:
            p1_pos = len(p1_data[p1_data['broad_sentiment'] == 'Positive'])
            p2_pos = len(p2_data[p2_data['broad_sentiment'] == 'Positive'])
            st.metric("Period 1 Positive %", f"{p1_pos/len(p1_data)*100:.1f}%" if len(p1_data) > 0 else "0%", delta=f"{(p1_pos/len(p1_data) - p2_pos/len(p2_data))*100:.1f}%" if len(p1_data) > 0 and len(p2_data) > 0 else None)
        
        with comp_col3:
            p1_neg = len(p1_data[p1_data['broad_sentiment'] == 'Negative'])
            p2_neg = len(p2_data[p2_data['broad_sentiment'] == 'Negative'])
            st.metric("Period 1 Negative %", f"{p1_neg/len(p1_data)*100:.1f}%" if len(p1_data) > 0 else "0%", delta=f"{(p1_neg/len(p1_data) - p2_neg/len(p2_data))*100:.1f}%" if len(p1_data) > 0 and len(p2_data) > 0 else None)
    
    with tab3:
        st.subheader("🔍 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Keywords by Sentiment")
            selected_sentiment = st.selectbox("Select sentiment", filtered_df['core_sentiment'].unique())
            
            sentiment_texts = filtered_df[filtered_df['core_sentiment'] == selected_sentiment]['clean_text']
            if len(sentiment_texts) > 0:
                all_words = ' '.join(sentiment_texts).split()
                word_freq = Counter(all_words)
                top_words = dict(word_freq.most_common(15))
                
                fig = px.bar(
                    x=list(top_words.keys()),
                    y=list(top_words.values()),
                    title=f"Top Keywords - {selected_sentiment}",
                    labels={'x': 'Keyword', 'y': 'Frequency'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Sentiment Label Distribution")
            label_counts = filtered_df['core_sentiment'].value_counts().head(10)
            
            fig = px.bar(
                y=label_counts.index,
                x=label_counts.values,
                orientation='h',
                title="Top 10 Sentiment Labels",
                labels={'x': 'Count', 'y': 'Label'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("📋 Sample Comments")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sample_sentiment = st.selectbox("Filter by sentiment", ["All"] + filtered_df['core_sentiment'].unique().tolist())
        
        with col2:
            sample_count = st.slider("Number of samples", 1, 20, 5)
        
        if sample_sentiment == "All":
            samples = filtered_df.sample(min(sample_count, len(filtered_df)))
        else:
            sentiment_data = filtered_df[filtered_df['core_sentiment'] == sample_sentiment]
            samples = sentiment_data.sample(min(sample_count, len(sentiment_data))) if len(sentiment_data) > 0 else pd.DataFrame()
        
        for idx, row in samples.iterrows():
            with st.container():
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.write(f"**{row['core_sentiment']}**")
                    st.write(row['clean_text'])
                with col2:
                    st.write(f"📅 {row['published_at'].strftime('%Y-%m-%d')}")
                st.divider()
    
    with tab5:
        st.subheader("⚙️ Export & Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📥 Export Data")
            
            if st.button("📊 Export as CSV"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"sentimen_timnas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📈 Export Summary"):
                summary = {
                    'Total Comments': len(filtered_df),
                    'Positive': len(filtered_df[filtered_df['broad_sentiment'] == 'Positive']),
                    'Negative': len(filtered_df[filtered_df['broad_sentiment'] == 'Negative']),
                    'Neutral': len(filtered_df[filtered_df['broad_sentiment'] == 'Neutral']),
                    'Export Date': datetime.now().isoformat()
                }
                summary_df = pd.DataFrame([summary])
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="Download Summary",
                    data=csv,
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.subheader("📊 Statistics")
            st.write(f"**Total Comments**: {len(filtered_df)}")
            st.write(f"**Date Range**: {date_range[0]} to {date_range[1]}")
            st.write(f"**Unique Sentiments**: {filtered_df['core_sentiment'].nunique()}")
            st.write(f"**Average Comment Length**: {filtered_df['clean_text'].str.len().mean():.0f} characters")

else:
    st.error("❌ Data tidak ditemukan. Pastikan file CSV sudah ada di data/processed/")
