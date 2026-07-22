
import sys
from pathlib import Path
from typing import Optional

# Add project root to sys.path to import src module
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.infrastructure.analytics_service import DuckDBAnalyticsService

st.set_page_config(
    page_title="Claude Code Usage Analytics",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Claude Code Usage Analytics Dashboard")


def main() -> None:
    analytics = DuckDBAnalyticsService()

    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Overview", "Cost & Models", "Tools", "Caching"]
    )

    daily_metrics: pd.DataFrame = analytics.get_daily_metrics()
    event_dist: pd.DataFrame = analytics.get_event_distribution()
    practice_dist: pd.DataFrame = analytics.get_user_role_distribution()

    if page == "Overview":
        display_overview(daily_metrics, event_dist, practice_dist, analytics)
    elif page == "Cost & Models":
        display_cost_models(analytics)
    elif page == "Tools":
        display_tools(analytics)
    elif page == "Caching":
        display_caching(analytics)


def display_overview(
    daily_metrics: pd.DataFrame,
    event_dist: pd.DataFrame,
    practice_dist: pd.DataFrame,
    analytics: DuckDBAnalyticsService
) -> None:
    st.header("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)
    total_users: int = practice_dist["users"].sum() if not practice_dist.empty else 0
    total_sessions: int = daily_metrics["sessions"].sum() if not daily_metrics.empty else 0
    total_events: int = daily_metrics["total_events"].sum() if not daily_metrics.empty else 0
    total_cost: float = round(daily_metrics["total_cost_usd"].sum(), 2) if not daily_metrics.empty else 0.0

    with col1:
        st.metric("Total Users", f"{total_users}")
    with col2:
        st.metric("Total Sessions", f"{total_sessions}")
    with col3:
        st.metric("Total Events", f"{total_events}")
    with col4:
        st.metric("Total Cost (USD)", f"${total_cost}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Events Over Time")
        if not daily_metrics.empty:
            fig = px.line(
                daily_metrics,
                x="date",
                y=["total_events", "active_users"],
                title="Daily Events & Active Users"
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Cost Over Time")
        if not daily_metrics.empty:
            fig = px.line(
                daily_metrics,
                x="date",
                y="total_cost_usd",
                title="Daily Cost (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Event Types")
        if not event_dist.empty:
            fig = px.pie(
                event_dist,
                values="count",
                names="event_type",
                title="Distribution of Events"
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Users by Practice")
        if not practice_dist.empty:
            fig = px.bar(
                practice_dist,
                x="practice",
                y="users",
                title="Engineering Practices",
                color="practice"
            )
            st.plotly_chart(fig, use_container_width=True)


def display_cost_models(analytics: DuckDBAnalyticsService) -> None:
    st.header("💰 Cost & Model Usage")

    model_usage: pd.DataFrame = analytics.get_model_usage()
    cost_by_practice: pd.DataFrame = analytics.get_cost_by_practice()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Model Usage")
        if not model_usage.empty:
            fig = px.bar(
                model_usage,
                x="model",
                y="total_cost",
                title="Cost by Model",
                color="model"
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Cost by Practice")
        if not cost_by_practice.empty:
            fig = px.bar(
                cost_by_practice,
                x="practice",
                y="total_cost",
                title="Cost by Engineering Practice",
                color="practice"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Model Statistics")
    if not model_usage.empty:
        st.dataframe(model_usage, use_container_width=True)


def display_tools(analytics: DuckDBAnalyticsService) -> None:
    st.header("🛠️ Tool Usage")
    tool_usage: pd.DataFrame = analytics.get_tool_usage()

    if not tool_usage.empty:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                tool_usage,
                x="tool_name",
                y="count",
                title="Tool Usage Count",
                color="tool_name"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            tool_usage_pd: pd.DataFrame = tool_usage.copy()
            tool_usage_pd["success_rate"] = tool_usage_pd["success_count"] / tool_usage_pd["count"] * 100
            fig = px.bar(
                tool_usage_pd,
                x="tool_name",
                y="success_rate",
                title="Tool Success Rate (%)",
                color="tool_name"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Tool Details")
        st.dataframe(tool_usage_pd, use_container_width=True)


def display_caching(analytics: DuckDBAnalyticsService) -> None:
    st.header("💾 Cache Usage & Efficiency")
    
    # Get all cache analytics data
    cache_stats: pd.DataFrame = analytics.get_cache_usage()
    cache_efficiency: pd.DataFrame = analytics.get_cache_efficiency()
    top_cache_users: pd.DataFrame = analytics.get_top_cache_users()
    cache_by_model: pd.DataFrame = analytics.get_cache_by_model()
    daily_cache: pd.DataFrame = analytics.get_daily_cache_metrics()

    if not cache_stats.empty and not cache_efficiency.empty:
        cache_pd: pd.Series = cache_stats.iloc[0]
        efficiency_pd: pd.Series = cache_efficiency.iloc[0]

        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cache Read", f"{int(cache_pd['total_cache_read']):,}")
        with col2:
            st.metric("Total Cache Create", f"{int(cache_pd['total_cache_create']):,}")
        with col3:
            st.metric("Read/Create Ratio", f"{efficiency_pd['cache_read_to_create_ratio']:.2f}x")
        with col4:
            st.metric("Cache Hit Rate", f"{(efficiency_pd['requests_with_cache_read'] / efficiency_pd['total_api_requests'] * 100):.1f}%")
        
        st.divider()
        
        # Cache trends over time
        if not daily_cache.empty:
            st.subheader("📈 Daily Cache Trends")
            daily_cache_pd: pd.DataFrame = daily_cache
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.line(
                    daily_cache_pd,
                    x="date",
                    y=["total_cache_read", "total_cache_create"],
                    title="Daily Cache Read vs Create (tokens)",
                    labels={"value": "Tokens", "variable": "Type"}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(
                    daily_cache_pd,
                    x="date",
                    y="daily_cache_efficiency",
                    title="Daily Cache Efficiency (Read/Create Ratio)",
                    labels={"daily_cache_efficiency": "Ratio"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Cache by model
        if not cache_by_model.empty:
            st.subheader("🤖 Cache Usage by Model")
            cache_by_model_pd: pd.DataFrame = cache_by_model
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    cache_by_model_pd,
                    x="model",
                    y=["total_cache_read", "total_cache_create"],
                    title="Total Cache Usage by Model",
                    labels={"value": "Tokens", "variable": "Type"},
                    barmode="group"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    cache_by_model_pd,
                    x="model",
                    y="cache_read_to_create_ratio",
                    title="Cache Efficiency Ratio by Model",
                    color="model"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(cache_by_model_pd, use_container_width=True)
        
        st.divider()
        
        # Top cache users
        if not top_cache_users.empty:
            st.subheader("👥 Top Cache Users")
            top_users_pd: pd.DataFrame = top_cache_users
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    top_users_pd,
                    x="user_email",
                    y="total_cache_usage",
                    title="Top Users by Total Cache Usage",
                    color="user_practice"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    top_users_pd,
                    x="user_email",
                    y="cache_efficiency_ratio",
                    title="Cache Efficiency Ratio by User",
                    color="user_practice"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(top_users_pd, use_container_width=True)
        
        st.divider()
        
        # Efficiency details
        st.subheader("⚡ Efficiency Overview")
        eff_col1, eff_col2, eff_col3 = st.columns(3)
        with eff_col1:
            st.metric("Total API Requests", f"{int(efficiency_pd['total_api_requests']):,}")
        with eff_col2:
            st.metric("Requests with Cache Read", f"{int(efficiency_pd['requests_with_cache_read']):,}")
        with eff_col3:
            st.metric("Requests with Cache Create", f"{int(efficiency_pd['requests_with_cache_create']):,}")


if __name__ == "__main__":
    main()
