from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_product_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        product_name = driver.find_element(By.ID, 'productTitle').text
        product_price = driver.find_element(By.ID, 'priceblock_ourprice').text
        return {
            'name': product_name.strip(),
            'price': float(product_price.replace('$', '').replace(',', ''))
        }
    except Exception as e:
        print(f"Error scraping data: {e}")
        return None
    finally:
        driver.quit()
