import pandas as pd

df_raw = pd.read_csv('data/zomato.csv')
df_clean = pd.read_csv('data/zomato_cleaned.csv')

print(f'Raw CSV rows: {len(df_raw)}')
print(f'Cleaned CSV rows: {len(df_clean)}')
print(f'Unique restaurants (raw): {df_raw["name"].nunique()}')
print(f'Unique restaurants (cleaned): {df_clean["name"].nunique()}')
