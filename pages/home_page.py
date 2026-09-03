from typing import Optional
from playwright.sync_api import Page
from pages.base_page import BasePage
from locators.home_locators import HomeLocators
from utils.logger import get_logger

logger = get_logger("HomePage")

class HomePage(BasePage):
    URL = "https://www.silhouettedesignstore.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = HomeLocators

    def open_home_page(self):
        logger.info(f"Opening Home Page: {self.URL}")
        self.navigate(self.URL)
        # Ensure body or main is loaded
        self.page.wait_for_selector("header.page-header", timeout=30000)

    # 1. Cookie Bar Actions
    def is_cookie_bar_visible(self) -> bool:
        return self.is_visible(self.locators.COOKIE_BAR, timeout=4000)

    def click_cookie_close(self):
        self.click(self.locators.COOKIE_CLOSE_BUTTON)

    def click_cookie_agree(self):
        self.click(self.locators.COOKIE_AGREE_BUTTON)

    def click_cookie_decline(self):
        self.click(self.locators.COOKIE_DECLINE_BUTTON)

    def click_cookie_custom(self):
        self.click(self.locators.COOKIE_CUSTOM_BUTTON)

    def click_cookie_privacy_link(self):
        self.click(self.locators.COOKIE_PRIVACY_LINK)

    # 2. Header Actions
    def click_logo(self):
        self.click(self.locators.STORE_LOGO)

    def click_silhouette_america(self):
        self.click(self.locators.SILHOUETTE_AMERICA_LOGO_LINK)

    def click_search_toggle(self):
        self.click(self.locators.SEARCH_TOGGLE_BUTTON)

    def fill_search_input(self, text: str):
        self.page.locator(self.locators.SEARCH_INPUT).fill(text)

    def click_search_submit(self):
        self.click(self.locators.SEARCH_SUBMIT_BUTTON)

    def click_header_wishlist(self):
        self.click(self.locators.HEADER_WISHLIST)

    def click_sign_in_register(self):
        self.click(self.locators.SIGN_IN_REGISTER_DROPDOWN)

    def click_mini_cart(self):
        self.click(self.locators.MINI_CART_LINK)

    def close_mini_cart(self):
        self.click(self.locators.MINI_CART_CLOSE_BUTTON)

    # 3. Main Navigation Actions
    def click_nav_item(self, selector: str):
        self.click(selector)

    # 4. Hero Carousel Actions
    def click_hero_dot(self, index: int = 0):
        dots = self.page.locator(self.locators.HERO_SLIDE_DOTS)
        dots.nth(index).click()

    def click_hero_prev(self):
        self.click(self.locators.HERO_PREV_BUTTON)

    def click_hero_next(self):
        self.click(self.locators.HERO_NEXT_BUTTON)

    def click_hero_active_slide(self):
        self.click(self.locators.HERO_ACTIVE_SLIDE_LINK)

    # 5. Discovery & Filters
    def is_discovery_type_visible(self) -> bool:
        return self.is_visible(self.locators.DISCOVERY_TYPE_SELECT)

    def is_design_type_visible(self) -> bool:
        return self.is_visible(self.locators.DESIGN_TYPE_SELECT)

    def click_discovery_view_all(self):
        self.click(self.locators.DISCOVERY_VIEW_ALL_LINK)

    # 6. Featured Products
    def click_first_product_image(self):
        self.click(self.locators.FIRST_PRODUCT_IMAGE_LINK)

    def click_first_product_title(self):
        self.click(self.locators.FIRST_PRODUCT_TITLE_LINK)

    def click_first_product_artist(self):
        self.click(self.locators.FIRST_PRODUCT_ARTIST_LINK)

    def click_first_product_add_to_cart(self):
        self.click(self.locators.FIRST_PRODUCT_ADD_TO_CART)

    def click_first_product_wishlist(self):
        self.click(self.locators.FIRST_PRODUCT_WISHLIST)

    # 7. Design Store Artists
    def click_first_artist(self):
        self.click(self.locators.ARTISTS_CARDS)

    def click_artists_view_all(self):
        self.click(self.locators.ARTISTS_VIEW_ALL_LINK)

    # 8. Bundles Section
    def click_first_bundle(self):
        self.click(self.locators.BUNDLES_CARDS)

    def click_bundles_view_all(self):
        self.click(self.locators.BUNDLES_VIEW_ALL_LINK)

    # 9. Promotional CTA Banner
    def click_become_an_artist_cta(self):
        self.click(self.locators.BECOME_AN_ARTIST_BANNER_LINK)

    # 10. Footer Actions
    def enter_newsletter_email(self, email: str):
        self.page.locator(self.locators.NEWSLETTER_INPUT).fill(email)

    def click_newsletter_subscribe(self):
        self.click(self.locators.NEWSLETTER_SUBSCRIBE_BUTTON)

    def toggle_footer_help(self):
        self.click(self.locators.FOOTER_HELP_ACCORDION)

    def toggle_footer_legal(self):
        self.click(self.locators.FOOTER_LEGAL_ACCORDION)

    def click_footer_faq(self):
        self.click(self.locators.FOOTER_FAQ_LINK)

    def click_footer_become_artist(self):
        self.click(self.locators.FOOTER_BECOME_ARTIST_LINK)

    def click_footer_sitemap(self):
        self.click(self.locators.FOOTER_SITEMAP_LINK)

    def click_footer_blog(self):
        self.click(self.locators.FOOTER_BLOG_LINK)

    def click_footer_privacy(self):
        self.click(self.locators.FOOTER_PRIVACY_LINK)

    def click_footer_terms(self):
        self.click(self.locators.FOOTER_TERMS_LINK)

    def click_footer_policies(self):
        self.click(self.locators.FOOTER_POLICIES_LINK)

    def click_footer_email(self):
        self.click(self.locators.FOOTER_EMAIL_LINK)

    def click_footer_social(self, selector: str):
        self.click(selector)

    # 11. Chatbot Actions
    def toggle_chatbot(self):
        self.click(self.locators.CHATBOT_ICON)

    def close_chatbot(self):
        self.click(self.locators.CHATBOT_CLOSE_BUTTON)
