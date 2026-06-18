import time
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def get_full_article_text(url):
    headers = {
        'User-Agent': 'chrome'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        body = soup.find('div', class_='tm-article-body')
        if not body:
            body = soup.find('div', class_='article-formatted-body')
        if not body:
            body = soup.find('div', class_='post-content')
        if body:
            return body.get_text(separator=' ', strip=True)
        return None
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return None

def parse_habr():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Загрузка главной страницы...")
        driver.get('https://habr.com/ru/all/')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tm-articles-list__item"))
        )

        # Прокрутка для подгрузки всех статей
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        articles = driver.find_elements(By.CLASS_NAME, "tm-articles-list__item")
        print(f"Всего статей на странице: {len(articles)}\n")

        found_preview = []   # статьи, найденные по заголовку + preview
        found_fulltext = []  # статьи, найденные только после загрузки полного текста

        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, "a.tm-title__link")
                title = title_element.text.strip()
                link = title_element.get_attribute("href")

                date_element = article.find_element(By.CSS_SELECTOR, "time")
                date_str = date_element.get_attribute("datetime")
                try:
                    dt = datetime.fromisoformat(date_str)
                    formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = date_str

                # Пробуем получить preview
                try:
                    preview = article.find_element(By.CSS_SELECTOR, ".tm-article-body").text.strip()
                except:
                    preview = ""

                # Проверяем preview
                text_preview = f"{title} {preview}".lower()
                found_in_preview = any(kw.lower() in text_preview for kw in KEYWORDS)

                if found_in_preview:
                    found_preview.append((formatted_date, title, link))
                else:
                    # Если в preview не найдено – загружаем полный текст
                    print(f"Проверяем полный текст: {title[:50]}...")
                    full_text = get_full_article_text(link)
                    if full_text and any(kw.lower() in full_text.lower() for kw in KEYWORDS):
                        found_fulltext.append((formatted_date, title, link))
                    time.sleep(0.3)

            except Exception as e:
                print(f"Ошибка при обработке статьи: {e}")
                continue

        # Вывод результатов
        print("\n" + "=" * 50)
        print("Статьи, найденные по заголовку + preview:")
        print("=" * 50)
        if found_preview:
            for date, title, link in found_preview:
                print(f"{date} – {title} – {link}")
        else:
            print("(нет таких статей)")

        print("\n" + "=" * 50)
        print("Статьи, найденные только после загрузки полного текста:")
        print("=" * 50)
        if found_fulltext:
            for date, title, link in found_fulltext:
                print(f"{date} – {title} – {link}")
        else:
            print("(нет таких статей)")

        total = len(found_preview) + len(found_fulltext)
        print(f"\nВсего найдено статей с ключевыми словами: {total}")

    finally:
        driver.quit()

if __name__ == '__main__':
    parse_habr()