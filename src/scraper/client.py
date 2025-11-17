
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from services import log_service

def fetch_search_page(driver: webdriver.Chrome, url: str, genre: str, wait_time: int = 5, page = 1) -> str:

     log_service.log_info(f"Fetching search page for genre '{genre}' at page {page}...")

     driver.get(url)

     log_service.log_info(f"Page loaded for URL: {url}")
     
     header_shadow_root_element = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='__header_root_']"))
     )

     log_service.log_info("Waiting for header shadow root element to be present...")

     try:
          header_shadow_root = driver.execute_script("return arguments[0].shadowRoot", header_shadow_root_element)
         
          search_link = header_shadow_root.find_element(
               By.CSS_SELECTOR,
               "a[data-tracking='explore-all']"
          )

          log_service.log_info("Found search link in header shadow root.")

          search_url = f"{search_link.get_attribute('href')}?genre_exact={genre}&page={page}"
          # esperar pagina carregar
          driver.get(search_url)
          time.sleep(wait_time)
          log_service.log_info(f"Search page loaded for genre '{genre}' at page {page}.")
        
     except Exception as e:
          log_service.log_error(f"Error while fetching search page: {e}")
          raise e
     
     page_source = driver.page_source
     
     log_service.log_info(f"Returning page source for genre '{genre}' at page {page}.")

     return page_source

def fetch_artist_page(driver: webdriver.Chrome, artist_url: str, wait_time: int = 5) -> str:     
     log_service.log_info(f"Fetching artist page for URL: {artist_url}")

     driver.get(artist_url)
     time.sleep(wait_time)

     log_service.log_info(f"Artist page loaded for URL: {artist_url}")

     page_source = driver.page_source
     return page_source

def fetch_album_page(driver: webdriver.Chrome, album_url: str, wait_time: int = 5) -> str:
     log_service.log_info(f"Fetching album page for URL: {album_url}")

     driver.get(album_url)
     time.sleep(wait_time)
     log_service.log_info(f"Album page loaded for URL: {album_url}")
     page_source = driver.page_source
     return page_source
