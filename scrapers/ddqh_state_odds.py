from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

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
        url = "https://elections2024.thehill.com/forecast/2024/president/"
    else:
        url = f"https://elections2024.thehill.com/forecast/2024/president/{state}/"

    driver.get(url)

    try:
        if general:
            try:
                # Check for Kamala Harris
                kamala_element = driver.find_element(By.CSS_SELECTOR, 'span.font-semibold')
                kamala_name = kamala_element.text.strip()
                
                if kamala_name == "Kamala Harris":
                    # Kamala Harris is present, get the value from the specific <span> with background color
                    element = driver.find_element(By.CSS_SELECTOR, 'span.style*="background-color: rgb(58, 88, 135);"')
                    odds = element.text.replace('%', '').strip()
                else:
                    # Kamala Harris is not present, get the general value and compute 100 - value
                    element = driver.find_element(By.CSS_SELECTOR, 'span.data-v-c4d31cfa')
                    general_value = element.text.replace('%', '').strip()
                    odds = str(100 - float(general_value))
            except Exception as e:
                print(f"Error occurred while scraping general odds: {e}")
                odds = "N/A"
        else:
            element = driver.find_element(By.CSS_SELECTOR, 'td.text-dem-100')
        # Extract the value from the data-value attribute
            odds = element.text.replace('%', '').strip()
    except Exception as e:
        print(f"Error occurred while scraping {state}: {e}")
        odds = "N/A"
    
    # Close the browser after scraping
    driver.quit()

    return odds

# Prepare CSV output
output_file = 'pres24_ddhq_scrape_stateodds_output.csv'

# Write the header row
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['State', 'DDHQ'])  # Header for the CSV

    # Scrape each state for all models and write the odds to the CSV
    for state in states:
        odds = scrape_odds_for_state(state)
        writer.writerow([state.replace("-", " ").title(), odds])

    # Scrape general election odds (Electoral College)
    electoral_odds = scrape_odds_for_state("general", general=True)
    writer.writerow(["Electoral College", electoral_odds])

print(f"Scraping completed. Results saved to {output_file}.")
