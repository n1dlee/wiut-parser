from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Настройки
USERNAME = "YOUR_LOGIN_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"
BASE_URL = "https://srs.wiut.uz"
MAX_RETRIES = 3
START_GROUP_ID = 13000  # Начальный ID группы
END_GROUP_ID = 13486  # Конечный ID группы
TARGET_NAMES = [
    {"First Name": "", "Last Name": "", "Found": False}
]


def attempt_login(driver):
    """Функция для выполнения попытки входа"""
    try:
        print("Попытка входа...")

        # Ввод логина
        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user"))
        )
        user_input.clear()
        user_input.send_keys(USERNAME)

        # Ввод пароля
        pass_input = driver.find_element(By.ID, "pass")
        pass_input.clear()
        pass_input.send_keys(PASSWORD)

        # Отправка формы
        pass_input.send_keys(Keys.RETURN)

        print("Форма отправлена.")
    except TimeoutException:
        print("Ошибка: Поля ввода недоступны.")


def login_with_retries(driver):
    """Функция для выполнения нескольких попыток входа"""
    driver.get(f"{BASE_URL}/Account/LoginMain")
    
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Попытка входа #{attempt}")
        attempt_login(driver)
        time.sleep(2)  # Пауза между попытками


def get_group_members(driver, group_id):
    """Функция для извлечения участников группы"""
    group_url = f"{BASE_URL}/groups/studentgroup/getgroupmembers?groupId={group_id}"
    driver.get(group_url)

    try:
        print(f"Ожидание загрузки участников группы {group_id}...")
        modal_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-body"))
        )
        table = modal_body.find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        members = []
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 2:
                first_name = cols[0].text.strip()
                last_name = cols[1].text.strip()
                members.append({"First Name": first_name, "Last Name": last_name})
        
        print(f"Найдено {len(members)} участников в группе {group_id}.")
        return members
    except TimeoutException:
        print(f"Ошибка: Не удалось загрузить участников группы {group_id}.")
        return []


def save_results_to_file(results, filename="results.txt"):
    """Функция для сохранения результатов в текстовый файл"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Результаты поиска:\n")
        file.write("=" * 30 + "\n")
        
        for result in results:
            if "Group ID" in result:
                file.write(
                    f"Найдено: {result['First Name']} {result['Last Name']} в группе ID {result['Group ID']}\n"
                )
            else:
                file.write(
                    f"Не найдено: {result['First Name']} {result['Last Name']}\n"
                )

        file.write("=" * 30 + "\n")
        print(f"Результаты сохранены в файл: {filename}")


def search_target_names(driver, start_id, end_id, target_names):
    """Функция для поиска указанных имён в группах"""
    results = []  # Список для хранения результатов

    for group_id in range(start_id, end_id + 1):
        print(f"Проверка группы ID: {group_id}")
        members = get_group_members(driver, group_id)

        # Проверка на совпадение имён
        for target in target_names:
            for member in members:
                if member["First Name"] == target["First Name"] and member["Last Name"] == target["Last Name"]:
                    print(f"Найдено: {target['First Name']} {target['Last Name']} в группе ID {group_id}")
                    results.append({"First Name": target["First Name"], "Last Name": target["Last Name"], "Group ID": group_id})

    # Добавляем информацию о ненайденных участниках
    found_names = {(result["First Name"], result["Last Name"]) for result in results}
    for target in target_names:
        if (target["First Name"], target["Last Name"]) not in found_names:
            results.append({"First Name": target["First Name"], "Last Name": target["Last Name"]})

    # Сохранение результатов в файл
    save_results_to_file(results)


def main():
    driver = webdriver.Chrome() 
    
    try:
        login_with_retries(driver)

        # Начинаем поиск по ID групп
        search_target_names(driver, START_GROUP_ID, END_GROUP_ID, TARGET_NAMES)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
