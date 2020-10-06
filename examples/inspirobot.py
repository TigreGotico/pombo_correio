from pybrowser import PyBrowser


class Inspirobot(PyBrowser):
    def __init__(self, exec_path=None, headless=True):
        super().__init__(exec_path, headless, "https://inspirobot.me/")

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
       print(url)