import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Twitter and log in manually
driver.get("https://twitter.com")

input("🔑 Log in manually, then press ENTER here to save cookies...")

# Save cookies
cookies = driver.get_cookies()
with open("twitter_cookies.pkl", "wb") as file:
    pickle.dump(cookies, file)

print("✅ Cookies saved! You can now use Selenium without logging in.")
driver.quit()
