# CDC Hackathon

Roshan: 
Claude was my primary AI assistant used as supplimental advice and guidance in this project. Below I will outline the specific ways in which Claude was used to help me complete my portion of this project.

# 1. Filtering data frame to only include the 50 US states:
This is the block of code that I used to filter the data frame to only include the 50 US states. I used Claude to help me identify the correct list of US state abbreviations to use for filtering, and to give a concise summary output of the changes.
Code: 
# Standardize to just the 50 traditional US states (drop DC, PR, VI, GU, AA/AE/AP military codes,
# the "UNITED STATES MINOR OUTLYING ISLANDS", missing/None, etc.)
df_states = df[df['State'].isin(US_STATES)].copy()

n_dropped = len(df) - len(df_states)
print(f"Rows before filter: {len(df):,}")
print(f"Rows dropped (non 50-state): {n_dropped:,} ({n_dropped / len(df):.2%})")
print(f"Rows after filter: {len(df_states):,}")
print(f"Unique states remaining: {df_states['State'].nunique()} / 50")


# 2. In this cell, I used Claude to help explain a default color schema when a sub-product did not fit the 7 critical sub-products. Claude helped me understand that the default color schema was used to ensure that all sub-products were represented in the heatmap.
subproduct_color = dict(zip(COL_ORDER, CATEGORICAL + ['#c3c2b7']))  # 'Other' -> neutral gray
## I used Claude to help me understand and create this function:
top10_by_year = (
    year_state_counts
    .groupby('year', group_keys=False)
    .apply(lambda s: s.sort_values(ascending=False).head(10))
    .reset_index()
)

# 3. I used Claude to help me understand and create a group of bar charts for the top 10 states, and their number of complaints for each sub-product. 
pivot = (
        sub.groupby(['State', 'Sub-product_grouped']).size()
        .unstack(fill_value=0)
        .reindex(index=top_states, columns=COL_ORDER, fill_value=0)
    )

    pivot.plot(
        kind='barh', stacked=True, ax=ax, width=0.75,
        color=[subproduct_color[c] for c in pivot.columns],
        legend=False,

Dev: 

I used Claude to help me combine the 2025 Customer Complaints dataset as it was initially over 100,000 rows and I split it into 3 parts by the months and then used Claude to combine it so I can use it locally. I used Claude to also help me combine some bar charts as I initially created individual ones from 2021-2025 and wanted a way to combine them into one. I ultimately made a line chart myself. 
    )

# 4. I used Claude to help me create and split the standardized disparity ratio heat map into two separate heatmaps, one for the top 25 states and one for the bottom 25 states. 
# This was done to make the heatmaps more readable and to allow for better comparison between the two groups of states.
