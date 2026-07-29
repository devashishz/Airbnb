import streamlit as st
import pandas as pd
import duckdb
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import logging

st.set_page_config(
    page_title="Airbnb Analytics", 
    page_icon="🏘️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = 'airbnb_local.duckdb'


@st.cache_data(ttl="1h", show_spinner="Querying Lakehouse...")
def load_data() -> pd.DataFrame:
    """Fetches and preprocesses data from the DuckDB analytical backend."""
    try:
        # Senior best practice: Always connect BI tools in read-only mode
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            query = """
                SELECT 
                    review_id,
                    listing_id,
                    reviewer_name,
                    review_date,
                    review_text,
                    review_sentiment,
                    is_full_moon
                FROM main.mart_fullmoon_reviews
            """
            df = conn.execute(query).df()
            
        # Standardize column names to uppercase for consistent referencing
        df.columns = [col.upper() for col in df.columns]
        
        # Precompute types and flags safely
        df["REVIEW_DATE"] = pd.to_datetime(df["REVIEW_DATE"])
        # Strict equality check prevents the substring bug
        df["IS_FULL_MOON_FLAG"] = df["IS_FULL_MOON"].str.lower() == "full moon"
        
        return df

    except duckdb.Error as e:
        st.error(f"🚨 Fatal Error: Unable to connect to analytical backend. Details: {e}")
        st.stop()

# ==========================================
# CACHED COMPUTATION LAYER
# ==========================================
@st.cache_resource(show_spinner=False)
def generate_wordcloud_figure(text_corpus: str) -> plt.Figure:
    """Generates a matplotlib figure containing the wordcloud. 
    Cached via st.cache_resource because matplotlib figures are not easily serializable."""
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='#0E1117', # Matches Streamlit dark mode
        colormap='Blues',
        max_words=150
    ).generate(text_corpus)
    
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0E1117')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    # Ensure layout is tight to prevent weird whitespace in UI
    plt.tight_layout(pad=0) 
    return fig

# ==========================================
# UI COMPONENTS
# ==========================================
def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Renders the sidebar and applies filters to the dataframe."""
    st.sidebar.header("⚙️ Global Filters")

    sentiment_filter = st.sidebar.multiselect(
        "Review Sentiment",
        options=df["REVIEW_SENTIMENT"].unique(),
        default=list(df["REVIEW_SENTIMENT"].unique())
    )

    full_moon_filter = st.sidebar.radio(
        "Lunar Phase Filter",
        options=["All Dates", "Full Moon Only", "Regular Dates Only"]
    )

    min_date = df["REVIEW_DATE"].min().date()
    max_date = df["REVIEW_DATE"].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply Filtering Logic
    filtered_df = df[df["REVIEW_SENTIMENT"].isin(sentiment_filter)]

    if full_moon_filter == "Full Moon Only":
        filtered_df = filtered_df[filtered_df["IS_FULL_MOON_FLAG"]]
    elif full_moon_filter == "Regular Dates Only":
        filtered_df = filtered_df[~filtered_df["IS_FULL_MOON_FLAG"]]

    # Ensure date range has two values before filtering to prevent index errors
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["REVIEW_DATE"].dt.date >= date_range[0]) &
            (filtered_df["REVIEW_DATE"].dt.date <= date_range[1])
        ]

    return filtered_df

def render_kpi_metrics(df: pd.DataFrame):
    """Renders the top-level KPI metrics."""
    cols = st.columns(4)
    cols[0].metric("Total Reviews", f"{len(df):,}")
    cols[1].metric("Unique Listings", f"{df['LISTING_ID'].nunique():,}")
    cols[2].metric("Unique Reviewers", f"{df['REVIEWER_NAME'].nunique():,}")
    cols[3].metric("Full Moon Events", f"{df['IS_FULL_MOON_FLAG'].sum():,}")

# ==========================================
# MAIN APPLICATION
# ==========================================
def main():
    st.title("🏘️ Airbnb Review Intelligence")
    st.markdown("Automated sentiment tracking and lunar pattern analysis over listing reviews.")
    
    # 1. Load Data
    raw_df = load_data()
    
    # 2. Render Sidebar & Filter Data
    df = render_sidebar_filters(raw_df)
    
    if df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        st.stop()
        
    # 3. Render Top KPIs
    render_kpi_metrics(df)
    st.divider()

    # 4. Render Tabbed Interface
    tab_trends, tab_nlp, tab_raw = st.tabs(["📈 Market Trends", "💬 NLP & Sentiment", "🗄️ Raw Data Warehouse"])

    with tab_trends:
        st.subheader("Review Volume Over Time")
        time_series = df.copy()
        time_series["YearMonth"] = time_series["REVIEW_DATE"].dt.to_period("M").dt.to_timestamp()
        monthly_counts = time_series.groupby("YearMonth").size().reset_index(name="Count")

        # Upgraded Altair chart with tooltips and clean UI
        line_chart = alt.Chart(monthly_counts).mark_area(
            line={'color':'#1f77b4'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#1f77b4', offset=0),
                       alt.GradientStop(color='transparent', offset=1)],
                x1=1, x2=1, y1=1, y2=0
            ),
            opacity=0.6
        ).encode(
            x=alt.X("YearMonth:T", title="Date", axis=alt.Axis(grid=False)),
            y=alt.X("Count:Q", title="Number of Reviews", axis=alt.Axis(grid=True)),
            tooltip=[alt.Tooltip("YearMonth:T", title="Month", format="%B %Y"), 
                     alt.Tooltip("Count:Q", title="Reviews")]
        ).properties(height=400)
        
        st.altair_chart(line_chart, use_container_width=True)

    with tab_nlp:
        col_bar, col_cloud = st.columns([1, 1])
        
        with col_bar:
            st.subheader("Sentiment Distribution")
            sentiment_counts = df["REVIEW_SENTIMENT"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Volume"]

            bar_chart = alt.Chart(sentiment_counts).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                x=alt.X("Sentiment:N", sort='-y', axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Volume:Q", title="Total Reviews"),
                color=alt.Color("Sentiment:N", legend=None, scale=alt.Scale(scheme='tableau10')),
                tooltip=["Sentiment", "Volume"]
            ).properties(height=350)
            st.altair_chart(bar_chart, use_container_width=True)
            
        with col_cloud:
            st.subheader("Keyword Extraction")
            # Create sub-tabs for the wordclouds so they don't take up the whole page
            sentiments = df["REVIEW_SENTIMENT"].dropna().unique()
            cloud_tabs = st.tabs([s.capitalize() for s in sentiments])
            
            for i, sentiment in enumerate(sentiments):
                with cloud_tabs[i]:
                    text_corpus = " ".join(df[df["REVIEW_SENTIMENT"] == sentiment]["REVIEW_TEXT"].dropna().astype(str))
                    if text_corpus.strip():
                        # Call the cached function instead of generating on the fly
                        fig = generate_wordcloud_figure(text_corpus)
                        st.pyplot(fig)
                    else:
                        st.info("Insufficient textual data for this sentiment.")

    with tab_raw:
        st.subheader("Granular Review Extracts")
        st.dataframe(
            df[[
                "REVIEW_DATE",
                "REVIEW_ID",
                "LISTING_ID",
                "REVIEW_SENTIMENT",
                "IS_FULL_MOON",
                "REVIEW_TEXT"
            ]].sort_values(by="REVIEW_DATE", ascending=False),
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()