from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# List of states
states = [ "alabama", "alaska", "arizona", "arkansas", "california", "colorado", 
    "connecticut", "delaware", "district-of-columbia", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky",
    "louisiana", "maine", "maine-1", "maine-2", "maryland", "massachusetts",
    "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska",
    "nebraska-1", "nebraska-2", "nebraska-3", "nevada", "new-hampshire",
    "new-jersey", "new-mexico", "new-york", "north-carolina", "north-dakota",
    "ohio", "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington",
    "west-virginia", "wisconsin", "wyoming" ]

# Function to scrape odds for a specific state or general election
def scrape_odds_for_state(state, general=False):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver with the options
    driver = webdriver.Chrome(options=chrome_options)

    if general:
        url = "https://projects.fivethirtyeight.com/2024-election-forecast/"
    else:
        url = f"https://projects.fivethirtyeight.com/2024-election-forecast/{state}/"

    driver.get(url)

    try:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(3)
    
    # Locate the element with the class "number" and extract its text
        element_text = driver.find_element(By.CSS_SELECTOR, 'div.dem.row div.number').text
        element_number = int(element_text.replace(',', ''))  # Remove commas if present
        element_divided = element_number / 1000
        print(f"{state} - {element_divided}")

    # If you need to extract data-value attribute
        odds = element_divided
    except Exception as e:
        print(f"Error occurred while scraping {state}: {e}")
        odds = "N/A"

    
    # Close the browser after scraping
    driver.quit()

    return odds

# Prepare CSV output
output_file = 'pres24_538_scrape_stateodds_output.csv'

# Write the header row
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'FTE'])  # Header for the CSV

    # Scrape each state for all models and write the odds to the CSV
    for state in states:
        odds = scrape_odds_for_state(state)
        writer.writerow([state.replace("-", " ").title(), odds])

    # Scrape general election odds (Electoral College)
    electoral_odds = scrape_odds_for_state("general", general=True)
    writer.writerow(["Electoral College", electoral_odds])

print(f"Scraping completed. Results saved to {output_file}.")
