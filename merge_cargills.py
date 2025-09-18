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

# Read the files
df_keells = pd.read_csv('keells_stores.csv')
df_ratings = pd.read_csv('ratings.csv')
df_cargills = pd.read_csv('cargills.csv')

df_keells = df_keells.rename(columns={'latitude': 'lat', 'longitude': 'lng'})
df_ratings = df_ratings.rename(columns={'avg_rating': 'rating'})
df_cargills=df_cargills.rename(columns={'user_ratings':'rating'})


keells_merged = pd.merge(df_keells, df_ratings[['place_id', 'num_ratings','rating']], on='place_id', how='left')

# Select columns and ensure order
cols = ['place_id', 'address', 'lat', 'lng', 'num_ratings','rating']
keells_selected = keells_merged[cols]
cargills_selected = df_cargills[cols]

# Combine all rows
combined = pd.concat([keells_selected, cargills_selected], ignore_index=True)

# Save to a new CSV
combined.to_csv('combined_places.csv', index=False)