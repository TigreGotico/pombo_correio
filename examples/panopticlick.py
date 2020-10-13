from os.path import join, dirname
from time import sleep
from pombo_correio import FirefoxBrowser

# https://github.com/mozilla/geckodriver/releases
geckodriver = join(dirname(__file__), "geckodriver")

# suggestion, create at https://ffprofile.com
prefs = join(dirname(__file__), "prefs.js")

extensions_folder = join(dirname(__file__), "extensions")

# Using context manager
with FirefoxBrowser(geckodriver, headless=True, prefs_js=prefs,
                    extensions_folder=extensions_folder,
                    homepage="https://panopticlick.eff.org/") as browser:

    browser.find_and_click_css_selector("#kcarterlink")
    full_results_link = browser.wait_for_css_selector(
        "#showFingerprintLink2", timeout=60)
    sleep(5)  # loading time  (TODO add an implicit wait for some element)

    browser.save_screenshot("panopticlick.png")
    browser.click_element(full_results_link)
    browser.wait_for_xpath('//*[@id="results"]')

    # scroll for screenshot
    browser.scroll_down(5)

    browser.save_screenshot("panopticlick_full.png")
