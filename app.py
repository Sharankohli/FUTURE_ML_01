import streamlit as st
import pandas as pd
import plotly.express as px

from st_aggrid import AgGrid, GridOptionsBuilder

from src.data_preprocessing import (
    preprocess_data,
    filter_data,
    aggregate_daily_sales
)
from src.feature_engineering import (
    add_time_features,
    add_lag_feature
)
from src.model import (
    train_forecasting_model,
    predict_future_sales
)

st.set_page_config(
    page_title="Sales & Demand Forecasting",
    layout="wide"
)

st.title("📊 Sales & Demand Forecasting Dashboard")

st.caption(
    "Business Objective: Predict short-term sales demand using historical data to support "
    "inventory planning, staffing decisions, and cash-flow management."
)

df = preprocess_data()


df = filter_data(df, store_id=1, family_name="GROCERY I")

daily_sales = aggregate_daily_sales(df)
daily_sales = add_time_features(daily_sales)
daily_sales = add_lag_feature(daily_sales)

st.sidebar.header("🔎 Filters")

min_date = daily_sales["date"].min()
max_date = daily_sales["date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_sales = daily_sales[
        (daily_sales["date"] >= start_date) &
        (daily_sales["date"] <= end_date)
    ]
else:
    filtered_sales = daily_sales.copy()

model, mae, predictions, actuals = train_forecasting_model(daily_sales)

last_date = daily_sales["date"].iloc[-1]
last_sales = daily_sales["sales"].iloc[-1]

future_df = predict_future_sales(
    model=model,
    last_date=last_date,
    last_sales=last_sales,
    days=15
)

avg_forecast = future_df["predicted_sales"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Mean Absolute Error (Units)", f"{mae:.0f}")
k2.metric("Avg Forecast (Next 15 Days)", f"{avg_forecast:.0f}")
k3.metric("Total Historical Days", filtered_sales.shape[0])
k4.metric("Latest Actual Sales", f"{last_sales:.0f}")

c1, c2 = st.columns(2)

with c1:
    tmp = filtered_sales.copy()
    tmp["Day Type"] = tmp["day_of_week"].apply(
        lambda x: "Weekend" if x >= 5 else "Weekday"
    )
    donut_df = tmp.groupby("Day Type", as_index=False)["sales"].sum()

    fig_donut = px.pie(
        donut_df,
        values="sales",
        names="Day Type",
        hole=0.6,
        title="Sales Contribution: Weekday vs Weekend"
    )
    fig_donut.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_donut, use_container_width=True)

with c2:
    fig_hist = px.line(
        filtered_sales,
        x="date",
        y="sales",
        title="Historical Daily Sales Trend"
    )
    fig_hist.update_layout(xaxis_title="Date", yaxis_title="Sales")
    st.plotly_chart(fig_hist, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    fig_forecast = px.line(
        future_df,
        x="date",
        y="predicted_sales",
        title="15-Day Sales Forecast",
        markers=True
    )
    fig_forecast.update_layout(
        xaxis_title="Date",
        yaxis_title="Predicted Sales"
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

with c4:
    top_days = filtered_sales.sort_values(
        "sales", ascending=False
    ).head(10)

    fig_top = px.bar(
        top_days,
        x="date",
        y="sales",
        title="Top 10 Highest-Sales Days",
        text_auto=True
    )
    fig_top.update_layout(xaxis_title="Date", yaxis_title="Sales")
    st.plotly_chart(fig_top, use_container_width=True)

st.subheader("📋 15-Day Sales Forecast")

display_tbl = future_df[["date", "predicted_sales"]].copy()
display_tbl["date"] = display_tbl["date"].dt.strftime("%Y-%m-%d")
display_tbl["Predicted Sales"] = display_tbl["predicted_sales"].round(0)
display_tbl = display_tbl[["date", "Predicted Sales"]]

gb = GridOptionsBuilder.from_dataframe(display_tbl)

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True
)

gb.configure_column(
    "Predicted Sales",
    type=["numericColumn"],
    valueFormatter="value.toLocaleString()",
    cellStyle={
        "fontWeight": "bold",
        "color": "#4C9AFF"
    }
)

gb.configure_column(
    "Predicted Sales",
    cellStyleJsCode="""
    function(params) {
        if (params.value > 3000) {
            return { 'color': 'white', 'backgroundColor': '#1F7A1F' };
        }
        if (params.value < 2200) {
            return { 'color': 'white', 'backgroundColor': '#7A1F1F' };
        }
        return null;
    }
    """
)

gb.configure_pagination(
    paginationAutoPageSize=False,
    paginationPageSize=7
)

gridOptions = gb.build()

AgGrid(
    display_tbl,
    gridOptions=gridOptions,
    theme="streamlit",
    fit_columns_on_grid_load=True,
    height=320
)

st.subheader("💡 Business Insights")

st.markdown(
    """
- Short-term demand is **stable** with **clear weekly seasonality**.
- **Weekdays generate higher sales** compared to weekends.
- The forecast enables the business to:
  - Optimize **inventory replenishment**
  - Adjust **staffing levels**
  - Reduce **overstocking and stock-out risks**
"""
)

st.success(
    "This dashboard can be used by store managers and business leaders "
    "to support short-term operational planning."
)
