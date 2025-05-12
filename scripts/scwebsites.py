# Author: Shuriky (May 2025)
# This script extracts data from https://wiki.hypixel.net/Category:Sea_Creature,
# then print out the URLs of all sea creature pages.

import requests
from bs4 import BeautifulSoup

# URL of the category page
url = "https://wiki.hypixel.net/Category:Sea_Creature"

# Send a request to fetch the HTML content of the page
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links to sea creature pages
sea_creature_links = soup.select('.mw-category-group a')

# Store all websites inside an array
sea_creature_urls = [f"https://wiki.hypixel.net{link['href']}" for link in sea_creature_links]

# Print out the array of URLs
print(sea_creature_urls)
