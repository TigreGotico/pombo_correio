from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import os
from os.path import join, dirname, exists
from tempfile import gettempdir
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pombo_correio.exceptions import NoSession, ElementNotFound, \
    FireFoxCrashed, InvalidElement, InvalidTabID, TorNotFound, DriverNotSet, \
    PreferencesFileNotFound, PreferencesParseError, TabDiscarded
from enum import IntEnum
from xdg import XDG_DATA_HOME
import json
from time import sleep
from pombo_correio.utils import Keys


class BrowserEvents(IntEnum):
    BROWSER_OPEN = 0
    WARMING_UP = 1
    EXTENSION_LOADED = 2
    EXTENSIONS_ALL_LOADED = 3
    WEBPAGE_OPEN = 10
    OPEN_URL = 11
    NEW_TAB = 12
    SWITCH_TAB = 20
    TAB_CLOSED = 25
    SEARCH_CSS = 30
    SEARCH_XPATH = 31
    WAIT_FOR_CSS = 40
    WAIT_FOR_XPATH = 41
    CSS_FOUND = 50
    XPATH_FOUND = 51
    CSS_NOT_FOUND = 60
    XPATH_NOT_FOUND = 61
    ELEMENT_CLICKED = 70
    ELEMENT_SEND_KEYS = 71
    ELEMENT_SUBMIT = 72
    SCREENSHOT = 80
    BROWSER_CLOSED = 100


