
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import requests
import time
import re
import sys
from bs4 import BeautifulSoup
DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )

def stealth_page_setup(page):
    """
    Small init script to reduce fingerprinting (hide webdriver and
    provide plausible navigator values).
    """
    page.add_init_script(
        """
        // overwrite the `navigator` properties that commonly reveal automation
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        // fix userAgent for some checks that look for "Headless"
        navigator.__proto__.userAgent = navigator.userAgent.replace('Headless', '');
        """
    )

def fetch_page_and_cookies(url,content,headless=True,timeout_ms=10000):
    """
    Navigate to `url` with Playwright, wait for a selector (if given) or for DOMContentLoaded.
    Returns (html, cookies_list).
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless, args=["--no-sandbox"])
        context = browser.new_context(user_agent=DEFAULT_USER_AGENT)
        selector_to_wait = content 
        page = context.new_page()
        stealth_page_setup(page)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            if selector_to_wait:
                page.wait_for_selector(selector_to_wait, timeout=timeout_ms)
            else:
                time.sleep(1.0)

            html = page.content()
            cookies = context.cookies()
            return html, cookies

        except PlaywrightTimeout as e:
            # fallback: try a longer wait but still avoid networkidle
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms * 2)
                if selector_to_wait:
                    page.wait_for_selector(selector_to_wait, timeout=timeout_ms * 2)
                html = page.content()
                cookies = context.cookies()
                return html, cookies
            except Exception as e2:
                 print(f"An Error occured, Likely the doujin you searched for does not exist\n{e2}")
                 sys.exit(1)
        finally:
            try:
                context.close()
                browser.close()
            except:
                pass

def make_requests_session_from_cookies(cookies):
    """Create requests.Session preloaded with Playwright cookies."""
    s = requests.Session()
    s.headers.update({
        "User-Agent":DEFAULT_USER_AGENT,
        "Referer": "https://nhentai.net/" 
    })
    for c in cookies:
        s.cookies.set(c["name"], c["value"], domain=c.get("domain"))
    return s


def fetch_doujin_src(sauce):
    sauce_link = f"https://nhentai.net/g/{sauce}/1"
    html, cookies = fetch_page_and_cookies(sauce_link,"section#image-container img", headless=True)
    session = make_requests_session_from_cookies(cookies)
    soup = BeautifulSoup(html, "html.parser")
    section = soup.find("section", id="image-container")
    img_tag = section.find("img") if section else None
    if img_tag:
        img_src = img_tag.get("src")

    if img_src.startswith("//"):
        img_srcs = "https:" + img_src
        parts = img_srcs.rsplit("/", 1)        
        src_base = parts[0] + "/"             
        file_type = "." + parts[1].split(".")[1]
        img_file = []
        img_file.append(src_base)
        img_file.append(file_type)
        return img_file
        
def fetch_page_num(sauce):
    sauce_link = f"https://nhentai.net/g/{sauce}/1"
    html, cookies = fetch_page_and_cookies(sauce_link, None,headless=True)
    session = make_requests_session_from_cookies(cookies)
    soup = BeautifulSoup(html, "html.parser")
    num_pages_element = soup.find("span", class_="num-pages")
    if num_pages_element:
        num_pages = int(num_pages_element.text)
        return num_pages
    else:
        return 0

def get_name(sauce):
    sauce_link = f"https://nhentai.net/g/{sauce}/1"
    html, cookies = fetch_page_and_cookies(sauce_link,None, headless=True)
    session = make_requests_session_from_cookies(cookies)
    match = re.search(r"<title>(.*?)»", html)
    if match:
        title = re.sub(r"\s-\s.*$", "", match.group(1).strip())
        return title
    

def get_code(title):
    parsed_title = title.replace(" ", "+")
    parsed_title = "+" + parsed_title
    sauce_link = f"https://nhentai.net/search/?q={parsed_title}"
    html, cookies = fetch_page_and_cookies(sauce_link,None, headless=True)
    session = make_requests_session_from_cookies(cookies)
    soup = BeautifulSoup(html, "html.parser")
    a_tag = soup.find("a", class_="cover")
    if a_tag:
        href = a_tag.get("href")
        sauce_href = re.search(r"/g/(\d+)/", href)
        if sauce_href:
            sauce = sauce_href.group(1)
            print(sauce)
    else:
        print("No doujins by that title")
        sys.exit(0)






