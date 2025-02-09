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
DM_GROUP_NAME = "🏋️‍♀️സാത്യൂസ് FiTStoP 💪"

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

    # Refresh the page to apply cookies
    driver.get("https://twitter.com/messages")

    # Wait until the messages page loads
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("messages"))
    time.sleep(5)  # Allow time for chat to load

    # Locate the Specific Group Chat
    print(f"🔍 Searching for group chat: {DM_GROUP_NAME}...")

    group_chat = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{DM_GROUP_NAME}')]"))
    )
    group_chat.click()
    print(f"✅ Opened group chat: {DM_GROUP_NAME}")

    time.sleep(5)  # Allow chat messages to load

    # Extract Messages from the Group Chat
    print("📩 Extracting messages from the group chat...")

    messages = driver.find_elements(By.XPATH, "//div[@data-testid='messageEntry']")
    
    with open("group_dm_messages.txt", "w", encoding="utf-8") as file:
        for index, msg in enumerate(messages):
            message_text = msg.text.strip()
            print(f"📩 Message {index+1}: {message_text}\n")
            file.write(f"Message {index+1}: {message_text}\n")

    print("✅ Done extracting messages! Saved in 'group_dm_messages.txt'")

except Exception as e:
    print("❌ Error:", str(e))
    driver.save_screenshot("error_screenshot.png")  # Take a screenshot for debugging
    print("📸 Error screenshot saved as 'error_screenshot.png'")

finally:
    driver.quit()