# WordPress Automation Test Suite

## Overview
This automation suite is designed to test the "WP Dark Mode" plugin for WordPress. It will:
- Log in to the WordPress site.
- Check if the WP Dark Mode plugin is active, and if not, install and activate it.
- Perform various customizations in the WP Dark Mode settings.
- Validate dark mode on the Admin Dashboard and frontend.

## Setup and Installation

### Requirements
- Python 3.12.5
- Selenium
- Chrome WebDriver (Ensure you download the appropriate version for your Chrome browser)

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repository-name.git

   
### Scenarios of Test Plan

- In this Test Plan I aim to test the following key scenarios:
1. Guest checkout (without login)
2. Registered user checkout
3. Payment method selection
4. Applying coupon codes
5. Free shipping and tax calculation
   
### Scenarios of Test Suite
1. Login to the admin panel.
2. navigate to the plugins screen.
3. Check whether the "WP Dark Mode" plugin is already installed/active/not installed/not active.
4. If not installed->install,not active-> activate, installed and active -> move furthur.
5. customize the WP floating button concerning size and position.

### Results of Test Suite
1. Login to the admin panel. (Success)
2. navigate to the plugins screen. (Success)
3. Check whether the "WP Dark Mode" plugin is already installed/active/not installed/not active. (Success)
4. If not installed->install,not active-> activate, installed and active -> move furthur. (Failed as WordPress Plugin Don't allow it with automated script, msg "sorry you are not allowed to access this page")
5. customize the WP floating button concerning size and position.(Failed as WordPress Plugin Don't allow it with automated script, msg "sorry you are not allowed to access this page")
