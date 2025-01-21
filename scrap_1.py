import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# IMDb Top 250 URL
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
driver.get(url)

all_movies_titles = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//a[@class='ipc-title-link-wrapper']")
    )
)
    
all_links = [movie.get_attribute("href") for movie in all_movies_titles]
print(f"Total movies found: {len(all_links)}")

# Iterate through the movie links
for link in all_links:  # Test with the first 5 movies; remove `[:5]` to fetch all
    driver.get(link)  # Navigate to the movie page
    
    try:
        # Wait for the title to load
        title_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@data-testid='hero__pageTitle' or @textlength='24']"))
        )
        title = title_element.text
        print(f"Movie Title: {title}")
        
        # Extract rating
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='hero-rating-bar__aggregate-rating__score' and starts-with(@class, 'sc-')]"))
            )
            rating = rating_element.text
        except Exception:
            rating = "N/A"
        print(f"Rating: {rating}")
        
        # Extract plot
        try:
            plot_element = driver.find_element(By.XPATH, "//span[@data-testid='plot-xl' and @role='presentation']")
            plot = plot_element.text
        except Exception:
            plot = "N/A"
        print(f"Plot: {plot}")
        
        try:
            writer_element = WebDriverWait(driver, 30).until(
               EC.presence_of_all_elements_located((By.XPATH, "//p[@data-testid='plot']/..//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt']/li"))
            )
            for w in writer_element:
                print(str(w.text).replace('\n', ':'))
        except Exception:
            writer = "N/A"
        print(f"Writer: {writer}")
        
        print("-" * 50)
    except Exception as e:
        print(f"Error fetching data for {link}: {e}")
    
    time.sleep(3)  # Small pause between requests

for data in all_links:
    driver.get(data)
    time.sleep(3)

driver.quit()

