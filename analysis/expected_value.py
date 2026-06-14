import pandas as pd

# Load the CSV files
master_odds = pd.read_csv('pres24_scrape_stateodds_output.csv')
silver_odds = pd.read_csv('/Users/RobertReedy/Downloads/silver_odds_final.csv')

silver_merge = pd.merge(
    master_odds,
    silver_odds,
    on='State',
    how='left'
)

exclude = ['Electoral College', 'Maine Cd 1', 'Maine Cd 2', 'Nebraska Cd 1', 'Nebraska Cd 2', 'Nebraska Cd 3', 'District Of Columbia']
exclude2 = ['Electoral College']
swing_states = ['Michigan', 'Pennsylvania', 'Wisconsin', 'Nevada', 'North Carolina', 'Georgia', 'Arizona']
silver_merge = silver_merge[~silver_merge['State'].isin(exclude2)]
silver_swing_states = silver_merge[silver_merge['State'].isin(swing_states)]

silver_swing_states['model_avg'] = silver_swing_states[['FTE', 'Standard', 'silver']].mean(axis=1)

print(silver_swing_states)

# Function to calculate adjusted odds
def calculate_odds(silver_merge):
    if silver_merge < 0.5:
        return 1 - silver_merge 
    else:
        return silver_merge

# Assuming the columns for each model are named like 'FTE', 'Standard', 'RWH', 'DDHQ'
model_columns = ['FTE', 'Standard', 'RWH', 'DDHQ', 'silver']

# Calculate and update the odds for each model
for column in model_columns:
    silver_merge[column] = silver_merge[column].apply(calculate_odds)

def to_percentage(value):
    return round(value * 100, 1)

print(f"FTE: {round(sum(silver_merge['FTE']), 1)} expected correct calls out of {silver_merge.shape[0]}, or {to_percentage(sum(silver_merge['FTE']) / silver_merge.shape[0])}%.")
print(f"JHK: {round(sum(silver_merge['Standard']), 1)} expected correct calls out of {silver_merge.shape[0]}, or {to_percentage(sum(silver_merge['Standard']) / silver_merge.shape[0])}%.")
print(f"DDHQ: {round(sum(silver_merge['DDHQ']), 1)} expected correct calls out of {silver_merge.shape[0]}, or {to_percentage(sum(silver_merge['DDHQ']) / silver_merge.shape[0])}%.")
print(f"RWH: {round(sum(silver_merge['RWH']), 1)} expected correct calls out of {silver_merge.shape[0]}, or {to_percentage(sum(silver_merge['RWH']) / silver_merge.shape[0])}%.")
print(f"Silver: {round(sum(silver_merge['silver']), 1)} expected correct calls out of {silver_merge.shape[0]}, or {to_percentage(sum(silver_merge['silver']) / silver_merge.shape[0])}%.")
