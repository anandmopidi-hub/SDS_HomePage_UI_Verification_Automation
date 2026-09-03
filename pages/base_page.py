from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from utils.logger import get_logger

logger = get_logger("BasePage")

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def wait_for_visible(self, selector: str, timeout: int = 15000) -> Locator:
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        try:
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            return locator.is_visible()
        except Exception:
            return False

    def is_clickable(self, selector: str, timeout: int = 5000) -> bool:
        try:
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            return locator.is_enabled()
        except Exception:
            return False

    def click(self, selector: str, timeout: int = 15000):
        logger.info(f"Clicking element: {selector}")
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=timeout)
        locator.scroll_into_view_if_needed(timeout=timeout)
        locator.click(timeout=timeout)

    def scroll_to(self, selector: str):
        locator = self.page.locator(selector).first
        locator.scroll_into_view_if_needed()

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_url_contains(self, pattern: str, timeout: int = 15000) -> bool:
        try:
            self.page.wait_for_url(lambda u: pattern in u, timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"Timeout waiting for URL pattern '{pattern}': {e}")
            return False
