from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import os

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
        driver.get("https://www.minuteinbox.com/email/id/2")
        try:
            driver.get(driver.find_element(By.XPATH,
                    "/html/body/div/div/div/center/div/center/table/tbody/tr[2]/td/p/a[1]").get_attribute("href"))
            break
        except: pass

def login(driver, email, password):
    driver.get("https://singlelogin.org/")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.XPATH,
        "/html/body/table/tbody/tr[2]/td/div/div/div/div/div/form/button").click()

def get_browser():
    while True:
        browser = input("chrome/gecko/tor > ")
        if browser == "chrome" or browser == "gecko" or browser == "tor":
            return browser

def get_port():
    port = input("tor proxy port (default 9050) > ")
    return (port, "9050")[port == ""]

def get_address():
    address = input("tor proxy address (default 127.0.0.1) > ")
    return (address, "127.0.0.1")[address == ""]

def get_torrc():
    torrc = input("where is your torrc folder (default /etc/tor/) > ")
    return (torrc, "/etc/tor/")[torrc == ""]

def set_privacy_settings(profile):
    profile.set_preference("places.history.enabled", False)
    profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
    profile.set_preference("privacy.clearOnShutdown.passwords", True)
    profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
    profile.set_preference("privacy.sanitize.sanitizeOnShutdown", False)
    profile.set_preference("singon.rememberSingons", False)
    profile.set_preference("network.cookie.lifetimePolicy", 2)
    profile.set_preference("network.dns.disablePrefetch", True)
    profile.set_preference("network.http.sendRefererHeader", 0)

def set_proxy_settings(profile, address, port):
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks_version", 5)
    profile.set_preference("network.proxy.socks", address)
    profile.set_preference("network.proxy.socks_port", int(port))
    profile.set_preference("network.proxy.socks_remote_dns", True)

    # javascript can be used to reveal your true ip
    profile.set_preference("javascript.enabled", False)

def check_tor(driver):
    try:
        driver.get("https://check.torproject.org/")
    except:
        driver.close()
        print("FATAL: INVALID PROXY SETTINGS")
        exit()

    if driver.find_element(By.XPATH, "/html/body/div[2]/h1").text == "Sorry. You are not using Tor.":
        driver.close()
        print("FATAL: NOT CONNECTED TO TOR")
        exit()

browser = get_browser()

if browser == "chrome":
    driver = webdriver.Chrome()
if browser == "gecko":
    driver = webdriver.Firefox()
if browser == "tor":
    torrc = get_torrc()
    address = get_address()
    port = get_port()

    profile = webdriver.FirefoxProfile(torrc)

    set_privacy_settings(profile)
    set_proxy_settings(profile, address, port)

    driver = webdriver.Firefox(firefox_profile=profile)
   
driver.implicitly_wait(2)

if browser == "tor":
    print("proxy address = " + address)
    print("proxy port = " + port)

    print("checking tor")
    check_tor(driver)

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
