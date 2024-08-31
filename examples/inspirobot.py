from pombo_correio import FirefoxBrowser


class Inspirobot(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=True):
        super().__init__(geckodriver, headless, "https://inspirobot.me/")

    def generate(self):
        self.got_to_url(self.homepage)
        self.find_and_click_xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div")
        picture = self.wait_for_css_selector(".generated-image")
        return self.get_element_attribute(picture, "src")


if __name__ == "__main__":
    from os.path import join, dirname

    geckodriver = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    # Using context manager
    with Inspirobot() as bot:
        url = bot.generate()
        print(url)
        #url = bot.generate()
        #url = bot.generate()
    """
BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'homepage': 'https://inspirobot.me/'}
BrowserEvents.OPEN_URL {'url': 'https://inspirobot.me/', 'old_url': 'https://inspirobot.me/', 'tab_id': '15'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': 'Generate', 'href': None, 'element_id': '364aec34-c17b-4796-bb53-b0c1bdd6f4df'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'element_text': 'Generate', 'tab_id': '15', 'url': 'https://inspirobot.me/', 'href': None}
BrowserEvents.WAIT_FOR_CSS {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.CSS_FOUND {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': '', 'href': 'https://generated.inspirobot.me/a/1Derv5MQe0.jpg', 'element_id': 'b23bdcd9-adbb-4daf-a5ab-e87053da7d7f'}
BrowserEvents.OPEN_URL {'url': 'https://inspirobot.me/', 'old_url': 'https://inspirobot.me/', 'tab_id': '15'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': 'Generate', 'href': None, 'element_id': '6a237d5a-e1c1-416a-8d76-044a6475d954'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'element_text': 'Generate', 'tab_id': '15', 'url': 'https://inspirobot.me/', 'href': None}
BrowserEvents.WAIT_FOR_CSS {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.CSS_FOUND {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': '', 'href': 'https://generated.inspirobot.me/a/wGJgD9YbPQ.jpg', 'element_id': '3d65624f-1ed7-4216-bbdb-7b2ec5464984'}
BrowserEvents.OPEN_URL {'url': 'https://inspirobot.me/', 'old_url': 'https://inspirobot.me/', 'tab_id': '15'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'timeout': 10, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': 'Generate', 'href': None, 'element_id': 'bfa06859-1eac-4c4b-94b0-643d175b8c63'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[2]/div[1]/div[1]/div[2]/div', 'element_text': 'Generate', 'tab_id': '15', 'url': 'https://inspirobot.me/', 'href': None}
BrowserEvents.WAIT_FOR_CSS {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/'}
BrowserEvents.CSS_FOUND {'css_selector': '.generated-image', 'timeout': 30, 'tab_id': '15', 'url': 'https://inspirobot.me/', 'element_text': '', 'href': 'https://generated.inspirobot.me/a/1QJxL57GJz.jpg', 'element_id': '3f95d9ea-acce-429c-86f0-818604541e25'}
BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://inspirobot.me/', 'tab2url': {'15': 'https://inspirobot.me/'}}
    """