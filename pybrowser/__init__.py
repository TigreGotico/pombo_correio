from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from os.path import join, dirname
from tempfile import gettempdir
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pybrowser.exceptions import NoSession, ElementNotFound, FireFoxCrashed, \
    InvalidElement, InvalidTabID
from enum import IntEnum


class BrowserEvents(IntEnum):
    BROWSER_OPEN = 0
    WEBPAGE_OPEN = 1
    NEW_TAB = 2
    SWITCH_TAB = 3
    SEARCH_CSS = 4
    SEARCH_XPATH = 5
    WAIT_FOR_CSS = 6
    WAIT_FOR_XPATH = 7
    CSS_FOUND = 8
    CSS_NOT_FOUND = 9
    XPATH_FOUND = 10
    XPATH_NOT_FOUND = 11
    ELEMENT_CLICKED = 12
    ELEMENT_SEND_KEYS = 16
    ELEMENT_SUBMIT = 17
    TAB_CLOSED = 13
    BROWSER_CLOSED = 14
    SCREENSHOT = 15


class PyBrowser:
    def __init__(self, exec_path=None, headless=False,
                 homepage="https://liberapay.com/jarbasAI/",
                 debug=True):
        self.options = Options()
        if headless:
            self.options.headless = True
        self.exec_path = exec_path
        self.driver = None
        self.homepage = homepage
        self.event_handlers = {}
        self.tab_elements = {}
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
    @property
    def tab2url(self):
        tab2url = {}
        if not self.driver:
            return tab2url
        current = self.current_tab_id
        switched = False
        for tab in self.open_tabs:
            if tab != current:
                switched = True
                self.switch_to_tab(tab)
            tab2url[tab] = self.current_url
        if switched:
            self.switch_to_tab(current)
        return tab2url

    @property
    def current_url(self):
        if not self.driver:
            return None
        try:
            return self.driver.current_url
        except NoSuchWindowException:
            raise FireFoxCrashed

    @property
    def open_tabs(self):
        if not self.driver:
            return []
        try:
            return self.driver.window_handles
        except NoSuchWindowException:
            raise FireFoxCrashed

    @property
    def current_tab_id(self):
        if not self.driver:
            return None
        try:
            return self.driver.current_window_handle
        except NoSuchWindowException:
            raise FireFoxCrashed

    # element interaction
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

    # element search
    def _cache_element(self, element, element_id):
        if element:
            if self.current_tab_id not in self.tab_elements:
                self.tab_elements[self.current_tab_id] = {}
            if element_id in self.tab_elements[self.current_tab_id]:
                self.tab_elements[self.current_tab_id][element_id].append(element)
            else:
                self.tab_elements[self.current_tab_id][element_id] = [element]

    def search_xpath(self, xpath):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        for e in self.driver.find_elements_by_xpath(xpath):
            pass

    def search_css_selector(self, css_selector):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        for e in self.driver.find_elements_by_css_selector(css_selector):
            pass

    def get_xpath(self, xpath, timeout=10, wait=False):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        if wait:
            return self.wait_for_xpath(xpath, timeout)

        event_data = {"xpath": xpath,
                      "tab_id": self.current_tab_id,
                      "url": self.current_url}
        self.handle_event(BrowserEvents.SEARCH_XPATH, event_data)

        element = self.driver.find_element_by_xpath(xpath)

        if element:
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or element.get_attribute(
                "src")
            event_data["href"] = href
            self.handle_event(BrowserEvents.XPATH_FOUND, event_data)
        else:
            self.handle_event(BrowserEvents.XPATH_NOT_FOUND, event_data)

        self._cache_element(element, xpath)
        return element

    def get_css_selector(self, css_selector, timeout=10, wait=False):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        if wait:
            return self.wait_for_css_selector(css_selector, timeout)

        event_data = {"css_selector": css_selector,
                      "tab_id": self.current_tab_id,
                      "url": self.current_url}
        self.handle_event(BrowserEvents.SEARCH_CSS, event_data)

        element = self.driver.find_element_by_css_selector(css_selector)

        if element:
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or element.get_attribute(
                "src")
            event_data["href"] = href
            self.handle_event(BrowserEvents.CSS_FOUND, event_data)
        else:
            self.handle_event(BrowserEvents.CSS_NOT_FOUND, event_data)
        self._cache_element(element, css_selector)
        return element

    def wait_for_xpath(self, xpath, timeout=30):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession

        event_data = {"xpath": xpath,
                      "timeout": timeout,
                      "tab_id": self.current_tab_id,
                      "url": self.current_url}
        self.handle_event(BrowserEvents.WAIT_FOR_XPATH, event_data)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(
                    (By.XPATH, xpath)))
        except Exception as e:
            element = None

        if element:
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or element.get_attribute(
                "src")
            event_data["href"] = href
            self.handle_event(BrowserEvents.XPATH_FOUND, event_data)
        else:
            self.handle_event(BrowserEvents.XPATH_NOT_FOUND, event_data)

        self._cache_element(element, xpath)
        return element

    def wait_for_css_selector(self, css_selector, timeout=30):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession

        event_data = {"css_selector": css_selector, "timeout": timeout,
                      "tab_id": self.current_tab_id, "url": self.current_url}
        self.handle_event(BrowserEvents.WAIT_FOR_CSS, event_data)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, css_selector)))
        except Exception as e:
            element = None

        if element:
            event_data["element_text"] = element.text
            href = element.get_attribute("href") or element.get_attribute(
                "src")
            event_data["href"] = href
            self.handle_event(BrowserEvents.CSS_FOUND, event_data)
        else:
            self.handle_event(BrowserEvents.CSS_NOT_FOUND, event_data)
        self._cache_element(element, css_selector)
        return element

    def clear_elements(self, tab_id=None):
        if tab_id:
            if tab_id in self.tab_elements:
                self.tab_elements.pop(tab_id)
            else:
                raise InvalidTabID
        else:
            self.tab_elements = {}

    # browser interaction
    def new_session(self):
        self.stop()
        if self.exec_path:
            self.driver = webdriver.Firefox(executable_path=self.exec_path,
                                            options=self.options)
        else:
            self.driver = webdriver.Firefox(options=self.options)

        self.driver.get(self.homepage)
        event_data = {"open_tabs": self.open_tabs,
                      "current_tab": self.current_tab_id,
                      "current_url": self.current_url,
                      "tab2url": self.tab2url}
        self.handle_event(BrowserEvents.BROWSER_OPEN, event_data)

    def open_new_tab(self, url, switch=True):
        self.driver.execute_script(
            '''window.open("{url}","_blank");'''.format(url=url))
        tab = self.open_tabs[-1]

        event_data = {"new_url": url,
                      "new_tab_id": tab}
        self.handle_event(BrowserEvents.NEW_TAB, event_data)

        if switch:
            self.switch_to_tab(tab)
        return tab

    def switch_to_tab(self, tab_id):
        if not self.driver:
            raise NoSession
        event_data = {"open_tabs": self.open_tabs,
                      "old_tab": self.current_tab_id,
                      "old_url": self.current_url,
                      "current_tab": tab_id}
        self.driver.switch_to.window(window_name=tab_id)
        self.handle_event(BrowserEvents.SWITCH_TAB, event_data)

    def close_tab(self, tab_id=None):

        if not tab_id:
            # close the active tab
            self.driver.close()
            tab_id = self.current_tab_id
        else:
            self.switch_to_tab(tab_id)
            self.driver.close()

        if tab_id in self.tab_elements:
            self.tab_elements.pop(tab_id)
        event_data = {"open_tabs": self.open_tabs,
                      "current_url": self.current_url,
                      "current_tab": self.current_tab_id,
                      "closed_tab": tab_id,
                      "tab2url": self.tab2url}

        self.handle_event(BrowserEvents.TAB_CLOSED, event_data)

        if not len(self.open_tabs):
            self.stop()

    def save_screenshot(self, path=None):
        path = path or join(gettempdir(), "pybrowser_screenshot.png")
        self.driver.save_screenshot(path)

        event_data = {"image": path,
                      "tab_id": self.current_tab_id,
                      "url": self.current_url}
        self.handle_event(BrowserEvents.SCREENSHOT, event_data)

        return path

    def stop(self):
        self.clear_elements()
        if self.driver is not None:
            event_data = {"open_tabs": self.open_tabs,
                          "current_tab": self.current_tab_id,
                          "current_url": self.current_url,
                          "tab2url": self.tab2url}

            self.driver.quit()

            self.handle_event(BrowserEvents.BROWSER_CLOSED, event_data)
        self.driver = None

    # context manager
    def __enter__(self):
        self.new_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
