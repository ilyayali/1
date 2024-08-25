from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка опций браузера (например, запуск в фоновом режиме)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Путь к ChromeDriver, по умолчанию /usr/lib/chromium-browser/chromedriver, необходимо указать свой
SERVICE = Service("/usr/lib/chromium-browser/chromedriver")
DRIVER = webdriver.Chrome(service=SERVICE, options=chrome_options)
WAIT = WebDriverWait(DRIVER, 10)

BASE_URL = "https://www.wildberries.ru/catalog/{id_product}/detail.aspx"


def find_element_with_retry(url: str, retries: int = 3) -> set | list:
    """
    Функция поиска кэшбэка и цены c WB кошельком
    :param url: ссылка на товар
    :param retries: количество попыток
    :return: множество кэшбэк и цена
    """
    attempts: int = 0
    cash_back_and_price: set = set()
    while attempts < retries:
        try:
            DRIVER.get(url)
            wallet_price = WAIT.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "price-block__wallet-price")
                )
            )
            feedback_points = WAIT.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "feedbacks-points-sum")
                )
            )
            for wallet_price in wallet_price:
                cash_back_and_price.add(wallet_price.text[:-2])
            for feedback_point in feedback_points:
                cash_back_and_price.add(feedback_point.text[:-2])

            return cash_back_and_price

        except TimeoutException:
            attempts += 1
            print(f"Попытка {attempts} не удалась. Повторный поиск...")
        finally:
            DRIVER.quit()
    return []


if __name__ == "__main__":
    print(
        find_element_with_retry(
            "https://www.wildberries.ru/catalog/226986621/detail.aspx"
        )
    )
