from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

# List of states
states = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", 
    "connecticut", "delaware", "district-of-columbia", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
    "louisiana", "maine", "maine-cd-1", "maine-cd-2", "maryland", "massachusetts",
    "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska",
    "nebraska-cd-1", "nebraska-cd-2", "nebraska-cd-3", "nevada", "new-hampshire",
    "new-jersey", "new-mexico", "new-york", "north-carolina", "north-dakota",
    "ohio", "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington",
    "west-virginia", "wisconsin", "wyoming"
]

# Function to convert percentage string to decimal
def percentage_to_decimal(percentage_str):
    if percentage_str.endswith('%'):
        return float(percentage_str.strip('%')) / 100
    return percentage_str

# Function to scrape odds for a specific URL
def scrape_odds_for_model(state, general=False):
# def scrape_odds_for_model(state, model_suffix, general=False):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver with the options
    driver = webdriver.Chrome(options=chrome_options)

    if general:
        url = f"https://projects.jhkforecasts.com/2024/president/#standard"
        # url = f"https://projects.jhkforecasts.com/2024/president/#{model_suffix}"
    else:
        url = f"https://projects.jhkforecasts.com/2024/president/states/{state}#standard"
        # url = f"https://projects.jhkforecasts.com/2024/president/states/{state}#{model_suffix}"

    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)  # Adjust if needed based on your internet speed and page load time

    try:
        harris_odds = percentage_to_decimal(driver.find_element(By.ID, "dem-win-top").text)
    except:
        harris_odds = "N/A"

    # Close the browser after scraping
    driver.quit()

    return harris_odds

# Prepare CSV output
output_file = 'pres24_jhk_scrape_statesodds_output_v2.csv'

# Write the header row
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'Standard'])
    # writer.writerow(['State', 'Standard', 'Simple', 'Now_Cast', 'Plus'])

    # Scrape each state for all models and write the odds to the CSV
    for state in states:
        standard_odds = scrape_odds_for_model(state)
        # simple_odds = scrape_odds_for_model(state, "#simple")
        # nowcast_odds = scrape_odds_for_model(state, "#now-cast")
        # plus_odds = scrape_odds_for_model(state, "#plus")
        
        writer.writerow([state.replace("-", " ").title(), standard_odds])
        # writer.writerow([state.replace("-", " ").title(), standard_odds, simple_odds, nowcast_odds, plus_odds])

    # Scrape general election odds (Electoral College)
    electoral_standard = scrape_odds_for_model("general", general=True)
    # electoral_simple = scrape_odds_for_model("general", "#simple", general=True)
    # electoral_nowcast = scrape_odds_for_model("general", "#now-cast", general=True)
    # electoral_plus = scrape_odds_for_model("general", "#plus", general=True)

    writer.writerow(["Electoral College", electoral_standard])
    # writer.writerow(["Electoral College", electoral_standard, electoral_simple, electoral_nowcast, electoral_plus])

print(f"Scraping completed. Results saved to {output_file}.")
