
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.infrastructure.analytics_service import DuckDBAnalyticsService

st.set_page_config(
    page_title="Claude Code Usage Analytics",
    page_icon="🤖",
    layout="centered"  # Changed to centered for better mobile experience
)

# Custom CSS for better mobile experience
st.markdown("""
    <style>
        /* General mobile optimizations */
        @media (max-width: 640px) {
            .stApp {
                padding: 0.5rem !important;
            }
            .stTitle {
                font-size: 1.5rem !important;
                margin-bottom: 1rem !important;
            }
            .stHeader {
                font-size: 1.2rem !important;
                margin-top: 1rem !important;
                margin-bottom: 0.5rem !important;
            }
            .stSubheader {
                font-size: 1rem !important;
                margin-top: 0.8rem !important;
                margin-bottom: 0.3rem !important;
            }
            .stMetric {
                padding: 0.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            .stPlotlyChart {
                margin-bottom: 0.8rem !important;
            }
            .stDataFrame {
                margin-top: 0.5rem !important;
                margin-bottom: 1rem !important;
            }
            div[data-testid="stVerticalBlock"] > div {
                margin-bottom: 0.5rem !important;
            }
        }
        
        /* Better spacing for all devices */
        .main > div {
            padding-top: 1rem !important;
        }
        .stDivider {
            margin: 1.5rem 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Claude Code Usage Analytics Dashboard")


def main():
    analytics = DuckDBAnalyticsService()

    st.sidebar.header("📱 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Overview", "Cost & Models", "Tools", "Caching"]
    )

    daily_metrics = analytics.get_daily_metrics()
    event_dist = analytics.get_event_distribution()
    practice_dist = analytics.get_user_role_distribution()

    if page == "Overview":
        display_overview(daily_metrics, event_dist, practice_dist, analytics)
    elif page == "Cost & Models":
        display_cost_models(analytics)
    elif page == "Tools":
        display_tools(analytics)
    elif page == "Caching":
        display_caching(analytics)


def display_overview(daily_metrics, event_dist, practice_dist, analytics):
    st.header("📊 Overview")

    # Responsive metric columns
    total_users = practice_dist["users"].sum() if not practice_dist.empty else 0
    total_sessions = daily_metrics["sessions"].sum() if not daily_metrics.empty else 0
    total_events = daily_metrics["total_events"].sum() if not daily_metrics.empty else 0
    total_cost = round(daily_metrics["total_cost_usd"].sum(), 2) if not daily_metrics.empty else 0.0

    # For mobile: 2 columns, for desktop: 4 columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Total Users", f"{total_users}")
        st.metric("📈 Total Events", f"{total_events}")
    with col2:
        st.metric("💻 Total Sessions", f"{total_sessions}")
        st.metric("💰 Total Cost", f"${total_cost}")

    st.divider()

    # Charts
    st.subheader("📈 Events & Activity")
    if not daily_metrics.empty:
        fig = px.line(
            daily_metrics,
            x="date",
            y=["total_events", "active_users"],
            title="Daily Events & Active Users",
            labels={"variable": "Metric", "value": "Count"}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("💵 Cost Trend")
    if not daily_metrics.empty:
        fig = px.line(
            daily_metrics,
            x="date",
            y="total_cost_usd",
            title="Daily Cost (USD)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📊 Distribution")
    col1, col2 = st.columns(2)
    with col1:
        if not event_dist.empty:
            fig = px.pie(
                event_dist,
                values="count",
                names="event_type",
                title="Event Types"
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        if not practice_dist.empty:
            fig = px.bar(
                practice_dist,
                x="practice",
                y="users",
                title="Users by Practice",
                color="practice"
            )
            st.plotly_chart(fig, use_container_width=True)


def display_cost_models(analytics):
    st.header("💰 Cost & Model Usage")

    model_usage = analytics.get_model_usage()
    cost_by_practice = analytics.get_cost_by_practice()

    st.subheader("🤖 Model Cost")
    if not model_usage.empty:
        fig = px.bar(
            model_usage,
            x="model",
            y="total_cost",
            title="Cost by Model",
            color="model"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏢 Cost by Practice")
    if not cost_by_practice.empty:
        fig = px.bar(
            cost_by_practice,
            x="practice",
            y="total_cost",
            title="Cost by Engineering Practice",
            color="practice"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("📋 Model Statistics")
    if not model_usage.empty:
        st.dataframe(model_usage, use_container_width=True)


def display_tools(analytics):
    st.header("🛠️ Tool Usage")
    tool_usage = analytics.get_tool_usage()

    if not tool_usage.empty:
        tool_usage_pd = tool_usage.copy()
        tool_usage_pd["success_rate"] = tool_usage_pd["success_count"] / tool_usage_pd["count"] * 100

        st.subheader("📊 Usage Count")
        fig = px.bar(
            tool_usage,
            x="tool_name",
            y="count",
            title="Tool Usage",
            color="tool_name"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("✅ Success Rate")
        fig = px.bar(
            tool_usage_pd,
            x="tool_name",
            y="success_rate",
            title="Tool Success Rate (%)",
            color="tool_name"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("📋 Tool Details")
        st.dataframe(tool_usage_pd, use_container_width=True)


def display_caching(analytics):
    st.header("💾 Cache Usage & Efficiency")
    
    # Get all cache analytics data
    cache_stats = analytics.get_cache_usage()
    cache_efficiency = analytics.get_cache_efficiency()
    top_cache_users = analytics.get_top_cache_users()
    cache_by_model = analytics.get_cache_by_model()
    daily_cache = analytics.get_daily_cache_metrics()

    if not cache_stats.empty and not cache_efficiency.empty:
        cache_pd = cache_stats.iloc[0]
        efficiency_pd = cache_efficiency.iloc[0]

        # Top metrics - responsive
        st.subheader("🔢 Key Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Cache Read", f"{int(cache_pd['total_cache_read']):,}")
            st.metric("Read/Create Ratio", f"{efficiency_pd['cache_read_to_create_ratio']:.2f}x")
        with col2:
            st.metric("Total Cache Create", f"{int(cache_pd['total_cache_create']):,}")
            st.metric("Cache Hit Rate", f"{(efficiency_pd['requests_with_cache_read'] / efficiency_pd['total_api_requests'] * 100):.1f}%")
        
        st.divider()
        
        # Cache trends over time
        if not daily_cache.empty:
            st.subheader("📈 Daily Trends")
            
            fig1 = px.line(
                daily_cache,
                x="date",
                y=["total_cache_read", "total_cache_create"],
                title="Daily Cache Read vs Create (tokens)",
                labels={"value": "Tokens", "variable": "Type"}
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.line(
                daily_cache,
                x="date",
                y="daily_cache_efficiency",
                title="Daily Cache Efficiency (Ratio)",
                labels={"daily_cache_efficiency": "Ratio"}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Cache by model
        if not cache_by_model.empty:
            st.subheader("🤖 Model Cache Usage")
            
            fig1 = px.bar(
                cache_by_model,
                x="model",
                y=["total_cache_read", "total_cache_create"],
                title="Cache Usage by Model",
                labels={"value": "Tokens", "variable": "Type"},
                barmode="group"
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.bar(
                cache_by_model,
                x="model",
                y="cache_read_to_create_ratio",
                title="Cache Efficiency by Model",
                color="model"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            st.dataframe(cache_by_model, use_container_width=True)
        
        st.divider()
        
        # Top cache users
        if not top_cache_users.empty:
            st.subheader("👥 Top Users")
            
            fig1 = px.bar(
                top_cache_users,
                x="user_email",
                y="total_cache_usage",
                title="Top Users by Total Cache Usage",
                color="user_practice"
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.bar(
                top_cache_users,
                x="user_email",
                y="cache_efficiency_ratio",
                title="Cache Efficiency by User",
                color="user_practice"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            st.dataframe(top_cache_users, use_container_width=True)
        
        st.divider()
        
        # Efficiency details
        st.subheader("⚡ Overview")
        eff_col1, eff_col2, eff_col3 = st.columns(3)
        with eff_col1:
            st.metric("Total Requests", f"{int(efficiency_pd['total_api_requests']):,}")
        with eff_col2:
            st.metric("With Cache Read", f"{int(efficiency_pd['requests_with_cache_read']):,}")
        with eff_col3:
            st.metric("With Cache Create", f"{int(efficiency_pd['requests_with_cache_create']):,}")


if __name__ == "__main__":
    main()
