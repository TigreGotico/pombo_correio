from os.path import join, dirname
from time import sleep
from pybrowser import PyBrowser

exec_path = join(dirname(__file__), "geckodriver")
# https://github.com/mozilla/geckodriver/releases

# Using context manager
with PyBrowser(exec_path, headless=False) as browser:

    assert browser.current_url == browser.homepage
    homepage_id = browser.current_tab_id

    tab_id = browser.open_new_tab("https://github.com/JarbasAl/pybrowser")
    sleep(3)  # allow page load
    assert browser.current_url == "https://github.com/JarbasAl/pybrowser"
    assert browser.current_tab_id == tab_id

    browser.switch_to_tab(homepage_id)
    sleep(3)
    assert browser.current_url == browser.homepage
    assert browser.current_tab_id == homepage_id

    print(browser.open_tabs)
