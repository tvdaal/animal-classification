# Credits go to Nikola Zivkovic from Rubik's Code for providing this module.
# The code can be found here:
# https://rubikscode.net/2021/06/21/scraping-images-with-python/.
# I only implemented minor modifications.


import hashlib
import io
import os
from PIL import Image
import requests
from selenium import webdriver
import time


class GoogleScraper():
    '''Downloades images from google based on the query.
       webdriver - Selenium webdriver
       max_num_of_images - Maximum number of images that we want to download
    '''
    def __init__(self, webdriver: webdriver, max_num_of_images: int = 400):
        self.wd = webdriver
        self.max_num_of_images = max_num_of_images

    def _scroll_to_the_end(self):
        for _ in range(4): # A maximum of 400 images can be loaded.
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Provides a window with 100 images.
            time.sleep(5)

    def _build_query(self, query: str):
        return f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"

    def _get_info(self, query: str):
        image_urls = set()

        self.wd.get(self._build_query(query))
        time.sleep(1)
        self._scroll_to_the_end()

        # img.Q4LuWd is the google tumbnail selector
        thumbnails = self.wd.find_elements_by_css_selector("img.Q4LuWd")

        # print(f"Found {len(thumbnails)} images...")
        # print(f"Obtaining the links...")

        for img in thumbnails[0:self.max_num_of_images]:
            # We need to click every thumbnail so we can get the full image.
            try:
                img.click()
            except Exception:
                # print('ERROR: Cannot click on the image.')
                continue

            images = self.wd.find_elements_by_css_selector('img.n3VNCb')
            time.sleep(1)

            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))

        return image_urls

    def download_image(self, folder_path: str, url: str):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            pass # print(f"ERROR: Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')

            with open(file, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            # print(f"SUCCESS: saved {url} - as {file}")

        except Exception as e:
            pass # print(f"ERROR: Could not save {url} - {e}")

    def scrape_images(self, query: str, folder: str):
        print(f"Searching for {query}...")

        if not os.path.exists(folder):
            os.makedirs(folder)

        image_info = self._get_info(query)
        # print(f"Downloading the images...")

        for image in image_info:
            self.download_image(folder, image)
