from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
from dotenv import load_dotenv  # Import this package

# Load the environment variables from .env
load_dotenv()

# WordPress login credentials from .env file
USERNAME = os.getenv("WORDPRESS_USERNAME")
PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WORDPRESS_URL = os.getenv("WORDPRESS_URL")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

# Initialize Selenium WebDriver (Chrome)
CHROMEDRIVER_PATH = "C:/Users/Zenkoders/Desktop/automation/chromedriver/chromedriver.exe" # Don't forget to change the path of your pc where ChromeDriver is.

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
driver.maximize_window()


def take_screenshot(name):
    # Ensure screenshots directory exists
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    driver.save_screenshot(f'screenshots/{name}.png')

def login_to_wordpress():
    driver.get(WORDPRESS_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_login")))

    # Enter username
    driver.find_element(By.ID, "user_login").send_keys(USERNAME)
    # Enter password
    driver.find_element(By.ID, "user_pass").send_keys(PASSWORD)
    # Click login button
    driver.find_element(By.ID, "wp-submit").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/wp-admin"))
    take_screenshot('login_success')

def is_plugin_active(plugin_slug):
    driver.get("https://dev-my-woo-store.pantheonsite.io/wp-admin/plugins.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "the-list")))

    try:
        plugin_row = driver.find_element(By.XPATH, f"//tr[contains(@data-slug, '{plugin_slug}')]")
        plugin_active = plugin_row.find_element(By.CLASS_NAME, 'active')
        if plugin_active:
            print(f"Plugin '{plugin_slug}' is active.")
            return True
    except NoSuchElementException:
        print(f"Plugin '{plugin_slug}' is not active or not installed.")
        return False

def install_and_activate_plugin(plugin_name, plugin_slug):
    driver.get("https://dev-my-woo-store.pantheonsite.io/wp-admin/plugin-install.php")
    
    try:
        # Ensure the plugin page is loaded and the search box is present
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-plugins"))
        )

        # Clear and search for the plugin
        search_box.clear()
        search_box.send_keys(plugin_name)
        search_box.send_keys(Keys.RETURN)
        print(f"Searching for plugin: {plugin_name}")

        # Wait until plugin results appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@data-slug='{plugin_slug}']"))
        )

        # Find the plugin card and attempt installation
        plugin_card = driver.find_element(By.XPATH, f"//div[@data-slug='{plugin_slug}']")
        install_button = plugin_card.find_element(By.XPATH, ".//button[contains(text(), 'Install Now')]")
        
        # Click the install button if found
        install_button.click()
        print(f"Clicked install for {plugin_name}")

        # Wait for the Activate button to appear
        activate_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@data-slug='{plugin_slug}']//a[contains(text(), 'Activate')]"))
        )
        activate_button.click()
        print(f"Activated plugin: {plugin_name}")

        # Confirm success by waiting for success notification or active status
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'updated')))
        take_screenshot('plugin_installed_and_activated')

    except TimeoutException:
        print(f"Timed out while searching or installing plugin '{plugin_name}'. Please check the network or plugin repository.")
        take_screenshot('plugin_installation_failed')
    except NoSuchElementException:
        print(f"Plugin '{plugin_name}' not found in search results or failed to install.")
        take_screenshot('plugin_not_found')

def customize_dark_mode():
    # Navigate to WP Dark Mode settings
    driver.get("https://dev-my-woo-store.pantheonsite.io/wp-admin/admin.php?page=wp-dark-mode-settings")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wp-dark-mode-enable-admin")))

    # Enable Admin Dashboard Dark Mode
    try:
        admin_toggle = driver.find_element(By.ID, "wp-dark-mode-enable-admin")
        if not admin_toggle.is_selected():
            admin_toggle.click()
            print("Admin Dashboard Dark Mode enabled.")
        take_screenshot('admin_dark_mode_enabled')
    except NoSuchElementException:
        print("Admin Dashboard Dark Mode toggle not found.")
        take_screenshot('admin_dark_mode_toggle_not_found')

    # Save settings
    try:
        save_button = driver.find_element(By.ID, "wp-dark-mode-submit")
        save_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'notice-success')))
        take_screenshot('settings_saved_admin_dark_mode')
    except NoSuchElementException:
        print("Save button not found.")
        take_screenshot('save_button_not_found')

def main():
    try:
        login_to_wordpress()

        plugin_slug = "wp-dark-mode"
        if not is_plugin_active(plugin_slug):
            install_and_activate_plugin("WP Dark Mode", plugin_slug)
        
        customize_dark_mode()

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
