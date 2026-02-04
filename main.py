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

df = preprocess_data()

df = filter_data(df, store_id=1, family_name="GROCERY I")

daily_sales = aggregate_daily_sales(df)

daily_sales = add_time_features(daily_sales)
daily_sales = add_lag_feature(daily_sales)

model, mae, predictions, actuals = train_forecasting_model(daily_sales)

print(f"Mean Absolute Error (MAE): {mae:.2f}")

last_date = daily_sales['date'].iloc[-1]
last_sales = daily_sales['sales'].iloc[-1]

future_df = predict_future_sales(
    model=model,
    last_date=last_date,
    last_sales=last_sales,
    days=15
)

print("\nFuture Sales Forecast (Next 15 Days):")
print(future_df)

daily_sales.to_csv("historical_sales.csv", index=False)
future_df.to_csv("future_sales_forecast.csv", index=False)

print("\nCSV files created for Power BI:")
print("✔ historical_sales.csv")
print("✔ future_sales_forecast.csv")
