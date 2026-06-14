import pandas as pd

# Load the CSV files
jhk_pres24 = pd.read_csv('pres24_jhk_scrape_statesodds_output.csv')
fte_538 = pd.read_csv('pres24_538_scrape_stateodds_output.csv')
ddhq = pd.read_csv('pres24_ddhq_scrape_stateodds_output.csv')
rwh = pd.read_csv('pres24_rwh_scrape_stateodds_output.csv')

# Rename state names in the FTE data
state_replacements = {
    'Maine 1': 'Maine Cd 1',
    'Maine 2': 'Maine Cd 2',
    'Nebraska 1': 'Nebraska Cd 1',
    'Nebraska 2': 'Nebraska Cd 2',
    'Nebraska 3': 'Nebraska Cd 3'
}

fte_538['State'] = fte_538['State'].replace(state_replacements)
ddhq['State'] = ddhq['State'].replace(state_replacements)

rwh['RWH'] = rwh['RWH'].round(4)

# Function to convert odds based on conditions
def convert_odds(value):
    # Ensure the value is treated as a string
    value_str = str(value)
    
    if value_str.startswith('>'):
        return 100  # Convert '>99%' to 100
    elif value_str.startswith('<'):
        return 0    # Convert '<1%' to 0
    else:
        # Remove % sign and convert to float
        return float(value_str.replace('%', ''))

# Apply the conversion function to the 'DDHQ' column
ddhq['DDHQ'] = ddhq['DDHQ'].apply(convert_odds)
ddhq['DDHQ'] = ddhq['DDHQ'].astype(float) * 0.01
ddhq['DDHQ'] = ddhq['DDHQ'].round(2)

# Merge the FTE and DDHQ datasets first
fte_ddhq_merged = fte_538[['State', 'FTE']].merge(ddhq[['State', 'DDHQ']], on='State', how='left')

# Now merge the rwh dataset with the merged FTE and DDHQ
merged_df = pd.merge(
    jhk_pres24,
    rwh,
    on='State',
    how='left'
).merge(
    fte_ddhq_merged,
    on='State',
    how='left'
)

# Define the FIPS codes and abbreviations for states
fips_codes = {
    'Alabama': '01', 'Alaska': '02', 'Arizona': '04', 'Arkansas': '05', 'California': '06',
    'Colorado': '08', 'Connecticut': '09', 'Delaware': '10', 'District Of Columbia': '11', 'Florida': '12', 'Georgia': '13',
    'Hawaii': '15', 'Idaho': '16', 'Illinois': '17', 'Indiana': '18', 'Iowa': '19',
    'Kansas': '20', 'Kentucky': '21', 'Louisiana': '22', 'Maine': '23', 'Maine Cd 1': '23',
    'Maine Cd 2': '23', 'Maryland': '24', 'Massachusetts': '25', 'Michigan': '26', 'Minnesota': '27',
    'Mississippi': '28', 'Missouri': '29', 'Montana': '30', 'Nebraska': '31', 'Nebraska Cd 1': '31',
    'Nebraska Cd 2': '31', 'Nebraska Cd 3': '31', 'Nevada': '32', 'New Hampshire': '33', 'New Jersey': '34',
    'New Mexico': '35', 'New York': '36', 'North Carolina': '37', 'North Dakota': '38', 'Ohio': '39',
    'Oklahoma': '40', 'Oregon': '41', 'Pennsylvania': '42', 'Rhode Island': '44', 'South Carolina': '45',
    'South Dakota': '46', 'Tennessee': '47', 'Texas': '48', 'Utah': '49', 'Vermont': '50',
    'Virginia': '51', 'Washington': '53', 'West Virginia': '54', 'Wisconsin': '55', 'Wyoming': '56'
}

state_abbr = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District Of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maine Cd 1': 'ME-1',
    'Maine Cd 2': 'ME-2', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nebraska Cd 1': 'NE-1',
    'Nebraska Cd 2': 'NE-2', 'Nebraska Cd 3': 'NE-3', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Add FIPS and state abbreviations as new columns
merged_df['FIPS'] = merged_df['State'].map(fips_codes)
merged_df['Abbreviation'] = merged_df['State'].map(state_abbr)

# Reorder columns so that 'FTE' comes right after 'State' and FIPS/Abbreviation at the end
column_order = ['State', 'FTE'] + [col for col in merged_df.columns if col not in ['State', 'FTE', 'FIPS', 'Abbreviation']] + ['FIPS', 'Abbreviation']
merged_df = merged_df[column_order]

# Save the combined data to a new CSV file
output_file = 'pres24_scrape_stateodds_output.csv'
merged_df.to_csv(output_file, index=False)

print(f"Combining completed. Results saved to {output_file}.")
