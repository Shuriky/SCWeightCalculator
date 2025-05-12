# Author: Shuriky (May 2025)
# This script extracts data from the Hypixel Wiki for various sea creatures.
# It retrieves the name, weight, requirements, rarity, and environment of each creature,
# then saves the data to a JSON file named 'sea_creature_data.json'.

import requests
from bs4 import BeautifulSoup
import json

# List of sea creature URLs to scrape
urls = ['https://wiki.hypixel.net/Abyssal_Miner', 'https://wiki.hypixel.net/Agarimoo', 'https://wiki.hypixel.net/Alligator', 'https://wiki.hypixel.net/Banshee', 'https://wiki.hypixel.net/Bayou_Sludge', 'https://wiki.hypixel.net/Bloated_Mithril_Grubber', 'https://wiki.hypixel.net/Blue_Ringed_Octopus', 'https://wiki.hypixel.net/Blue_Shark', 'https://wiki.hypixel.net/Carrot_King', 'https://wiki.hypixel.net/Catfish', 'https://wiki.hypixel.net/Deep_Sea_Protector', 'https://wiki.hypixel.net/Dumpster_Diver', 'https://wiki.hypixel.net/Fiery_Scuttler', 'https://wiki.hypixel.net/Fire_Eel', 'https://wiki.hypixel.net/Fireproof_Witch', 'https://wiki.hypixel.net/Flaming_Worm', 'https://wiki.hypixel.net/Fried_Chicken', 'https://wiki.hypixel.net/Frog_Man', 'https://wiki.hypixel.net/Frosty_(Mob)', 'https://wiki.hypixel.net/Frozen_Steve', 'https://wiki.hypixel.net/Great_White_Shark', 'https://wiki.hypixel.net/Grim_Reaper', 'https://wiki.hypixel.net/Grinch', 'https://wiki.hypixel.net/Guardian_Defender', 'https://wiki.hypixel.net/Large_Mithril_Grubber', 'https://wiki.hypixel.net/Lava_Blaze', 'https://wiki.hypixel.net/Lava_Flame', 'https://wiki.hypixel.net/Lava_Leech', 'https://wiki.hypixel.net/Lava_Pigman', 'https://wiki.hypixel.net/Lord_Jawbus', 'https://wiki.hypixel.net/Magma_Slug', 'https://wiki.hypixel.net/Medium_Mithril_Grubber', 'https://wiki.hypixel.net/Mithril_Grubber', 'https://wiki.hypixel.net/Moogma', 'https://wiki.hypixel.net/Night_Squid', 'https://wiki.hypixel.net/Nightmare', 'https://wiki.hypixel.net/Nurse_Shark', 'https://wiki.hypixel.net/Nutcracker', 'https://wiki.hypixel.net/Oasis_Rabbit', 'https://wiki.hypixel.net/Oasis_Sheep', 'https://wiki.hypixel.net/Phantom_Fisher', 'https://wiki.hypixel.net/Plhlegblast', 'https://wiki.hypixel.net/Poisoned_Water_Worm', 'https://wiki.hypixel.net/Pyroclastic_Worm', 'https://wiki.hypixel.net/Ragnarok', 'https://wiki.hypixel.net/Reindrake', 'https://wiki.hypixel.net/Rider_Of_The_Deep', 'https://wiki.hypixel.net/Scarecrow', 'https://wiki.hypixel.net/Sea_Archer', 'https://wiki.hypixel.net/Sea_Creatures', 'https://wiki.hypixel.net/Sea_Emperor', 'https://wiki.hypixel.net/Sea_Guardian', 'https://wiki.hypixel.net/Sea_Leech', 'https://wiki.hypixel.net/Sea_Walker', 'https://wiki.hypixel.net/Sea_Witch', 'https://wiki.hypixel.net/Snapping_Turtle', 'https://wiki.hypixel.net/Squid', 'https://wiki.hypixel.net/Taurus', 'https://wiki.hypixel.net/Thunder', 'https://wiki.hypixel.net/Tiger_Shark', 'https://wiki.hypixel.net/Titanoboa', 'https://wiki.hypixel.net/Trash_Gobbler', 'https://wiki.hypixel.net/Water_Hydra', 'https://wiki.hypixel.net/Water_Worm', 'https://wiki.hypixel.net/Werewolf', 'https://wiki.hypixel.net/Wiki_Tiki', 'https://wiki.hypixel.net/Yeti']

# Function to get the sea creature's name
def get_name(soup):
    name = soup.find('h1', {'id': 'firstHeading'}).text.strip()
    return name

# Function to get the weight value
def get_weight_value(soup):
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1 and 'Weight' in cells[0].text:
            weight_value = cells[1].find('span', class_='color-aqua').text.strip()
            return weight_value
    return 'N/A'

# Function to get the requirements
def get_requirements(soup):
    requirements = {}
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1 and 'Requirements' in cells[0].text:
            requirements_text = cells[1].text.strip()
            requirements_parts = requirements_text.split('⏣')
            fishing_level = requirements_parts[0].strip()
            areas = [area.strip() for area in requirements_parts[1:]]
            requirements['level_required'] = fishing_level.split(' ')[-1]
            requirements['areas'] = areas
            if requirements['areas'] == []:
                requirements['areas'] = ["Any"]
            return requirements
    return 'N/A'

# Function to get the rarity
def get_rarity(soup):
    rarity_tag = soup.find('td', class_='attributes-minor')
    if rarity_tag:
        rarity = rarity_tag.find('b').text.strip()
        return rarity
    return 'N/A'

# Function to get the rod type
def get_rod_type(soup):
    rod_type_tag = soup.find('td', class_='attributes-minor')
    if rod_type_tag:
        rod_type = rod_type_tag.find_next_sibling('td').text.strip()
        if 'Rod Type' in rod_type:
            rod_type = rod_type.replace('Rod Type', '').strip()
        return rod_type
    return 'N/A'

# Function to get the image link
def get_image_link(soup):
    img_tag = soup.find('img', alt=True)
    if img_tag:
        img_link = img_tag['src']
        return f"https://wiki.hypixel.net{img_link}"
    return 'N/A'


# Main script
all_data = []

# Load existing data from the JSON file if it exists
try:
    with open('sea_creature_data.json', 'r') as f:
        existing_data = json.load(f)
        if isinstance(existing_data, list):
            all_data = existing_data
        else:
            all_data = [existing_data]
except (FileNotFoundError, json.JSONDecodeError):
    all_data = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    name = get_name(soup)
    weight_value = get_weight_value(soup)
    requirements = get_requirements(soup)
    rarity = get_rarity(soup)
    rod_type = get_rod_type(soup)
    image_link = get_image_link(soup)
    
    data = {
        'name': name,
        'weight': weight_value,
        'requirements': requirements,
        'rarity': rarity,
        'environment': rod_type,
        'image_link': image_link
    }
    
    # Print the data for each sea creature (for debugging)
    print(f"The name is: {name}")
    print(f"The weight value is: {weight_value}")
    print(f"The requirements are: {requirements}")
    print(f"The rarity is: {rarity}")
    print(f"Environment: {rod_type}")
    print(f"The image link is: {image_link}")

    
    # Append new data to the list
    all_data.append(data)

# Save all data to the JSON file
with open('assets/data/sea_creature_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

# Done
print("Data has been saved to sea_creature_data.json")
