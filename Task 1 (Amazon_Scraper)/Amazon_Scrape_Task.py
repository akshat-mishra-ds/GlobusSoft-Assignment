import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Amazon search URL
url = "https://www.amazon.in/s?k=laptop"

# Headers to mimic a browser
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
}

# Send request
response = requests.get(url, headers=headers)

# Parse HTML
soup = BeautifulSoup(response.content, "html.parser")

products = []

# Find product containers
results = soup.find_all("div", {"data-component-type": "s-search-result"})

for item in results:

    # Title
    title_tag = item.find("h2")
    title = title_tag.get_text(strip=True) if title_tag else "N/A"

    # Image
    image_tag = item.find("img", class_="s-image")
    image = image_tag["src"] if image_tag else "N/A"

    # Rating
    rating_tag = item.find("span", class_="a-icon-alt")
    rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

    # Price
    price_tag = item.find("span", class_="a-price-whole")
    price = price_tag.get_text(strip=True) if price_tag else "N/A"

    # Ad / Organic
    ad_text = item.get_text().lower()

    if "sponsored" in ad_text:
        result_type = "Ad"
    else:
        result_type = "Organic"

    products.append({
        "Title": title,
        "Image": image,
        "Rating": rating,
        "Price": price,
        "Result Type": result_type
    })

# Create DataFrame
df = pd.DataFrame(products)

# Timestamped filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"amazon_laptops_{timestamp}.csv"

# Save CSV
df.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"Data saved successfully to: {filename}")
print(f"Total products scraped: {len(df)}")