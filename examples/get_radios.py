import time
from typing import Iterable, Tuple, Optional, Dict

import requests
from json_database import JsonStorageXDG

from pombo_correio import FirefoxBrowser


class Scraper(FirefoxBrowser):
    N_PER_PAGE = 62
    N_PAGES = 5

    def __init__(self, name, homepage, geckodriver=None, headless=True, extensions_folder=None):
        super().__init__(geckodriver=geckodriver,
                         headless=headless,
                         homepage=homepage,
                         extensions_folder=extensions_folder)
        self.radios = JsonStorageXDG(name, subfolder="radios_online")

    @property
    def db_path(self) -> str:
        return self.radios.path

    def index_radios(self, force=False, start_page=1):
        if not len(self.radios) or force or start_page > 1:
            print("Indexing all radio stations")
            for name, img, radio_page in self._iter_radio_pages(start_page):
                self.radios[radio_page] = {
                    "name": name,
                    "image": img,
                    "url": radio_page
                }
                self.radios.store()

    def extract_radio_stream(self, url: str) -> Optional[str]:
        if url in self.radios and self.radios[url].get("stream", ""):
            return self.radios[url]["stream"]
        print(f"Extracting stream: {url}")
        self.goto_url(url)
        button = self.wait_for_css_selector("#play_pause_button")
        action = self.get_element_attribute(button, "onclick")
        try:
            self.click_element(button)
        except:
            time.sleep(1)
            self.click_element(button)
        time.sleep(1)
        if "openPopUp" in action:
            for r in self.iterate_requests():
                if "/embed/" in r.url:
                    self.radios[r.url] = self.radios[url]
                    self.radios.store()
                    print("   Parsing PopUp")
                    return self.extract_radio_stream(r.url)
            else:
                return None
        candidates = []
        history = []
        for request in self.iterate_requests():
            history.append(request)
            if request.url.endswith(".m3u8") or request.url.split("?")[0].endswith(".m3u8"):
                candidates.append(request.url)
            if "audio" not in request.headers.get("Accept", ""):
                continue
            if request.url.startswith('https://playerservices.streamtheworld.com/api/'):
                continue
            self.radios[url]["stream"] = request.url
            self.radios.store()
            return request.url

        for u in candidates:
            self.radios[url]["stream"] = u
            self.radios.store()
            return u

        # TODO
        print("ERROR: failed to extract stream", history)

    def _iter_radio_pages(self, start_page=1) -> Iterable[Tuple[str, str, str]]:
        for p in range(start_page, self.N_PAGES):
            print(f"Parsing page {p}")
            self.goto_url(self.homepage + f"/?page={p}")
            for i in range(1, self.N_PER_PAGE):
                try:
                    picture = self.wait_for_css_selector(
                        f"#radio_list_li_{i} > a:nth-child(1) > div:nth-child(1) > img:nth-child(1)",
                        timeout=2 if i > 1 else 10)
                    img = self.get_element_attribute(picture, "src")
                    name = self.get_element_attribute(picture, "alt")
                    entry = self.wait_for_css_selector(f"#radio_list_li_{i} > a:nth-child(1)")
                    radio_page = self.get_element_attribute(entry, "href")
                    yield name, img, radio_page
                except:
                    continue

    def iter_radios(self, check_status: bool = False) -> Iterable[Tuple[str, Dict]]:
        self.index_radios()
        for url, data in dict(self.radios).items():
            try:
                stream = self.extract_radio_stream(url)
                data["stream"] = stream
                if check_status:
                    try:
                        r = requests.head(stream)
                        data["status"] = r.status_code
                    except Exception as e:
                        data["status"] = "UNVERIFIED"
                else:
                    data["status"] = "UNVERIFIED"
                yield url, data
            except Exception as e:
                print("EXCEPTION: failed to extract", e, url)
                continue


class RadiosOnlinePT(Scraper):
    N_PAGES = 13

    def __init__(self, geckodriver=None, headless=True, extensions_folder=None):
        super().__init__(geckodriver=geckodriver,
                         headless=headless,
                         name="radios_pt",
                         homepage="https://www.radios-online.pt",
                         extensions_folder=extensions_folder)


class RadiosOnlineBR(Scraper):
    N_PAGES = 94

    def __init__(self, geckodriver=None, headless=True, extensions_folder=None):
        super().__init__(geckodriver=geckodriver,
                         headless=headless,
                         name="radios_br",
                         homepage="https://www.radio-ao-vivo.com",
                         extensions_folder=extensions_folder)


class RadiosOnlineES(Scraper):
    N_PAGES = 42

    def __init__(self, geckodriver=None, headless=True, extensions_folder=None):
        super().__init__(geckodriver=geckodriver,
                         headless=headless,
                         name="radios_es",
                         homepage="https://www.radio-espana.es",
                         extensions_folder=extensions_folder)


if __name__ == "__main__":

    with RadiosOnlinePT(headless=True) as bot:
        print(bot.db_path, print(len(bot.radios)))
        for url, data in bot.iter_radios(check_status=False):
            print(data)
    exit(1)
    with RadiosOnlineES(headless=True) as bot:
        print(bot.db_path, print(len(bot.radios)))
        for url, data in bot.iter_radios(check_status=False):
            print(data)


    with RadiosOnlineBR(headless=True) as bot:
        print(bot.db_path, print(len(bot.radios)))
        for url, data in bot.iter_radios(check_status=False):
            print(data)



