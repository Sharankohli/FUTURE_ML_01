import pandas as pd

def preprocess_data():
    df = pd.read_csv("data/train.csv")

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    return df


def filter_data(df, store_id=1, family_name="GROCERY I"):
    df = df[
        (df['store_nbr'] == store_id) &
        (df['family'] == family_name)
    ]
    return df


def aggregate_daily_sales(df):
    daily_df = (
        df.groupby('date', as_index=False)['sales']
        .sum()
    )
    return daily_df
