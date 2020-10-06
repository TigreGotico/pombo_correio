from pybrowser import PyBrowser


class Cleverbot(PyBrowser):
    def __init__(self, exec_path=None, headless=True):
        super().__init__(exec_path, headless, "https://www.cleverbot.com/")
        self.utterances = []

    def new_session(self):
        super().new_session()
        self.utterances = []
        self._accept()

    def _accept(self):
        accept_btn = self.wait_for_xpath(
                                  "/html/body/div[1]/div[2]/div[1]/div/div/form/input")
        accept_btn.click()

    def ask(self, utterance):
        xpath = "/html/body/div[1]/div[2]/div[3]/form/input[1]"
        input = self.wait_for_xpath(xpath)
        input.send_keys(utterance)
        input.submit()
        share_marker = '//*[@id="snipTextIcon"]'
        _ = self.wait_for_xpath(share_marker)
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
    except: # timeout and such
        pass

    # ensure stop is called or a firefox process will be left running!
    bot.stop()
