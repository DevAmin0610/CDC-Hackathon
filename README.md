# CDC Hackathon

# What Gets You Relief?
### Predicting how companies handle debt collection complaints, 2021–2025

CDC Hackathon project by Ishi, Srinidhi, Roshan and Dev.

## Question

What predicts whether a debt collection complaint gets a **timely response**, or any **relief**, and how has that changed from 2021 to 2025?

We examine how outcomes vary by **company**, **debt type (sub-product)**, **issue** and **state**.

## Data

Debt collection complaints from the [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/), 2021–2025.

| Year | Complaints |
|------|-----------:|
| 2021 | 53,873 |
| 2022 | 45,230 |
| 2023 | 49,844 |
| 2024 | 68,206 |
| 2025 | 128,799 |

**Outcomes we measure**

- **Timely response:** whether the company answered within the CFPB's deadline (15 days after the CFPB sends the complaint, or 60 days for a final response if first marked "in progress"). Taken from the `Timely response?` column.
- **Relief:** from `Company response to consumer`:
  - *Closed with monetary relief:* the company paid the consumer or reduced what they owe.
  - *Closed with non-monetary relief:* the company fixed the issue without a payment.
  - *Closed with explanation:* the company investigated but gave no relief.

**Notes on the data**

- The 2025 data is split into three files (`debt-complaints-2025-1.csv` to `-3.csv`) to stay under GitHub's file size limit. `load_data.py` combines them and removes duplicate complaint IDs.
- The CFPB added **Rental debt** and **Telecommunications debt** as categories in August 2023. Before that, most of those complaints were filed as "Other debt."
- Complaints reflect who chose to file, not all consumers, and relief is labeled by the company itself.

## Repository structure

```
CDC-Hackathon/
├── CDC_Hackathon_Data/          # CSVs, one per year (2025 split into three parts)
├── notebooks/
│   └── ishi.ipynb               # Timely response analysis
├── load_data.py                 # Shared loading code used by every notebook
├── .gitignore
└── README.md
```

## Setup

```bash
git clone <repo-url>
cd CDC-Hackathon
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install pandas matplotlib scikit-learn ipykernel
```

In VS Code, open a notebook and choose `.venv` as the kernel.

## Loading the data

Every notebook starts with:

```python
import sys
sys.path.append("..")              # lets notebooks/ find load_data.py

from load_data import load_all
df = load_all()                    # all years stacked, with a `year` column
```

`load_all()` also adds a `late` column (1 = the company did not respond on time), so everyone uses the same target definition.

## Team roles

| Member | Focus |
|--------|-------|
| Dev | Top sub-products and complaint trends over time |
| Ishi | Timely response rates by company, sub-product and issue |
| Srinidhi | How the company affects the likelihood of relief, 2021–2025 |
| Roshan | How geography (state) affects response outcomes and timeliness |

## Ishi's Work: 

- **Late responses are rare overall:** 2–3% of debt complaints each year (3.1% in 2021, 2.7% in 2025).
- **They are concentrated in a few companies.** In 2025, six companies answered 22–100% of their complaints late, against an average of 2.7%.
- **The company matters most.** In 2025, late-response rates ranged from 0% to 100% across companies, but only about 2–4% across issues.
- **A prediction model confirms it.** A logistic regression using only the company predicts late responses far better (AUC ≈ 0.95 in 2025) than one using debt type, issue, state, submission method and tags combined (AUC ≈ 0.69). The result holds with the three credit bureaus removed.
- **Late responses come in episodes.** Some companies went from mostly late to on time within the same year, and others the reverse, so monthly monitoring would catch problems that yearly averages hide.


## Dev's Work:

Dev: 

I used Claude to help me combine the 2025 Customer Complaints dataset as it was initially over 100,000 rows and I split it into 3 parts by the months and then used Claude to combine it so I can use it locally. I used Claude to also help me combine some bar charts as I initially created individual ones from 2021-2025 and wanted a way to combine them into one. I ultimately made a line chart myself. 

# 4. I used Claude to help me create and split the standardized disparity ratio heat map into two separate heatmaps, one for the top 25 states and one for the bottom 25 states. 
# This was done to make the heatmaps more readable and to allow for better comparison between the two groups of states.


## Srinidhi's Work:
I used ChatGPT to help me analyze the data in a more efficient way and create a better understanding of the relief index, I also used it to help me make the data more readable and seperate based on the top ten companies.

## Roshan's Work
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



## Methods

- Rates are calculated only for groups with enough complaints (100+ for companies, debt types and issues; 300+ for states) to avoid misleading results from small samples.
- Models are logistic regressions with one-hot encoded categories, trained on 75% of each year's complaints and tested on the remaining 25%.
- We excluded `Company response to consumer` and `Company public response` as model features, because they are filled in after the outcome is known and would leak the answer.

## Context: why complaints jumped in 2025

Complaints about the three credit bureaus (Equifax, TransUnion, Experian) grew from about 6% of debt collection complaints in 2021 to 27% in 2025. The CFPB attributes much of its overall rise in complaints to credit repair organizations and AI-generated submissions; that explanation is disputed. More complaints does not necessarily mean more debt problems.

Sources:
- [CFPB: Correcting Flaws to Restore Integrity and Utility to the Consumer Complaint System](https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-is-correcting-flaws-to-restore-integrity-and-utility-to-the-consumer-complaint-system/)
- [Orrick: CFPB reports complaint volume doubled in 2025](https://infobytes.orrick.com/2026-04-10/cfpb-reports-complaint-volume-doubled-in-2025-citing-surge-in-credit-reporting-disputes/)

## Limitations

- Complaints are self-reported and don't represent all consumers.
- Relief labels are reported by the companies themselves.
- Debt categories changed in August 2023.
- Findings are associations, not causes.