class PyBrowser:
    def __init__(self, headless=False,
                 homepage="https://liberapay.com/jarbasAI/",
                 debug=True):
        self.options = Options()
        if headless:
            self.options.headless = True
        self._driver = None
        self.homepage = homepage
        self.event_handlers = {}
        self.tab_elements = {}
        self._tab2url = {}
        self.debug = debug

    # event handling
    def add_event_handler(self, event, handler):
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)

    def handle_event(self, event, data):
        if self.debug:
            print(event, data)
        if event not in self.event_handlers:
            return
        for handler in self.event_handlers[event]:
            try:
                handler(data)
            except Exception as e:
                print("ERROR: exception in event handler")
                print(str(e))

    # browser properties
    def _sync_tab2url(self):
        if not self._driver:
            return self._tab2url
        current = self.current_tab_id
        switched = False
        self._tab2url = {}
        for tab in self.open_tabs:
            try:
                if tab != current:
                    switched = True
                    self.switch_to_tab(tab)
                self._tab2url[tab] = self.current_url
            except:
                pass
        if switched:
            self.switch_to_tab(current)
        return self._tab2url

    @property
    def tab2url(self):
        return self._tab2url

    @property
    def current_url(self):
        if not self._driver:
            return None
        try:
            return self._driver.current_url
        except NoSuchWindowException:
            raise TabDiscarded

    @property
    def open_tabs(self):
        if not self._driver:
            return []
        try:
            return self._driver.window_handles
        except NoSuchWindowException:
            raise TabDiscarded

    @property
    def current_tab_id(self):
        if not self._driver:
            return None
        try:
            return self._driver.current_window_handle
        except NoSuchWindowException:
            raise TabDiscarded

    # webpage elements
    def _validate_element(self, element, idx=0):
        if not element:
            raise ElementNotFound
        # lookup xpath/css reference
        if isinstance(element, str):
            tab_id = self.current_tab_id
            if tab_id in self.tab_elements:
                if element in self.tab_elements[tab_id]:
                    elements = self.tab_elements[tab_id][element]
                    if len(elements) < idx + 1:
                        raise InvalidElement
                    element = elements[idx]
                else:
                    raise InvalidElement
            else:
                raise InvalidElement
        return element

    def get_element_attribute(self, element, attr):
        element = self._validate_element(element)
        return element.get_attribute(attr)

    def click_element(self, element, event_data=None):
        element = self._validate_element(element)

        # TODO type check for element and exception
        event_data = event_data or {}
        event_data["element_text"] = element.text
        event_data["tab_id"] = self.current_tab_id
        event_data["url"] = self.current_url
        href = element.get_attribute("href") or element.get_attribute("src")
        event_data["href"] = href
        element.click()
        self.handle_event(BrowserEvents.ELEMENT_CLICKED, event_data)

    def send_keys_element(self, keys, element, event_data=None):
        element = self._validate_element(element)
        event_data = event_data or {}
        event_data["keys"] = keys
        event_data["element_text"] = element.text
        event_data["tab_id"] = self.current_tab_id
        event_data["url"] = self.current_url
        href = element.get_attribute("href") or element.get_attribute("src")
        event_data["href"] = href
        element.send_keys(keys)
        self.handle_event(BrowserEvents.ELEMENT_SEND_KEYS, event_data)

    def submit_element(self, element, event_data=None):
        element = self._validate_element(element)
        event_data = event_data or {}
        event_data["element_text"] = element.text
        event_data["tab_id"] = self.current_tab_id
        event_data["url"] = self.current_url
        href = element.get_attribute("href") or element.get_attribute("src")
        event_data["href"] = href
        element.submit()
        self.handle_event(BrowserEvents.ELEMENT_SUBMIT, event_data)

    def clear_elements(self, tab_id=None):
        if tab_id:
            if tab_id in self.tab_elements:
                self.tab_elements.pop(tab_id)
            else:
                raise InvalidTabID
        else:
            self.tab_elements = {}

    def _cache_element(self, element, element_id):
        if element:
            if self.current_tab_id not in self.tab_elements:
                self.tab_elements[self.current_tab_id] = {}
            if element_id in self.tab_elements[self.current_tab_id]:
                self.tab_elements[self.current_tab_id][element_id].append(
                    element)
            else:
                self.tab_elements[self.current_tab_id][element_id] = [element]

    # element search
    def search_xpath(self, xpath, source_element=None, filter=None):
        event_data = {"xpath": xpath,
                      "tab_id": self.current_tab_id,
                      "filter": filter,
                      "url": self.current_url}

        if source_element is None:
            source_element = self._driver
        else:
            source_element = self._validate_element(source_element)
            event_data["source_element"] = source_element.id

        self.handle_event(BrowserEvents.SEARCH_XPATH, event_data)

        found = False
        for element in source_element.find_elements_by_xpath(xpath):
            skip = False

            if not filter:
                pass
            elif isinstance(filter, str):
                # contains attribute
                if not self.get_element_attribute(element, filter):
                    skip = True
            elif isinstance(filter, list):
                # contains all attributes
                if not all([self.get_element_attribute(element, f) for f in
                            filter]):
                    skip = True
            elif isinstance(filter, dict):
                for k in filter:
                    if isinstance(filter[k], str):
                        # requite attribute value
                        if self.get_element_attribute(
                                element, k) != filter[k]:
                            skip = True
                    elif isinstance(filter[k], list):
                        # requite attribute value in value list
                        if self.get_element_attribute(
                                element, k) not in filter[k]:
                            skip = True
                    else:
                        raise ValueError

            if skip:
                continue
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or \
                   element.get_attribute("src")
            event_data["href"] = href
            event_data["element_id"] = element.id
            self.handle_event(BrowserEvents.XPATH_FOUND, event_data)

            self._cache_element(element, xpath)
            yield element
            found = True

        if not found:
            self.handle_event(BrowserEvents.XPATH_NOT_FOUND, event_data)

    def search_css(self, css_selector, source_element=None, filter=None):
        event_data = {"css_selector": css_selector,
                      "tab_id": self.current_tab_id,
                      "filter": filter,
                      "url": self.current_url}

        if source_element is None:
            source_element = self._driver
        else:
            source_element = self._validate_element(source_element)
            event_data["source_element"] = source_element.id

        self.handle_event(BrowserEvents.SEARCH_CSS, event_data)

        found = False
        for element in source_element.find_elements_by_css_selector(
                css_selector):
            skip = False

            if not filter:
                pass
            elif isinstance(filter, str):
                # contains attribute
                if not self.get_element_attribute(element, filter):
                    skip = True
            elif isinstance(filter, list):
                # contains all attributes
                if not all([self.get_element_attribute(element, f) for f in
                            filter]):
                    skip = True
            elif isinstance(filter, dict):
                for k in filter:
                    if isinstance(filter[k], str):
                        # requite attribute value
                        if self.get_element_attribute(
                                element, k) != filter[k]:
                            skip = True
                    elif isinstance(filter[k], list):
                        # requite attribute value in value list
                        if self.get_element_attribute(
                                element, k) not in filter[k]:
                            skip = True
                    else:
                        raise ValueError

            if skip:
                continue
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or \
                   element.get_attribute("src")
            event_data["href"] = href
            event_data["element_id"] = element.id
            self.handle_event(BrowserEvents.CSS_FOUND, event_data)

            self._cache_element(element, css_selector)
            yield element
            found = True

        if not found:
            self.handle_event(BrowserEvents.CSS_NOT_FOUND, event_data)

    # element selection
    def get_xpath(self, xpath, timeout=10, wait=False):
        if self._driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        if wait:
            return self.wait_for_xpath(xpath, timeout)
        for elem in self.search_xpath(xpath):
            return elem

    def get_css_selector(self, css_selector, timeout=10, wait=False):
        if self._driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        if wait:
            return self.wait_for_css_selector(css_selector, timeout)
        for element in self.search_css(css_selector):
            return element

    def wait_for_xpath(self, xpath, timeout=30):
        if self._driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession

        event_data = {"xpath": xpath,
                      "timeout": timeout,
                      "tab_id": self.current_tab_id,
                      "url": self.current_url}
        self.handle_event(BrowserEvents.WAIT_FOR_XPATH, event_data)

        try:
            element = WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(
                    (By.XPATH, xpath)))
        except Exception as e:
            element = None

        if element:
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or element.get_attribute(
                "src")
            event_data["href"] = href
            event_data["element_id"] = element.id
            self.handle_event(BrowserEvents.XPATH_FOUND, event_data)
        else:
            self.handle_event(BrowserEvents.XPATH_NOT_FOUND, event_data)

        self._cache_element(element, xpath)
        return element

    def wait_for_css_selector(self, css_selector, timeout=30):
        if self._driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession

        event_data = {"css_selector": css_selector, "timeout": timeout,
                      "tab_id": self.current_tab_id, "url": self.current_url}
        self.handle_event(BrowserEvents.WAIT_FOR_CSS, event_data)

        try:
            element = WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, css_selector)))
        except Exception as e:
            element = None

        if element:
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or element.get_attribute(
                "src")
            event_data["href"] = href
            event_data["element_id"] = element.id
            self.handle_event(BrowserEvents.CSS_FOUND, event_data)
        else:
            self.handle_event(BrowserEvents.CSS_NOT_FOUND, event_data)
        self._cache_element(element, css_selector)
        return element

    # action chains
    def find_and_click_xpath(self, xpath, timeout=10, wait=True):
        if wait:
            element = self.wait_for_xpath(xpath, timeout)
        else:
            element = self.get_xpath(xpath)
        self.click_element(element, {"xpath": xpath})

    def find_and_click_css_selector(self, css_selector, timeout=10, wait=True):
        if wait:
            element = self.wait_for_css_selector(css_selector, timeout)
        else:
            element = self.get_css_selector(css_selector)
        self.click_element(element, {"css_selector": css_selector})

    def find_and_send_keys_xpath(self, keys, xpath, timeout=10, wait=True):
        if wait:
            element = self.wait_for_xpath(xpath, timeout)
        else:
            element = self.get_xpath(xpath)
        self.send_keys_element(keys, element, {"xpath": xpath})

    def find_and_send_keys_selector(self, keys, css_selector, timeout=10,
                                    wait=True):
        if wait:
            element = self.wait_for_css_selector(css_selector, timeout)
        else:
            element = self.get_css_selector(css_selector)
        self.send_keys_element(keys, element, {"css_selector": css_selector})

    def find_and_submit_xpath(self, xpath, timeout=10, wait=True):
        if wait:
            element = self.wait_for_xpath(xpath, timeout)
        else:
            element = self.get_xpath(xpath)
        self.submit_element(element, {"xpath": xpath})

    def find_and_submit_css_selector(self, css_selector, timeout=10,
                                     wait=True):
        if wait:
            element = self.wait_for_css_selector(css_selector, timeout)
        else:
            element = self.get_css_selector(css_selector)
        self.submit_element(element, {"css_selector": css_selector})

    # browser interaction
    def scroll_down(self, times=1):
        # move to bottom
        element = self._driver.find_element_by_tag_name('body')
        keys = [Keys.ARROW_DOWN] * times
        self.send_keys_element(keys, element)

    def create_driver(self):
        if self._driver is None:
            raise DriverNotSet

    def new_session(self):
        self.stop()
        self.create_driver()

        extensions = self.load_extensions()

        self._driver.get(self.homepage)

        self._driver.maximize_window()
        sleep(2)
        event_data = {"open_tabs": self.open_tabs,
                      "tab_id": self.current_tab_id,
                      "homepage": self.homepage}
        self.handle_event(BrowserEvents.BROWSER_OPEN, event_data)
        self._sync_tab2url()

    def load_extensions(self):
        return []

    def close_extensions_tabs(self):
        pass

    def open_new_tab(self, url, switch=True):
        self._driver.execute_script(
            '''window.open("{url}","_blank");'''.format(url=url))
        tab = self.open_tabs[-1]

        event_data = {"new_url": url,
                      "new_tab_id": tab}
        self.handle_event(BrowserEvents.NEW_TAB, event_data)

        if switch:
            self.switch_to_tab(tab)

        self._sync_tab2url()
        return tab

    def switch_to_tab(self, tab_id):
        if not self._driver:
            raise NoSession
        event_data = {"open_tabs": self.open_tabs,
                      "old_tab": self.current_tab_id,
                      "old_url": self.current_url,
                      "tab_id": tab_id}
        self._driver.switch_to.window(window_name=tab_id)
        self.handle_event(BrowserEvents.SWITCH_TAB, event_data)

    def got_to_url(self, url, tab_id=None):
        if tab_id:
            self.switch_to_tab(tab_id)
        else:
            tab_id = self.current_tab_id
        event_data = {"url": url,
                      "old_url": self.current_url,
                      "tab_id": tab_id}
        self._driver.get(url)
        self.handle_event(BrowserEvents.OPEN_URL, event_data)
        self._sync_tab2url()

    def close_tab(self, tab_id=None):

        if not tab_id:
            # close the active tab
            self._driver.close()
            tab_id = self.current_tab_id
        else:
            self.switch_to_tab(tab_id)
            self._driver.close()

        if tab_id in self.tab_elements:
            self.tab_elements.pop(tab_id)
        event_data = {"open_tabs": self.open_tabs,
                      "current_url": self.current_url,
                      "tab_id": self.current_tab_id,
                      "closed_tab": tab_id,
                      "tab2url": self.tab2url}

        self.handle_event(BrowserEvents.TAB_CLOSED, event_data)

        self._sync_tab2url()

    def save_screenshot(self, path=None):
        path = path or join(gettempdir(), "pybrowser_screenshot.png")
        self._driver.save_screenshot(path)

        event_data = {"image": path,
                      "tab_id": self.current_tab_id,
                      "url": self.current_url}
        self.handle_event(BrowserEvents.SCREENSHOT, event_data)

        return path

    def stop(self):
        self.clear_elements()
        if self._driver is not None:
            event_data = {"open_tabs": self.open_tabs,
                          "tab_id": self.current_tab_id,
                          "current_url": self.current_url,
                          "tab2url": self.tab2url}

            self._driver.quit()

            self.handle_event(BrowserEvents.BROWSER_CLOSED, event_data)
        self._driver = None
        self._tab2url = {}

    # context manager
    def __enter__(self):
        self.new_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class FirefoxBrowser(PyBrowser):
    def __init__(self, geckodriver=None, headless=False,
                 homepage="https://liberapay.com/jarbasAI/",
                 debug=True, binary=None, prefs_js=None,
                 extensions_folder=None):
        super().__init__(headless, homepage, debug)
        self.geckodriver = geckodriver
        if binary:
            self.firefox_binary = FirefoxBinary(binary)
        else:
            self.firefox_binary = None

        if prefs_js:
            self.preferences = self.parse_prefsjs(prefs_js)
        else:
            self.preferences = {}

        self.firefox_profile = self.create_firefox_profile()
        self.extensions_folder = extensions_folder

    @staticmethod
    def find_firefox():
        """ look for firefox binary """
        paths = ["/usr/bin/firefox"]
        binaries = []
        for p in paths:
            if exists(p):
                binaries.append(p)
        return binaries

    @staticmethod
    def parse_prefsjs(path):
        if not exists(path):
            raise PreferencesFileNotFound
        with open(path) as f:
            json_str = "{\n"
            for p in f.read().split("\n"):
                try:
                    if not p.strip() or p.startswith("//"):
                        continue
                    k, val = p.split('user_pref("')[1].split('", ')
                    val = val.split(");")[0]
                    json_str += '"{key}": {val},'.format(key=k, val=val)
                except:
                    raise PreferencesParseError
            json_str = json_str[:-1] + "\n}"
            prefs = json.loads(json_str)
        return prefs

    def create_firefox_profile(self):
        profile = FirefoxProfile()
        for pref in self.preferences:
            profile.set_preference(pref, self.preferences[pref])
        return profile

    def create_driver(self):
        if self.geckodriver:
            self.driver = webdriver.Firefox(
                executable_path=self.geckodriver,
                firefox_profile=self.firefox_profile,
                options=self.options)
        else:
            self.driver = webdriver.Firefox(
                firefox_profile=self.firefox_profile,
                options=self.options)

    def load_extensions(self):
        if self.extensions_folder and exists(self.extensions_folder):
            extensions = os.listdir(self.extensions_folder)
            for extension in extensions:
                self.driver.install_addon(
                    join(self.extensions_folder, extension), temporary=True)
                event_data = {"extension": extension}
                self.handle_event(BrowserEvents.EXTENSION_LOADED,
                                  event_data)

            event_data = {"extensions": extensions}
            self.handle_event(BrowserEvents.EXTENSIONS_ALL_LOADED, event_data)
            return extensions
        return []

    def close_extensions_tabs(self):
        self._sync_tab2url()
        for tab in self.tab2url:
            if self.tab2url[tab].startswith("moz-extension://"):
                self.close_tab(tab)


