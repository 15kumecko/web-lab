import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_scraper():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        file_path = f"file://{os.path.abspath('lab3/index.html')}"
        driver.get(file_path)
        
        wait = WebDriverWait(driver, 5)
        
        username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = driver.find_element(By.ID, "password")
        
        username_input.send_keys("admin")
        password_input.send_keys("1234")
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Увійти')]")
        login_button.click()
        
        wait.until(EC.presence_of_element_located((By.ID, "articles-container")))
        time.sleep(1) 
        
        articles = driver.find_element(By.ID, "articles-container").text
        print("Scraped data:")
        print(articles)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
