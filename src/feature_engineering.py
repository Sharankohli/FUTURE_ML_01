def add_time_features(df):
    """
    Extract time-based features from date column
    """
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    return df


def add_lag_feature(df):
    """
    Add previous day's sales as a feature
    """
    df['sales_lag_1'] = df['sales'].shift(1)

    df = df.dropna().reset_index(drop=True)
    return df
