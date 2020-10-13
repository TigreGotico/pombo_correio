from pombo_correio import FirefoxBrowser


class Inspirobot(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=True):
        super().__init__(geckodriver, headless, "https://inspirobot.me/")

    def generate(self):
        self.driver.get(self.homepage)
        xpath = "/html/body/div[2]/div[1]/div[1]/div[2]/div"
        button = self.wait_for_xpath(xpath)
        button.click()

        picture = self.wait_for_css_selector(".generated-image")
        return picture.get_attribute("src")


if __name__ == "__main__":
    from os.path import join, dirname

    geckodriver = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    # Using context manager
    with Inspirobot(geckodriver) as bot:
       url = bot.generate()
    """
BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'homepage': 'https://inspirobot.me/'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': 'Generate', 'href': None, 'element_id': '7070cd65-9a4d-4634-960d-f9776aa7b296'}
BrowserEvents.WAIT_FOR_CSS {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.CSS_FOUND {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': '', 'href': 'https://generated.inspirobot.me/a/rVJqw1KQ6w.jpg', 'element_id': 'b31c8dfc-4710-4e6e-a265-735d65cb0aab'}
BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://inspirobot.me/', 'tab2url': {'15': 'https://inspirobot.me/'}}
    """