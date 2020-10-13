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

    geckodriver = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    # Using context manager
    with Cleverbot(geckodriver) as bot:
        answer = bot.ask("hello")
        answer = bot.ask("are you a bot")
        answer = bot.ask("what is love")
        answer = bot.ask("are you stupid")
        answer = bot.ask("are you alive")
        answer = bot.ask("does god exist")
        answer = bot.ask("who created evil")
        answer = bot.ask("are you religious")
        answer = bot.ask("what is your favorite food")
        path = bot.save_screenshot("cleverbot.png")
        print(bot.utterances)
    """
BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'homepage': 'https://www.cleverbot.com/'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[1]/div/div/form/input', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[1]/div/div/form/input', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '390ee818-5241-4cfd-b3d7-9c33a0b5ce0a'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[1]/div[2]/div[1]/div/div/form/input', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'hello', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': 'a92aca2c-0f9e-4fe7-afef-9aa514a087d6'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'How are you?', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'are you a bot', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '883a0f52-b4ab-4277-be34-22ac2df2c4fb'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': "No. I'm a human.", 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'what is love', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '42e40996-ea2c-4f65-936c-6d58a5fd743e'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'Love is a feeling that comes when you meet someone.', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'are you stupid', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '5cc6e355-99f6-4008-8ece-6e34b81b42c0'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'No. Make a friends:).', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'are you alive', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': 'e4565759-6ce5-4f69-8640-c705d480127d'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'Of course.', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'does god exist', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '1fc1ec17-055f-47aa-a426-52d067ca2bae'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'Yes He does.', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'who created evil', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': 'b9ad6dd6-65d9-4836-a34e-a06bedfb1163'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'Whoever created the earth.', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'are you religious', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '83389449-f605-46a5-92ae-038cf0724e4a'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': 'Yes a little.', 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SEND_KEYS {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'keys': 'what is your favorite food', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'timeout': 10, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': '', 'element_id': '69253a15-867b-43d6-b463-d18ad99369e8'}
BrowserEvents.ELEMENT_SUBMIT {'xpath': '/html/body/div[1]/div[2]/div[3]/form/input[1]', 'element_text': '', 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'href': ''}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '//*[@id="snipTextIcon"]', 'timeout': 30, 'tab_id': '15', 'url': 'https://www.cleverbot.com/', 'element_text': '', 'href': None, 'element_id': '454906ec-1556-4aa7-a1f4-a65713c5495f'}
BrowserEvents.SEARCH_XPATH {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[1]/div[2]/div[3]/p[9]/span[1]', 'tab_id': '15', 'filter': None, 'url': 'https://www.cleverbot.com/', 'element_text': "I don't really have one...", 'href': None, 'element_id': '2cf2de4b-9688-460f-8e48-6b260425cab0'}
BrowserEvents.SCREENSHOT {'image': 'cleverbot.png', 'tab_id': '15', 'url': 'https://www.cleverbot.com/'}
BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://www.cleverbot.com/', 'tab2url': {'15': 'https://www.cleverbot.com/'}}
  """
