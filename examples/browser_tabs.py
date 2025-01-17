from os.path import join, dirname
from time import sleep
from pombo_correio import FirefoxBrowser

geckodriver = join(dirname(__file__), "geckodriver")
# https://github.com/mozilla/geckodriver/releases

# Using context manager
with FirefoxBrowser(geckodriver, headless=False) as browser:

    assert browser.current_url == browser.homepage
    homepage_id = browser.current_tab_id

    tab_id = browser.open_new_tab("https://github.com/JarbasAl/pombo_correio")
    sleep(3)  # allow page load
    assert browser.current_url == "https://github.com/JarbasAl/pombo_correio"
    assert browser.current_tab_id == tab_id

    browser.switch_to_tab(homepage_id)
    sleep(3)
    assert browser.current_url == browser.homepage
    assert browser.current_tab_id == homepage_id

    print(browser.open_tabs)
    """
BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'homepage': 'https://liberapay.com/jarbasAI/'}
BrowserEvents.NEW_TAB {'new_url': 'https://github.com/JarbasAl/pombo_correio', 'new_tab_id': '2147483649'}
BrowserEvents.SWITCH_TAB {'open_tabs': ['15', '2147483649'], 'old_tab': '15', 'old_url': 'https://liberapay.com/jarbasAI/', 'tab_id': '2147483649'}
BrowserEvents.SWITCH_TAB {'open_tabs': ['15', '2147483649'], 'old_tab': '2147483649', 'old_url': 'about:blank', 'tab_id': '15'}
BrowserEvents.SWITCH_TAB {'open_tabs': ['15', '2147483649'], 'old_tab': '15', 'old_url': 'https://liberapay.com/jarbasAI/', 'tab_id': '2147483649'}
BrowserEvents.SWITCH_TAB {'open_tabs': ['15', '2147483649'], 'old_tab': '2147483649', 'old_url': 'https://github.com/JarbasAl/pombo_correio', 'tab_id': '15'}
BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15', '2147483649'], 'tab_id': '15', 'current_url': 'https://liberapay.com/jarbasAI/', 'tab2url': {'15': 'https://liberapay.com/jarbasAI/', '2147483649': 'https://liberapay.com/jarbasAI/'}}
    """
