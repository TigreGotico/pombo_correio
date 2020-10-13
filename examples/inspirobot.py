from pombo_correio import FirefoxBrowser


class Inspirobot(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=True):
        super().__init__(geckodriver, headless, "https://inspirobot.me/")

    def generate(self):
        self.driver.get(self.homepage)
        self.find_and_click_xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div")
        picture = self.wait_for_css_selector(".generated-image")
        return self.get_element_attribute(picture, "src")


if __name__ == "__main__":
    from os.path import join, dirname

    geckodriver = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    # Using context manager
    with Inspirobot(geckodriver) as bot:
        url = bot.generate()
    """
BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'homepage': 'https://inspirobot.me/'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': 'Generate', 'href': None, 'element_id': '909e70af-535f-450c-b858-92726076ce62'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'element_text': 'Generate', 'tab_id': '15', 'url': 'https://inspirobot.me/', 'href': None}
BrowserEvents.WAIT_FOR_CSS {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.CSS_FOUND {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': '', 'href': 'https://generated.inspirobot.me/a/DdP0mzKg67.jpg', 'element_id': '8304217a-d004-43d5-86b9-7b28fcf19a6b'}
BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://inspirobot.me/', 'tab2url': {'15': 'https://inspirobot.me/'}}
    """