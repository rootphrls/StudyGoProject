import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def check_info(username,password):
    WINDOW_SIZE = "1920,1080"

    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Firefox(options=firefox_options)

    wait = WebDriverWait(driver,3)

    driver.get("https://studygo.com/nl/?gclid=EAIaIQobChMI8-vU5In6gQMVhKztCh1SpQB0EAAYASAAEgJgVfD_BwE")

    cookies = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cookie-policy-intro"]/div/a/div')))
    cookies = driver.find_element(By.XPATH, '//*[@id="cookie-policy-intro"]/div/a/div')

    cookies.click()

    niet_veranderen = wait.until(EC.element_to_be_clickable((By.ID,"trp_ald_x_button_textarea")))
    niet_veranderen = driver.find_element(By.ID,"trp_ald_x_button_textarea")
    niet_veranderen.click()

    inloggen = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div/div[3]/a/span')))
    inloggen = driver.find_element(By.XPATH, '/html/body/div[1]/header/div/div/div[3]/a/span')
    inloggen.click()

    username_input = wait.until(EC.element_to_be_clickable((By.NAME,"email")))
    username_input = driver.find_element(By.NAME,"email")
    username_input.send_keys(username)

    password_input = wait.until(EC.element_to_be_clickable((By.NAME,"password")))
    password_input = driver.find_element(By.NAME,"password")
    password_input.send_keys(password)


    login_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div[1]/form/div[3]/button')
    login_button.click()

    time.sleep(3)

    title = driver.title

    if title == "Inloggen | StudyGo":
        return False
    else:
        return True