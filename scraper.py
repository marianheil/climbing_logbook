from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

BASE_URL = "https://klettern-ettringen.de"


def get_page(driver, url: str):
    print(f"Called {url}")
    driver.get(url)
    driver.implicitly_wait(1)
    return BeautifulSoup(driver.page_source, "html.parser")


def parse_routes(entry):
    # example text: 'Gastspiel (a.k.a. Null Problemo) (8)'
    texts = entry.text.split("(")
    return {"name": "(".join(texts[:-1]).strip(), "grade": texts[-1][:-1].strip()}


def get_routes_for_sector(driver, sector_url):
    return [
        parse_routes(entry)
        for entry in get_page(driver, sector_url).select(".ke-content-main ol li")
    ]


def parse_zone(driver, zone_entry):
    return [
        {
            "name": sector.text.strip(),
            "url": sector.get("href"),
            "routes": get_routes_for_sector(driver, sector.get("href")),
        }
        for sector in zone_entry.select("a")
    ]


def get_zones_for_region(driver, region_url):
    return [
        {
            "name": zone_entry.text.split("(")[0].strip(),
            "sectors": parse_zone(driver, zone_entry),
        }
        for zone_entry in get_page(driver, region_url).select(".entry-content ul li")
    ]


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

regions = []

# Adapt selector based on real DOM structure
for page_entry in get_page(driver, f"{BASE_URL}/basalt/routen-datenbank").select(
    ".wp-block-list li"
):  # example, adjust class
    region_name = page_entry.text.strip()
    region_url = page_entry.find("a").get("href")
    zones = get_zones_for_region(driver, region_url)
    regions.append({"name": region_name, "url": region_url, "zones": zones})

driver.quit()

with open("ettringen_all_routes.json", "w", encoding="utf8") as f:
    json.dump(regions, f, ensure_ascii=False, sort_keys=True, indent=4)
