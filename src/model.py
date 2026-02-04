import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def train_forecasting_model(df):
    """
    Train a time-series forecasting model using Linear Regression
    """

    X = df[['year', 'month', 'day', 'day_of_week', 'sales_lag_1']]
    y = df['sales']

    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    return model, mae, predictions, y_test


def predict_future_sales(model, last_date, last_sales, days=15):
    """
    Predict future sales for next N days
    """

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=days
    )

    future_df = pd.DataFrame({'date': future_dates})

    future_df['year'] = future_df['date'].dt.year
    future_df['month'] = future_df['date'].dt.month
    future_df['day'] = future_df['date'].dt.day
    future_df['day_of_week'] = future_df['date'].dt.dayofweek

    future_df['sales_lag_1'] = last_sales

    future_df['predicted_sales'] = model.predict(
        future_df[['year', 'month', 'day', 'day_of_week', 'sales_lag_1']]
    )

    return future_df
