from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 2000, "height": 2000})
    page.goto(f"file://{os.getcwd()}/index.html")
    time.sleep(2)  # ждём, пока карта прогрузится
    page.screenshot(path="preview.png")
    browser.close()
