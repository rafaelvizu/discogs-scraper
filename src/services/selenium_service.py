from selenium import webdriver


def get_driver() -> webdriver.Chrome:
     options = webdriver.ChromeOptions()
     options.add_argument('--no-sandbox')
     options.add_argument('--start-maximized')
     options.add_argument('--disable-dev-shm-usage')
     driver = webdriver.Chrome(options=options)
     driver.set_page_load_timeout(30)
     driver.set_script_timeout(30)

     
     return driver

