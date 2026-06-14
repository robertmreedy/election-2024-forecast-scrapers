import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Set up Chrome options (headless mode to run in the background)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver with the options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the page
    url = "https://e.infogram.com/26e9d474-948d-4cd5-9184-1701e81e5b4c?src=embed"
    driver.get(url)
    
    # Wait for the page to fully load
    time.sleep(5)
    
    # Initialize a list to hold state odds data
    state_odds = []
    
    # Loop through states 10 to 60
    for state_num in range(1, 52):
        try:
            # Locate the specific element for each state
            state_odds_element = driver.find_element(By.XPATH, f'//*[@id="a766c15b-c363-48ef-ba5b-88827a720a219aa3743a-d920-4033-bf52-6e15b2d414d5"]/figure/div/div/div[1]/div[1]/div[4]/div[{state_num}]/span')
            # Extract the aria-label attribute
            aria_label = state_odds_element.get_attribute("aria-label")
            
            # Extract state name and Harris odds
            parts = aria_label.split('. ')
            state_name = parts[0].split(' - ')[0].replace("DC", "District Of Columbia")  # Convert "DC" to "District of Columbia"
            harris_odds = float(parts[2].split(': ')[1].replace('%', '').strip()) / 100  # Convert to decimal
            
            # Append the data to the list
            state_odds.append([state_name, harris_odds])

        except Exception as e:
            print(f"Error extracting data for state number {state_num}: {e}")
    
    # Locate and extract Electoral College odds
    try:
        harris_odds_element = driver.find_element(By.ID, '3213d20b-cbc9-4f23-9f25-64e63de29adb7d57799a-3ea4-4a5d-a314-63811cee8354')
        full_text = harris_odds_element.text
        lines = full_text.split('\n')

        harris_odds = None
        for i, line in enumerate(lines):
            if "Kamala Harris" in line:
                harris_odds_line = lines[i + 3]  # Odds line 3 below Kamala Harris text
                if "%" in harris_odds_line:
                    harris_odds = float(harris_odds_line.replace('% Chance', '').strip()) / 100
                    break
        
        if harris_odds is not None:
            # Append Electoral College odds to state_odds
            state_odds.append(["Electoral College", harris_odds])
        else:
            print("Kamala Harris odds not found")
    
    except Exception as e:
        print(f"Error extracting Electoral College odds: {e}")
    
    # Now, extract additional data for CD percentages
    # Navigate to the same page again
    driver.get(url)
    
    # Wait for the page to fully load
    time.sleep(5)
    
    # Locate the table body using the provided XPath
    table_body = driver.find_element(By.XPATH, '//*[@id="//*[@id="d9929162-fdce-42a9-a36b-357175499b7f6b289bd1-149c-4842-95a5-407dbf4ccbfe"]/figure/div/div/div/div/div/table/tbody')
    
    # Extract all rows from the table body
    rows = table_body.find_elements(By.TAG_NAME, "tr")
    
    # Loop through each row and extract data from relevant columns
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        
        if columns:
            # Get the first and third columns (name and percentage)
            state_name = columns[0].text.strip()
            percentage_info = columns[2].text.strip()
            
            # Only process rows containing "CD-" in the first column
            if "CD-" in state_name:
                # Format the state name: "Nebraska CD-2" to "Nebraska Cd 2"
                state_name = state_name.replace("CD-", "Cd ").replace("Neb.", "Nebraska")
                
                # Extract the percentage value and candidate (e.g., "83% for Trump")
                percentage_value = percentage_info.split('%')[0].strip()  # Extract "83"
                candidate = percentage_info.split('for ')[1].strip()  # Extract "Trump" or "Harris"

                # Handle special case where the value is "99%+"
                if "+" in percentage_value:
                    percentage_value = "100"
                
                # Convert the percentage to a decimal value
                decimal_value = float(percentage_value) / 100

                # If the candidate is Trump, adjust the value to 1 minus the decimal value
                if "Trump" in candidate:
                    decimal_value = 1 - decimal_value

                # Append the result (formatted state name and decimal value) to the state_odds list
                state_odds.append([state_name, decimal_value])

    # Write the output to a CSV file
    output_filename = 'pres24_rwh_scrape_stateodds_output.csv'
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["State", "RWH"])
        # Write the state odds data including Electoral College odds and CD percentages
        writer.writerows(state_odds)

    print(f"Data written to {output_filename}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()
