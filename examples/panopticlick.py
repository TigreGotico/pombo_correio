from os.path import join, dirname
from time import sleep
from pombo_correio import FirefoxBrowser, PrivacyFoxBrowser, TorBrowser

# https://github.com/mozilla/geckodriver/releases
geckodriver = join(dirname(__file__), "geckodriver")


def panopticlick(browser, name="test"):
    browser.find_and_click_css_selector("#kcarterlink")
    full_results_link = browser.wait_for_css_selector(
        "#showFingerprintLink2", timeout=60)
    sleep(6)  # loading time  (TODO add an implicit wait for some element)
    browser.scroll_down(5)
    sleep(1)
    browser.save_screenshot("panopticlick_{name}.png".format(name=name))
    browser.click_element(full_results_link)
    browser.wait_for_xpath('//*[@id="results"]')

    # scroll for screenshot
    browser.scroll_down(5)
    sleep(1)

    browser.save_screenshot("panopticlick_full_{name}.png".format(name=name))


with FirefoxBrowser(geckodriver, headless=True,
                    homepage="https://panopticlick.eff.org/") as browser:
    panopticlick(browser, name="firefox")

with PrivacyFoxBrowser(geckodriver, headless=True,
                       homepage="https://panopticlick.eff.org/") as browser:
    panopticlick(browser, name="privacyfox")

with TorBrowser(geckodriver, headless=True,
                homepage="https://panopticlick.eff.org/") as browser:
    panopticlick(browser, name="tor")
