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

    exec_path = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    # Using context manager
    with Inspirobot(exec_path) as bot:
       url = bot.generate()
       """
      BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://inspirobot.me/', 'tab2url': {'15': 'https://inspirobot.me/'}}
        BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
        BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': 'Generate', 'href': None, 'element_id': '42fea98e-bb8d-49e9-b309-4468f6e46258'}
        BrowserEvents.WAIT_FOR_CSS {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
        BrowserEvents.CSS_FOUND {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': '', 'href': 'https://generated.inspirobot.me/a/rVJqEXgbJw.jpg', 'element_id': '8777ca1c-5351-46f0-b299-9571dc2ed646'}
        BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://inspirobot.me/', 'tab2url': {'15': 'https://inspirobot.me/'}}
       """