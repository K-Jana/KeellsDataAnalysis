import pandas as pd

df1 = pd.read_csv('cargills_outlets.csv')
df2 = pd.read_csv('cargills_stores.csv')

# 'place_id' is a common column for comparison
merged_df = pd.merge(df1, df2, on='place_id', how='outer', indicator=True)
for col in df1.columns:
    if col != "place_id" and col in df2.columns:  # only for overlapping cols
        merged_df[col] = merged_df[f"{col}_x"].combine_first(merged_df[f"{col}_y"])
        merged_df.drop([f"{col}_x", f"{col}_y"], axis=1, inplace=True)

cleaned_df = merged_df[merged_df['name'].astype(str).str.strip().str.lower().str.startswith('cargills')]
cleaned_df.to_csv('cargills.csv', index=False)