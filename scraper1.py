from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

def get_html_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html

def scrape_hourly_weather(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.city-list__item")

    weather_data = []
    for item in items:
        try:
            godzina = item.select_one(".city-list__title").text.strip()
            temperatura = item.select_one(".json-temperature").text.strip()
            warunki = item.select_one(".city-list__temp--string").text.strip()
            odczuwalna = item.select_one(".json-temp-sensed").text.strip()
            wiatr = item.select_one(".json-wind-speed").text.strip()
            porywy = item.select_one(".json-wind-speed-max").text.strip()
            opady = item.select_one(".json-raining-amount").text.strip()
            cisnienie = item.select_one(".json-pressure").text.strip()
            wilgotnosc = item.select_one(".json-humidity").text.strip()
            chmury = item.select_one(".json-clouds-amount").text.strip()
            termika = item.select_one(".json-thermals").text.strip()
            biomet = item.select_one(".json-biomet").text.strip()
        except AttributeError:
            continue

        weather_data.append({
            "Godzina": godzina,
            "Temp (°C)": temperatura,
            "Odczuwalna (°C)": odczuwalna,
            "Warunki": warunki,
            "Wiatr": wiatr,
            "Porywy": porywy,
            "Opady": opady,
            "Ciśnienie": cisnienie,
            "Wilgotność": wilgotnosc,
            "Chmury": chmury,
            "Termika": termika,
            "Biomet": biomet
        })
    return weather_data

def save_to_csv(data, filename="pogoda.csv"):
    if not data or not isinstance(data, list) or not isinstance(data[0], dict):
        print("❌ Brak danych lub nieprawidłowy format danych do zapisania.")
        return

    keys = list(data[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()  # <-- To zapisuje nagłówki
        writer.writerows(data)

    print(f"✅------------> Dane zapisane do pliku (nadpisano): {filename}")


def plot_column(df, column_name, filename):
    try:
        df[column_name] = (
            df[column_name]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.extract(r"([-+]?\d*\.?\d+)", expand=False)
            .astype(float)
        )
    except Exception as e:
        print(f"Błąd przy konwersji kolumny {column_name}: {e}")
        return

    plt.figure(figsize=(10, 4))
    plt.plot(df["Godzina"], df[column_name], marker="o")
    plt.title(f"{column_name} wg godziny")
    plt.xlabel("Godzina")
    plt.ylabel(column_name)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, format="png")
    plt.close()
    print(f"✅ ----------------> Wykres zapisany jako: {filename}")

def plot_temperature_chart():
    df = pd.read_csv("pogoda.csv", encoding="utf-8")
    df = df.dropna(subset=["Godzina"])
    df = df.tail(24)  # tylko ostatni dzień

    plot_column(df, "Temp (°C)", "temp.png")
    plot_column(df, "Wilgotność", "wilgotnosc.png")
    plot_column(df, "Ciśnienie", "cisnienie.png")
    plot_column(df, "Wiatr", "wiatr.png")

# URL do strony pogodowej
city_url = "https://www.twojapogoda.pl/prognoza-godzinowa-polska/podkarpackie-rzeszow/"

# Główna logika działania
html = get_html_selenium(city_url)
data = scrape_hourly_weather(html)
save_to_csv(data)
plot_temperature_chart()
