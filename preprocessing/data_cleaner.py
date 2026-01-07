def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(df.median(numeric_only=True))
    return df
