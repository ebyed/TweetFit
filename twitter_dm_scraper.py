import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")  # Full screen
# options.add_argument("--headless")  # Uncomment this to run without GUI
DM_GROUP_ID = "1212682433683963904"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔍 Opening Twitter...")
    driver.get("https://twitter.com")

    # Load saved cookies
    with open("twitter_cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    print("✅ Cookies loaded! No login required.")

    # Refresh to apply cookies and navigate directly to the group chat
    driver.get(f"https://twitter.com/messages/{DM_GROUP_ID}")

    # Wait for messages to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains(f"messages/{DM_GROUP_ID}"))
    time.sleep(5)  # Allow chat to load

    print("📩 Extracting messages from the group chat...")

    # Scroll multiple times to load all messages from January
    for _ in range(10):  # Adjust the range based on message history
        driver.execute_script("window.scrollBy(0, -500);")
        time.sleep(2)

    # Extract messages and timestamps
    messages = driver.find_elements(By.XPATH, "//div[@data-testid='messageEntry']")
    timestamps = driver.find_elements(By.XPATH, "//time")  # Extract timestamps

    with open("january_messages.txt", "w", encoding="utf-8") as file:
        for index, msg in enumerate(messages):
            message_text = msg.text.strip()
            message_date = timestamps[index].get_attribute("datetime")  # Extracts full timestamp

            # Convert timestamp to readable format (e.g., "2024-01-15T12:34:56.000Z")
            if message_date.startswith("2024-01"):  # Only keep messages from January
                print(f"📩 {message_date}: {message_text}\n")
                file.write(f"{message_date}: {message_text}\n")

    print("✅ Done extracting messages from January! Saved in 'january_messages.txt'")

except Exception as e:
    print("❌ Error:", str(e))
    driver.save_screenshot("error_screenshot.png")  # Take a screenshot for debugging
    print("📸 Error screenshot saved as 'error_screenshot.png'")

finally:
    driver.quit()