class PrivacyFoxBrowser(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=False,
                 homepage="https://liberapay.com/jarbasAI/",
                 debug=True, binary=None, prefs_js=None,
                 extensions_folder=None):
        prefs_js = prefs_js or join(dirname(__file__), "res", "prefs.js")
        extensions_folder = extensions_folder or \
                            join(dirname(__file__), "res", "extensions")
        super().__init__(geckodriver, headless, homepage, debug, binary,
                         prefs_js, extensions_folder)


class TorBrowser(FirefoxBrowser):
    def __init__(self, geckodriver=None, headless=False,
                 homepage="https://check.torproject.org/",
                 debug=True, binary=None, prefs_js=None,
                 extensions_folder=None, torrc='/etc/tor/',
                 js_enabled=False, images_enabled=True):

        self.javascript_enabled = js_enabled
        self.images_enabled = images_enabled
        self.torrc = torrc

        if not binary:
            binary = self.find_tor_browser()
            if not len(binary):
                raise TorNotFound
            binary = binary[0]

        if not exists(binary):
            raise TorNotFound

        super().__init__(geckodriver, headless, homepage, debug, binary,
                         prefs_js, extensions_folder)

    @staticmethod
    def find_tor_browser():
        """ look for tor browser binary """
        binaries = []
        tor_xdg = join(XDG_DATA_HOME, "torbrowser/tbb/")
        for base, folders, files in os.walk(tor_xdg):
            if "firefox" in files:
                binaries.append(join(base, "firefox"))
        return binaries

    def create_tor_profile(self):
        profile = FirefoxProfile(self.torrc)
        # set some privacy settings by default
        profile.set_preference("places.history.enabled", False)
        profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        profile.set_preference("privacy.clearOnShutdown.passwords", True)
        profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
        profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        profile.set_preference("signon.rememberSignons", False)
        profile.set_preference("network.cookie.lifetimePolicy", 2)
        profile.set_preference("network.dns.disablePrefetch", True)
        profile.set_preference("network.http.sendRefererHeader", 0)

        # set socks proxy
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks_version", 5)
        profile.set_preference("network.proxy.socks", '127.0.0.1')
        profile.set_preference("network.proxy.socks_port", 9050)
        profile.set_preference("network.proxy.socks_remote_dns", True)

        # user defined preferences
        for pref in self.preferences:
            profile.set_preference(pref, self.preferences[pref])

        # if you're really hardcore about your security
        # js can be used to reveal your true i.p.
        profile.set_preference("javascript.enabled", self.javascript_enabled)

        # get a huge speed increase by not downloading images
        if not self.images_enabled:
            profile.set_preference("permissions.default.image", 2)

        return profile

    def create_firefox_profile(self):
        return self.create_tor_profile()
