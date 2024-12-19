import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
import time

from colorama import init
init(autoreset=True)

CA = "# INSERT CA FROM DS LINK #"
URL = f"https://dexscreener.com/solana/{CA}"

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    uc.TARGET_VERSION = 130
    driver = uc.Chrome(options=options, version_main=130)
    return driver

def fetch_top_traders(driver):
    driver.get(URL)
    driver.maximize_window()
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        print(Fore.BLUE + f"URL: {URL}")
        print(Fore.GREEN + "Page loaded successfully!")
    except Exception as e:
        print(f"Page failed to load. Error: {e}")
    try:
        time.sleep(10)
        href_list = []
        elements = driver.find_elements(By.CLASS_NAME, "custom-1nvxwu0")
        if elements:
            for element in elements:
                nested_elements = element.find_elements(By.CLASS_NAME, "custom-1dwgrrr")
                if nested_elements:
                    for nested_element in nested_elements:
                        anchor_elements = nested_element.find_elements(By.TAG_NAME, "a")
                        for anchor in anchor_elements:
                            href = anchor.get_attribute("href")
                            if href:
                                href_list.append(href)
                else:
                    print("No nested elements found with class 'custom-1dwgrrr' inside this 'custom-1nvxwu0'.")
        else:
            print("No elements found with class 'custom-1nvxwu0'.")
    except Exception as e:
        print(f"Error finding elements: {e}")
    return href_list

def process_hrefs(href_list):
    base_url = "https://solscan.io/account/"
    return [href.replace(base_url, "") for href in href_list if href.startswith(base_url)]

def main():
    driver = setup_driver()
    href_list = fetch_top_traders(driver)
    wallet_list = process_hrefs(href_list)
    with open("list_top_traders.txt", "w") as file:
        for wallet in wallet_list:
            file.write(f"{wallet}\n")
    driver.quit()

if __name__ == "__main__":
    main()
