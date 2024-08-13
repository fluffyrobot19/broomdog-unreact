import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


# fb login details from yaml file
yaml_file_path = 'login-details.yml'
with open(yaml_file_path, 'r') as file:
    conf = yaml.safe_load(file)
my_email = conf['fb_user']['email']
my_passwd = conf['fb_user']['password']


# disable notifications in chrome
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


driver = setup_driver()
wait = WebDriverWait(driver, 3)


def open_browser():
    try:
        driver.get("https://www.facebook.com/")
        print(" ✓ Facebook opened in new window")
    except Exception as e:
        print(e)


def decline_cookies():
    try:
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Decline optional cookies']").click()
        print(" ✓ cookies declined")
    except Exception as e:
        print(e)


def login():
    try:
        driver.find_element(By.ID, "email").send_keys(my_email)
        driver.find_element(By.ID, "pass").send_keys(my_passwd)
        driver.find_element(By.NAME, "login").click()
        print(" ✓ login successful")
    except Exception as e:
        print(e)


def settings_and_privacy():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Your profile']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Settings & privacy')]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Activity log')]"))).click()
        print(" ✓ locating activity log successful")
    except Exception as e:
        print(e)


def list_likes_and_reactions():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='List of activity log items']")))
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Your Facebook activity')]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Comments and reactions')]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Likes and reactions')]"))).click()
        print(" ✓ listing likes and reactions successful")
    except Exception as e:
        print(e)


def unreact_to_comments():
    try:
        action_options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[aria-label='Action options']")))
        print(len(action_options))
        for option in action_options:
            option.click()
            menu_item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='menuitem']")))
            target_element = menu_item.find_element(By.TAG_NAME, "span")
            if target_element.text == "Unlike":
                target_element.click()
            else:
                continue
    except Exception as e:
        print(e)


def main():
    open_browser()
    decline_cookies()
    login()
    settings_and_privacy()
    list_likes_and_reactions()
    unreact_to_comments()
    time.sleep(10)


main()
