from os.path import join, dirname
from time import sleep
from pybrowser import PyBrowser

exec_path = join(dirname(__file__), "geckodriver")
# https://github.com/mozilla/geckodriver/releases

# Using context manager
with PyBrowser(exec_path, headless=False) as browser:
    print(browser.open_tabs)
    print(browser.current_tab_id)
    print(browser.current_url)
    browser.open_new_tab("https://www.hellochatterbox.net")

    sleep(10)
    print(browser.current_url)
    print(browser.open_tabs)
    print(browser.current_tab_id)

    browser.switch_to_tab("https://liberapay.com/jarbasAI/")
    print(browser.current_url)
    print(browser.open_tabs)
    print(browser.current_tab_id)
    sleep(10)
