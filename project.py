import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Amazon search page
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sa"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll to load more products
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the browser
driver.quit()

# Extract product details
products = soup.find_all('div', {'data-component-type': 's-search-result'})

# Separate lists for each field
product_names = []
product_prices = []
product_ratings = []
product_sellers = []

for product in products:
    try:
        # Extract Product Name
        name = product.find('h2').text.strip()
    except:
        name = "N/A"
    product_names.append(name)

    try:
        # Extract Product Price
        price = product.find('span', {'class': 'a-price-whole'}).text.strip()
    except:
        price = "N/A"
    product_prices.append(price)

    try:
        # Extract Product Rating
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip()
    except:
        rating = "N/A"
    product_ratings.append(rating)

    try:
        # Extract Seller Name (Not always available)
        seller = product.find('span', {'class': 'a-size-small a-color-base'}).text.strip()
    except:
        seller = "N/A"
    product_sellers.append(seller)

# Create a DataFrame
df = pd.DataFrame({
    'Product Name': product_names,
    'Price': product_prices,
    'Rating': product_ratings,
    'Seller': product_sellers
})

# Save to CSV
csv_filename = "amazon_products.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8")

print(f"Data saved to {csv_filename}")
