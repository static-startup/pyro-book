from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_email(driver):
    driver.get("https://www.minuteinbox.com/")
    return driver.find_element(By.XPATH, "//*[@id=\"email\"]").text

def register(driver, email, name, password):
    driver.get("https://singlelogin.org/registration.php")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//*[@id=\"registrationForm\"]/button").click()

def confirm(driver):
    while True:
        driver.get("https://www.minuteinbox.com/window/id/2")
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/p")
        except: break

    driver.switch_to.frame(1)
    driver.get(driver.find_element(By.XPATH,
            "/html/body/div/div/div/center/div/center/table/tbody/tr[2]/td/p/a[1]").text)

def login(driver, email, password):
    driver.get("https://singlelogin.org/")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH,
            "/html/body/table/tbody/tr[2]/td/div/div/div/div/div/form/button").click()

driver = webdriver.Chrome()
driver.implicitly_wait(1)

email = get_email(driver)
password = "123456"
name = "123"

print("email = " + email)
print("password = " + password)
print("name = " + name)

register(driver, email, name, password)

print("registration successful")

confirm(driver)

print("account confirmed")

login(driver, email, password)

print("logined in")

print("account creation process complete")
time.sleep(99999999)
