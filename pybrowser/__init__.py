from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from os.path import join, dirname
from tempfile import gettempdir
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pybrowser.exceptions import NoSession


class PyBrowser:
    def __init__(self, exec_path=None, headless=False,
                 homepage="https://liberapay.com/jarbasAI/"):
        self.options = Options()
        if headless:
            self.options.headless = True
        self.exec_path = exec_path
        self.driver = None
        self.homepage = homepage

    def new_session(self):
        self.stop()
        if self.exec_path:
            self.driver = webdriver.Firefox(executable_path=self.exec_path,
                                            options=self.options)
        else:
            self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(self.homepage)

    @property
    def tab2url(self):
        tab2url = {}
        current = self.current_tab_id
        for tab in self.open_tabs:
            self.switch_to_tab(tab)
            tab2url[tab] = self.current_url
        self.switch_to_tab(current)
        return tab2url

    @property
    def current_url(self):
        if not self.driver:
            return None
        return self.driver.current_url

    @property
    def open_tabs(self):
        if not self.driver:
            return None
        return self.driver.window_handles

    @property
    def current_tab_id(self):
        if not self.driver:
            return None
        return self.driver.current_window_handle

    def open_new_tab(self, url, switch=True):
        self.driver.execute_script(
            '''window.open("{url}","_blank");'''.format(url=url))
        tab = self.open_tabs[-1]
        if switch:
            self.switch_to_tab(tab)
        return tab

    def switch_to_tab(self, tab_id):
        if not self.driver:
            raise NoSession
        self.driver.switch_to.window(window_name=tab_id)

    def close_tab(self, tab_id=None):
        if not tab_id:
            # close the active tab
            self.driver.close()
        else:
            self.switch_to_tab(tab_id)
            self.driver.close()

    def wait_for_xpath(self, xpath, timeout=30):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        element = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(
            (By.XPATH, xpath)))
        return element

    def get_xpath(self, xpath, timeout=10, wait=False):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        if wait:
            return self.wait_for_xpath(xpath, timeout)
        element = self.driver.find_element_by_xpath(xpath)
        return element

    def wait_for_css_selector(self, css_selector, timeout=30):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        element = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, css_selector)))
        return element

    def get_css_selector(self, css_selector, timeout=10, wait=False):
        if self.driver is None:
            print("[ERROR] please call new_session() first")
            raise NoSession
        if wait:
            return self.wait_for_css_selector(css_selector, timeout)
        element = self.driver.find_element_by_css_selector(css_selector)
        return element

    def save_screenshot(self, path=None):
        path = path or join(gettempdir(), "pybrowesr_screenshot.png")
        self.driver.save_screenshot(path)
        return path

    def stop(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def __enter__(self):
        self.new_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

