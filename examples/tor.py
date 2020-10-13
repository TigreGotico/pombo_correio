from pombo_correio import TorBrowser

if __name__ == "__main__":
    from os.path import join, dirname, expanduser

    gecko_driver = join(dirname(__file__), "geckodriver")
    # https://github.com/mozilla/geckodriver/releases

    binary = expanduser("~/Downloads/tor-browser_en-US/Browser/firefox")
    # Using context manager
    with TorBrowser(gecko_driver,
                    headless=True,
                    js_enabled=False,
                    binary=binary) as browser:
        url = browser.find_and_click_xpath("/html/body/div[2]/p[2]/a[2]")
        browser.wait_for_xpath("/html/body/div/div[4]/div[2]/h2/span")
        browser.save_screenshot("tor_relay.png")
"""
BrowserEvents.BROWSER_OPEN {'open_tabs': ['15'], 'tab_id': '15', 'homepage': 'https://check.torproject.org/'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div[2]/p[2]/a[2]', 'timeout': 10, 'tab_id': '15', 'url': 'https://check.torproject.org/'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div[2]/p[2]/a[2]', 'timeout': 10, 'tab_id': '15', 'url': 'https://check.torproject.org/', 'element_text': 'Relay Search', 'href': 'https://metrics.torproject.org/rs.html#search/31.220.3.107', 'element_id': '75fa7b6e-fa33-4792-b507-f20b4eebf828'}
BrowserEvents.ELEMENT_CLICKED {'xpath': '/html/body/div[2]/p[2]/a[2]', 'element_text': 'Relay Search', 'tab_id': '15', 'url': 'https://check.torproject.org/', 'href': 'https://metrics.torproject.org/rs.html#search/31.220.3.107'}
BrowserEvents.WAIT_FOR_XPATH {'xpath': '/html/body/div/div[4]/div[2]/h2/span', 'timeout': 30, 'tab_id': '15', 'url': 'https://metrics.torproject.org/rs.html#search/31.220.3.107'}
BrowserEvents.XPATH_FOUND {'xpath': '/html/body/div/div[4]/div[2]/h2/span', 'timeout': 30, 'tab_id': '15', 'url': 'https://metrics.torproject.org/rs.html#search/31.220.3.107', 'element_text': '', 'href': None, 'element_id': '0ccc6fc6-d254-4c59-bebf-e15674a61488'}
BrowserEvents.SCREENSHOT {'image': 'tor_relay.png', 'tab_id': '15', 'url': 'https://metrics.torproject.org/rs.html#details/3BFFFD2035BB388B2FDBF47F2E4BA58DD7AB7942'}
BrowserEvents.BROWSER_CLOSED {'open_tabs': ['15'], 'tab_id': '15', 'current_url': 'https://metrics.torproject.org/rs.html#details/3BFFFD2035BB388B2FDBF47F2E4BA58DD7AB7942', 'tab2url': {'15': 'https://check.torproject.org/'}}
"""