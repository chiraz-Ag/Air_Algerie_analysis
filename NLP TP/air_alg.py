from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time



NB_PAGES = 3  

# Empêche Chrome de se fermer automatiquement
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

all_data = []



for page in range(1, NB_PAGES + 1):

    url = f"https://www.trustpilot.com/review/airalgerie.dz?page={page}"
    driver.get(url)

    print(f"Scraping page {page}...")
    time.sleep(5)

    reviews = driver.find_elements(By.CSS_SELECTOR, "article")

    for review in reviews:
        try:
            titre = review.find_element(By.CSS_SELECTOR, "h2").text
            commentaire = review.find_element(By.CSS_SELECTOR, "p").text
            note = review.find_element(By.CSS_SELECTOR, "[data-service-review-rating]").get_attribute("data-service-review-rating")
            date = review.find_element(By.TAG_NAME, "time").text

            all_data.append({
                "Note": note,
                "Titre": titre,
                "Commentaire": commentaire,
                "Date": date
            })

        except:
            continue



df = pd.DataFrame(all_data)

print("\n===== REVIEWS SCRAPED =====\n")
print(df)

# Sauvegarde CSV
df.to_csv("trustpilot_air_algerie_reviews.csv", index=False, encoding="utf-8-sig")

