"""
Scraper Google Play - Reviews App Air Algérie
App ID : com.amadeus.merci.ah
Utilise google-play-scraper (pip install google-play-scraper)
"""

import csv
import time
from google_play_scraper import reviews, Sort

APP_ID = "com.amadeus.merci.ah"
OUTPUT_CSV = "reviews_googleplay_air_algerie.csv"
COUNT = 500  # Nombre de reviews à récupérer (max ~3000)

def scrape_reviews():
    print(f"📱 App : {APP_ID}")
    print(f"🎯 Objectif : {COUNT} reviews\n")

    all_reviews = []

    # Scraper en français
    print("🌍 Langue : Français...")
    result_fr, _ = reviews(
        APP_ID,
        lang='fr',
        country='dz',
        sort=Sort.NEWEST,
        count=COUNT,
    )
    print(f"   ✅ {len(result_fr)} reviews en français")
    all_reviews.extend(result_fr)

    time.sleep(2)

    # Scraper en anglais
    print("🌍 Langue : Anglais...")
    result_en, _ = reviews(
        APP_ID,
        lang='en',
        country='dz',
        sort=Sort.NEWEST,
        count=COUNT,
    )
    print(f"   ✅ {len(result_en)} reviews en anglais")
    all_reviews.extend(result_en)

    time.sleep(2)

    # Scraper en arabe
    print("🌍 Langue : Arabe...")
    result_ar, _ = reviews(
        APP_ID,
        lang='ar',
        country='dz',
        sort=Sort.NEWEST,
        count=COUNT,
    )
    print(f"   ✅ {len(result_ar)} reviews en arabe")
    all_reviews.extend(result_ar)

    # Dédoublonner par ID
    seen = set()
    unique = []
    for r in all_reviews:
        if r['reviewId'] not in seen:
            seen.add(r['reviewId'])
            unique.append(r)

    print(f"\n🎉 Total unique : {len(unique)} reviews")
    return unique


def save_to_csv(reviews_list, filename):
    if not reviews_list:
        print("Aucune review à sauvegarder.")
        return

    fieldnames = ["note", "texte", "date", "reviewer", "likes", "version_app"]

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in reviews_list:
            writer.writerow({
                "note": r.get("score"),
                "texte": r.get("content"),
                "date": str(r.get("at", ""))[:10],
                "reviewer": r.get("userName"),
                "likes": r.get("thumbsUpCount", 0),
                "version_app": r.get("appVersion"),
            })

    print(f"💾 CSV sauvegardé : {filename} ({len(reviews_list)} reviews)")


def main():
    print("🚀 Scraper Google Play - Air Algérie App")
    print("=" * 50)

    try:
        reviews_list = scrape_reviews()
        save_to_csv(reviews_list, OUTPUT_CSV)
        print("\n✅ Terminé !")
    except ImportError:
        print("❌ Module manquant ! Lance d'abord :")
        print("   pip install google-play-scraper")


if __name__ == "__main__":
    main()