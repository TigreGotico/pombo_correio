from pombo_correio import FirefoxBrowser


class Cleverbot(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=True):
        super().__init__(geckodriver, headless, "https://www.cleverbot.com/")
        self.utterances = []

    def new_session(self):
        super().new_session()
        self.utterances = []
        # click accept button
        self.find_and_click_xpath("/html/body/div[1]/div[2]/div[1]/div/div/form/input")

    def ask(self, utterance):
        # submit input
        xpath = "/html/body/div[1]/div[2]/div[3]/form/input[1]"
        self.find_and_send_keys_xpath(utterance, xpath)
        self.find_and_submit_xpath(xpath)

        # wait for response
        share_marker = '//*[@id="snipTextIcon"]'
        self.wait_for_xpath(share_marker)
        answer = self.get_xpath('/html/body/div[1]/div[2]/div[3]/p[9]/span[1]').text
        self.utterances.append((utterance, answer))
        return answer


if __name__ == "__main__":
    from os.path import join, dirname

    exec_path = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    # Using context manager
    with Cleverbot(exec_path) as bot:
        answer = bot.ask("hello")
        print(answer)
        answer = bot.ask("are you a bot")
        print(answer)
        answer = bot.ask("what is love")
        print(answer)
        answer = bot.ask("are you stupid")
        print(answer)
        answer = bot.ask("are you alive")
        print(answer)
        answer = bot.ask("does god exist")
        print(answer)
        answer = bot.ask("who created evil")
        print(answer)
        answer = bot.ask("are you religious")
        print(answer)
        answer = bot.ask("what is your favorite food")
        print(answer)

        path = bot.save_screenshot()
        print(path)
        print(bot.utterances)
    """
   BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://www.cleverbot.com/', 'tab2url': {'15': 'https://www.cleverbot.com/'}}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[1]/div/div/form/input', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[1]/div/div/form/input', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '1cf6a574-e314-4adc-8dc6-4206d4fd6a56'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[1]/div[2]/div[1]/div/div/form/input', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '434c3fa1-e945-48ac-b7cf-623249bd7295'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'hello', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '434c3fa1-e945-48ac-b7cf-623249bd7295'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '5c23bd63-56ca-432c-8a6a-4009523990d4'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'How is it going?', 'href': None, 'element_id': 'df2ff9ce-1132-4a88-a873-13d1bf43764f'}
   """

    # Manual session handling
    bot = Cleverbot(exec_path)
    try:
        bot.new_session()
        bot.ask("hello")
        bot.ask("hello")
        bot.ask("hello")
        bot.ask("hello")
        print(bot.utterances)

        bot.save_screenshot("sess1.png")

        bot.new_session()

        bot.ask("hello")
        bot.ask("hello")
        print(bot.utterances)

        bot.save_screenshot("sess2.png")
    except Exception as e: # timeout and such
        print(e)

    # ensure stop is called or a firefox process will be left running!
    bot.stop()
