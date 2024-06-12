from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import json
import time
import re


# configuring the chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

# Read the json file
with open("flights.json", "r") as file:
    data = json.load(file)

keys = list(data.keys())

for i in range(len(keys)):
    flights_for_trip = []
    print(f"Getting flights for {keys[i]}")
    for j in tqdm(range(len(data[keys[i]]["URLS"])), desc="Progress", unit="URL"):
        driver.get(data[keys[i]]["URLS"][j])

        trip_info = {
            "dates": "",
            "prices": [],
            "Best Price": "",
        }

        time.sleep(5)

        dates = driver.find_elements(By.CLASS_NAME, "ZmKdL")
        for date in dates:
            if date.text:
                trip_info["dates"] = date.text.replace("\u2009", " ").replace(
                    "\u2013", "-"
                )

        elements = driver.find_elements(By.CLASS_NAME, "Rk10dc")
        elements = [element for element in elements if element.text]

        pattern = re.compile(r"\$\d+\,\d+", re.MULTILINE)
        prices_str = []
        for element in elements:
            prices_str += re.findall(pattern, element.text)

        sorted_prices_str = sorted(prices_str)
        sorted_prices_ints = [
            int(price.replace("$", "").replace(",", "")) for price in sorted_prices_str
        ]

        trip_info["prices"] = sorted_prices_str
        trip_info["Best Price"] = sorted_prices_str[0]

        flights_for_trip.append(trip_info)

    data[keys[i]]["Flights"] = flights_for_trip

# Write the json file
with open("flights.json", "w") as file:
    json.dump(data, file, indent=4)


driver.quit()
