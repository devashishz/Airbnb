import streamlit as st
import pandas as pd
import duckdb
import altair as alt

st.set_page_config(
    page_title="Olist E-Commerce Intelligence", 
    page_icon="📦", 
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = 'olist_local.duckdb'

@st.cache_data(ttl="1h", show_spinner="Fetching Order Statuses...")
def get_available_statuses():
    """Fetches the unique order statuses dynamically from the DB."""
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            query = "SELECT DISTINCT order_status FROM main_gold.fct_orders WHERE order_status IS NOT NULL"
            df = conn.execute(query).df()
            return df['order_status'].tolist()
    except duckdb.Error:
        # Fallback if db hasn't been initialized yet
        return ["delivered", "shipped", "canceled", "invoiced", "processing", "unavailable", "approved"]

def get_kpi_metrics(status_filter: list) -> dict:
    """Calculates top-level metrics directly in DuckDB."""
    if not status_filter:
        return {"total_revenue": 0, "total_orders": 0, "avg_delivery": 0, "avg_basket": 0}
        
    placeholders = ", ".join(["?"] * len(status_filter))
    query = f"""
        SELECT 
            SUM(calculated_order_cost) AS total_revenue,
            COUNT(*) AS total_orders,
            AVG(days_to_delivery) AS avg_delivery,
            AVG(total_items_in_order) AS avg_basket
        FROM main_gold.fct_orders
        WHERE order_status IN ({placeholders})
    """
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            result = conn.execute(query, status_filter).fetchone()
    except duckdb.Error:
        result = (0, 0, 0, 0)
        
    return {
        "total_revenue": result[0] or 0,
        "total_orders": result[1] or 0,
        "avg_delivery": result[2] or 0,
        "avg_basket": result[3] or 0
    }

def get_monthly_revenue_trends(status_filter: list) -> pd.DataFrame:
    """Pre-aggregates monthly revenue in DuckDB for lightweight plotting."""
    if not status_filter:
        return pd.DataFrame()
        
    placeholders = ", ".join(["?"] * len(status_filter))
    query = f"""
        SELECT 
            DATE_TRUNC('month', purchased_at) AS YearMonth,
            SUM(calculated_order_cost) AS revenue
        FROM main_gold.fct_orders
        WHERE purchased_at IS NOT NULL
          AND order_status IN ({placeholders})
        GROUP BY 1
        ORDER BY 1
    """
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            df = conn.execute(query, status_filter).df()
            if not df.empty:
                df['YearMonth'] = pd.to_datetime(df['YearMonth'])
            return df
    except duckdb.Error:
        return pd.DataFrame(columns=["YearMonth", "revenue"])

def get_delivery_data(status_filter: list) -> pd.DataFrame:
    """Fetches only the days to delivery column for distribution visualization."""
    if not status_filter:
        return pd.DataFrame()
        
    placeholders = ", ".join(["?"] * len(status_filter))
    query = f"""
        SELECT days_to_delivery
        FROM main_gold.fct_orders
        WHERE days_to_delivery IS NOT NULL
          AND order_status IN ({placeholders})
    """
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            df = conn.execute(query, status_filter).df()
            return df
    except duckdb.Error:
        return pd.DataFrame(columns=["days_to_delivery"])

def get_filtered_raw_data(status_filter: list) -> pd.DataFrame:
    """Fetches only the raw data needed based on user filters."""
    if not status_filter:
        return pd.DataFrame()
        
    placeholders = ", ".join(["?"] * len(status_filter))
    query = f"""
        SELECT 
            order_id AS ORDER_ID,
            order_status AS ORDER_STATUS,
            purchased_at AS PURCHASED_AT,
            delivered_at AS DELIVERED_AT,
            total_items_in_order AS TOTAL_ITEMS_IN_ORDER,
            calculated_order_cost AS CALCULATED_ORDER_COST,
            days_to_delivery AS DAYS_TO_DELIVERY
        FROM main_gold.fct_orders
        WHERE purchased_at IS NOT NULL 
          AND order_status IN ({placeholders})
        ORDER BY purchased_at DESC
        LIMIT 1000
    """
    try:
        with duckdb.connect(DB_PATH, read_only=True) as conn:
            df = conn.execute(query, status_filter).df()
            if not df.empty:
                df["PURCHASED_AT"] = pd.to_datetime(df["PURCHASED_AT"])
            return df
    except duckdb.Error as e:
        st.error(f"🚨 Fatal Error: Unable to connect to analytical backend. Details: {e}")
        return pd.DataFrame()


def render_kpi_metrics(kpis: dict):
    """Renders top-level E-commerce KPIs."""
    cols = st.columns(4)
    cols[0].metric("Total Revenue", f"${kpis['total_revenue']:,.2f}")
    cols[1].metric("Total Orders", f"{kpis['total_orders']:,}")
    cols[2].metric("Avg Days to Delivery", f"{kpis['avg_delivery']:.1f} Days")
    cols[3].metric("Avg Basket Size", f"{kpis['avg_basket']:.1f} Items")


def main():
    st.title("📦 Olist Logistics & Revenue Intelligence")
    st.markdown("Automated tracking of order volume, revenue, and delivery SLAs.")
    
    # Sidebar Filters
    st.sidebar.header("⚙️ Global Filters")
    
    available_statuses = get_available_statuses()
    default_status = ["delivered"] if "delivered" in available_statuses else available_statuses
    
    status_filter = st.sidebar.multiselect(
        "Order Status",
        options=available_statuses,
        default=default_status
    )
    
    if not status_filter:
        st.warning("⚠️ Please select at least one order status to view data.")
        st.stop()
        
    # 1. Fetch lightweight aggregated KPIs
    kpis = get_kpi_metrics(status_filter)
    render_kpi_metrics(kpis)
    st.divider()

    tab_trends, tab_logistics, tab_raw = st.tabs(["📈 Revenue Trends", "🚚 Logistics SLAs", "🗄️ Raw Gold Data"])

    with tab_trends:
        st.subheader("Monthly Revenue")
        
        # 2. Fetch lightweight aggregated trend data
        monthly_rev = get_monthly_revenue_trends(status_filter)
        
        if not monthly_rev.empty:
            line_chart = alt.Chart(monthly_rev).mark_area(
                line={'color':'#2ca02c'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#2ca02c', offset=0), alt.GradientStop(color='transparent', offset=1)],
                    x1=1, x2=1, y1=1, y2=0
                ),
                opacity=0.6
            ).encode(
                x=alt.X("YearMonth:T", title="Date"),
                y=alt.Y("revenue:Q", title="Revenue ($)"),
                tooltip=[
                    alt.Tooltip("YearMonth:T", title="Month", format="%B %Y"), 
                    alt.Tooltip("revenue:Q", title="Revenue", format="$,.2f")
                ]
            ).properties(height=400)
            
            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.info("No revenue data to display for the selected filters.")

    with tab_logistics:
        st.subheader("Delivery Time Distribution")
        
        # Fetch just the delivery days column
        delivery_df = get_delivery_data(status_filter)
        
        if not delivery_df.empty:
            hist_chart = alt.Chart(delivery_df).mark_bar(color='#ff7f0e').encode(
                x=alt.X("days_to_delivery:Q", bin=alt.Bin(maxbins=30), title="Days to Delivery"),
                y=alt.Y("count():Q", title="Number of Orders"),
                tooltip=["count()"]
            ).properties(height=400)
            
            st.altair_chart(hist_chart, use_container_width=True)
        else:
            st.info("No delivery data to display for the selected filters.")

    with tab_raw:
        st.subheader("Gold Layer Fact Table")
        
        # Fetch limited raw data
        raw_df = get_filtered_raw_data(status_filter)
        if not raw_df.empty:
            st.dataframe(raw_df, use_container_width=True, hide_index=True)
        else:
            st.info("No raw data to display.")

if __name__ == "__main__":
    main()
