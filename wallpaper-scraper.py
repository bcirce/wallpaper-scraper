from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request

# to run Firefox in headless mode
options = Options()
options.add_argument("--headless")

# initialize a Firefox WebDriver instance
driver = webdriver.Firefox(
    service=FirefoxService(),
    options=options
)

driver.maximize_window()

# Function to scrape image URLs from a given URL
def scrape_images_from_url(driver, url, category, max_num_images=3, wallpaper_folder="C:\\Users\\barba\\git\\wallpaper-scraper\\wallpapers\\"):
    driver.get(url)
    
    # select the node images on the page
    image_html_nodes = driver.find_elements(By.CSS_SELECTOR, "[data-testid=\"photo-grid-masonry-img\"]")
    image_urls = []

    # extract the URLs from each image
    for image_html_node in image_html_nodes:
        try:
            # use the URL in the "src" as the default behavior
            image_url = image_html_node.get_attribute("src")

            # extract the URL of the largest image from "srcset",
            # if this attribute exists
            srcset = image_html_node.get_attribute("srcset")
            if srcset is not None:
                # get the last element from the "srcset" value
                srcset_last_element = srcset.split(", ")[-1]
                # get the first element of the value,
                # which is the image URL
                image_url = srcset_last_element.split(" ")[0]

            # add the image URL to the list
            image_urls.append(image_url)
        except StaleElementReferenceException:
            continue

    # to keep track of the images saved to disk
    image_name_counter = 1

    for image_url in image_urls:
        if image_name_counter > max_num_images:
            break
        print(f"downloading image no. {image_name_counter} for category '{category}'...")

        file_name = wallpaper_folder + f"{category}_{image_name_counter}.jpg"
        # download the image
        urllib.request.urlretrieve(image_url, file_name)

        print(f"Image saved as \"{file_name}\"\n")

        # increment the image counter
        image_name_counter += 1

# List of categories to automate
categories = [
    "wallpaper",
    "nature",
    "abstract",
    "animals",
    "archival",
    "architecture-interior",
    "film",
    "food-drink",
    "sports",
    "street-photography",
    "textures-patterns",
    "travel"
]

base_url = "https://unsplash.com/s/photos/{category}?license=free"

# Automate for multiple categories
for category in categories:
    print(f"Scraping category: {category}")
    formatted_url = base_url.format(category=category)
    scrape_images_from_url(driver, formatted_url, category)

driver.quit()
