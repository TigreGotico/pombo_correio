# Pombo Correio

## Overview

This repository provides an automated browser controller using Selenium and Selenium Wire. It includes classes and methods for handling browser sessions, managing events, interacting with web elements, and handling browser extensions. The primary goal is to simplify browser automation tasks such as web scraping, testing, and automated interactions with web pages.

## Features

- **Browser Session Management**: Start, stop, and manage browser sessions with ease.
- **Event Handling**: Define custom handlers for various browser events like opening URLs, clicking elements, switching tabs, etc.
- **Element Interaction**: Search, click, send keys, and submit forms using both CSS selectors and XPath.
- **Extension Management**: Load and manage default browser extensions such as ad blockers and cookie managers.
- **Headless Mode**: Run the browser in headless mode for faster execution and use in CI/CD pipelines.
- **Screenshot Capture**: Capture and save screenshots of the current browser view.

## Usage

To demonstrate the capabilities of this repository, let’s create a simple script that uses the `FirefoxBrowser` class to interact with the [Inspirobot](https://inspirobot.me/) website. The script will automatically generate a new inspirational image and retrieve the URL of the generated image.

### Example Script

```python
from pombo_correio import FirefoxBrowser

class Inspirobot(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=True):
        super().__init__(geckodriver, headless, "https://inspirobot.me/")

    def generate(self):
        self.goto_url(self.homepage)
        self.find_and_click_xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div")
        picture = self.wait_for_css_selector(".generated-image")
        return self.get_element_attribute(picture, "src")

geckodriver =  "path/to/geckodriver" # optional, set to None to use system firefox
# https://github.com/mozilla/geckodriver/releases

# Using context manager
with Inspirobot(geckodriver=geckodriver) as bot:
    url = bot.generate()
    print(url)
```

### How It Works

1. **Class Definition**: The `Inspirobot` class extends `FirefoxBrowser` and defines a method `generate()` to automate the process of generating and retrieving an inspirational image.

2. **Browser Navigation**: The script navigates to the Inspirobot homepage, clicks the "Generate" button, waits for the image to appear, and then retrieves the URL of the image.

3. **Running the Script**: When the script is run, it will print the URL of the generated inspirational image to the console.

### Requirements

- **Python**: Make sure you have Python installed.
- **Selenium and Selenium Wire**: Install these packages using pip:
  ```bash
  pip install selenium selenium-wire
  ```
- **Geckodriver**: Download `geckodriver` from the [official releases page](https://github.com/mozilla/geckodriver/releases) and place it in the same directory as the script or add it to your system's PATH.

> **NOTE** - if Geckodriver is not provided the system firefox install will be used if available

### Output

After running the script, you should see an output like this:

```
https://generated.inspirobot.me/a/1Derv5MQe0.jpg
```

This URL points to the newly generated inspirational image on Inspirobot.

## Acknowledgements

- [Selenium](https://www.selenium.dev/)
- [Selenium Wire](https://github.com/wkeeling/selenium-wire)
