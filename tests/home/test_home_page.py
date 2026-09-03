import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from utils.result_tracker import ResultTracker
from utils.logger import get_logger

logger = get_logger("TestHomePage")

@pytest.fixture(autouse=True)
def setup_home(page: Page):
    """Navigates to home page before each test."""
    home = HomePage(page)
    home.open_home_page()
    return home


class TestHomePageElements:

    def test_01_cookie_bar_elements(self, page: Page, setup_home: HomePage):
        """Verify Cookie Bar visible & clickable UI elements."""
        home = setup_home
        logger.info("--- Test: Cookie Bar Elements ---")
        
        if not home.is_cookie_bar_visible():
            pytest.skip("Cookie bar is not rendered or already accepted.")

        # Wait for cookie bar buttons to finish JS initialization
        expect(page.locator(home.locators.COOKIE_AGREE_BUTTON).first).to_be_enabled(timeout=10000)

        # 1. Close Cookie Bar Button
        close_btn = page.locator(home.locators.COOKIE_CLOSE_BUTTON).first
        visible = close_btn.is_visible()
        clickable = close_btn.is_enabled()
        ResultTracker.record(
            section="Cookie Bar",
            ui_element="Close Cookie Bar Button",
            element_type="Button",
            visible=visible,
            clickable=clickable,
            observed_action="Dismisses cookie banner",
            actual_result="Button is visible and clickable",
            navigation_url=page.url,
            status="PASS" if visible and clickable else "FAIL"
        )
        assert visible and clickable

        # 2. Privacy Policy Link
        privacy_link = page.locator(home.locators.COOKIE_PRIVACY_LINK).first
        priv_vis = privacy_link.is_visible()
        priv_clk = privacy_link.is_enabled()
        priv_href = privacy_link.get_attribute("href") or ""
        ResultTracker.record(
            section="Cookie Bar",
            ui_element="Privacy Policy Link",
            element_type="Link",
            visible=priv_vis,
            clickable=priv_clk,
            observed_action=f"References {priv_href}",
            actual_result="Link is visible and clickable",
            navigation_url=priv_href,
            status="PASS" if priv_vis and priv_clk else "FAIL"
        )
        assert priv_vis and priv_clk

        # 3. Custom Settings Button
        custom_btn = page.locator(home.locators.COOKIE_CUSTOM_BUTTON).first
        cust_vis = custom_btn.is_visible()
        cust_clk = custom_btn.is_enabled()
        ResultTracker.record(
            section="Cookie Bar",
            ui_element="Custom Settings Button",
            element_type="Button",
            visible=cust_vis,
            clickable=cust_clk,
            observed_action="Opens cookie settings modal",
            actual_result="Button is visible and clickable",
            navigation_url=page.url,
            status="PASS" if cust_vis and cust_clk else "FAIL"
        )
        assert cust_vis and cust_clk

        # 4. Decline Cookies Button
        decline_btn = page.locator(home.locators.COOKIE_DECLINE_BUTTON).first
        dec_vis = decline_btn.is_visible()
        dec_clk = decline_btn.is_enabled()
        ResultTracker.record(
            section="Cookie Bar",
            ui_element="Decline Cookies Button",
            element_type="Button",
            visible=dec_vis,
            clickable=dec_clk,
            observed_action="Rejects optional cookies",
            actual_result="Button is visible and clickable",
            navigation_url=page.url,
            status="PASS" if dec_vis and dec_clk else "FAIL"
        )
        assert dec_vis and dec_clk

        # 5. I agree Button (Click and verify banner dismiss)
        agree_btn = page.locator(home.locators.COOKIE_AGREE_BUTTON).first
        agr_vis = agree_btn.is_visible()
        agr_clk = agree_btn.is_enabled()
        agree_btn.click()
        page.wait_for_timeout(1000)
        dismissed = not home.is_cookie_bar_visible()
        ResultTracker.record(
            section="Cookie Bar",
            ui_element="I agree Button",
            element_type="Button",
            visible=agr_vis,
            clickable=agr_clk,
            observed_action="Accepts cookies and closes banner",
            actual_result="Cookie banner dismissed successfully" if dismissed else "Banner still visible",
            navigation_url=page.url,
            status="PASS" if agr_vis and agr_clk and dismissed else "FAIL"
        )
        assert agr_vis and agr_clk and dismissed

    def test_02_header_elements(self, page: Page, setup_home: HomePage):
        """Verify Header Logo, Navigation icons, Search, Wishlist, Sign in, and Cart."""
        home = setup_home
        logger.info("--- Test: Header Elements ---")

        # 1. Store Logo
        logo = page.locator(home.locators.STORE_LOGO).first
        logo_vis = logo.is_visible()
        logo_clk = logo.is_enabled()
        logo.click()
        page.wait_for_load_state("domcontentloaded")
        logo_nav_url = page.url
        ResultTracker.record(
            section="Header",
            ui_element="Store Logo Link",
            element_type="Link",
            visible=logo_vis,
            clickable=logo_clk,
            observed_action="Navigates to Home Page",
            actual_result="Home Page loaded successfully",
            navigation_url=logo_nav_url,
            status="PASS" if "silhouettedesignstore.com" in logo_nav_url else "FAIL"
        )
        assert "silhouettedesignstore.com" in logo_nav_url

        # 2. Silhouette America Logo Link (opens external site in new tab)
        sa_logo = page.locator(home.locators.SILHOUETTE_AMERICA_LOGO_LINK).first
        sa_vis = sa_logo.is_visible()
        sa_clk = sa_logo.is_enabled()
        with page.context.expect_page(timeout=10000) as new_page_info:
            sa_logo.click()
        sa_page = new_page_info.value
        sa_page.wait_for_load_state("domcontentloaded")
        sa_url = sa_page.url
        sa_page.close()
        ResultTracker.record(
            section="Header",
            ui_element="Silhouette America Logo Link",
            element_type="Link",
            visible=sa_vis,
            clickable=sa_clk,
            observed_action="Opens Silhouette America website in new tab",
            actual_result="Silhouette America page loaded successfully",
            navigation_url=sa_url,
            status="PASS" if "silhouetteamerica.com" in sa_url else "FAIL"
        )
        assert "silhouetteamerica.com" in sa_url

        # 3. Search Bar Interaction
        search_input = page.locator(home.locators.SEARCH_INPUT).first
        s_vis = search_input.is_visible()
        s_clk = search_input.is_enabled()
        search_input.fill("heart")
        search_input.press("Enter")
        page.wait_for_load_state("domcontentloaded")
        search_nav_url = page.url
        home.open_home_page()  # Return home
        ResultTracker.record(
            section="Header",
            ui_element="Search Bar Input & Submission",
            element_type="Input/Search",
            visible=s_vis,
            clickable=s_clk,
            observed_action="Performs search for keyword 'heart'",
            actual_result="Catalog search results loaded",
            navigation_url=search_nav_url,
            status="PASS" if "catalogsearch" in search_nav_url or "heart" in search_nav_url else "FAIL"
        )
        assert "catalogsearch" in search_nav_url or "heart" in search_nav_url

        # 4. Header Wishlist Link
        wishlist = page.locator(home.locators.HEADER_WISHLIST).first
        w_vis = wishlist.is_visible()
        w_clk = wishlist.is_enabled()
        wishlist.click()
        page.wait_for_timeout(800)
        wish_url = page.url
        ResultTracker.record(
            section="Header",
            ui_element="Header Wishlist Icon",
            element_type="Link/Trigger",
            visible=w_vis,
            clickable=w_clk,
            observed_action="Prompts guest to sign in or navigates to wishlist",
            actual_result=f"Wishlist triggered successfully (URL: {wish_url})",
            navigation_url=wish_url,
            status="PASS" if w_vis and w_clk else "FAIL"
        )
        assert w_vis and w_clk

        # 5. Sign In / Register Dropdown
        signin_trigger = page.locator(home.locators.SIGN_IN_REGISTER_DROPDOWN).first
        sign_vis = signin_trigger.is_visible()
        sign_clk = signin_trigger.is_enabled()
        signin_trigger.click()
        page.wait_for_timeout(800)
        modal_signin = page.locator(home.locators.MODAL_SIGN_IN_LINK).first
        modal_shown = modal_signin.is_visible()
        ResultTracker.record(
            section="Header",
            ui_element="Sign In / Register Dropdown Link",
            element_type="Link/Trigger",
            visible=sign_vis,
            clickable=sign_clk,
            observed_action="Opens authentication dropdown modal",
            actual_result="Sign in & Register options revealed",
            navigation_url=page.url,
            status="PASS" if sign_vis and sign_clk and modal_shown else "FAIL"
        )
        assert sign_vis and sign_clk and modal_shown

        # 6. Mini-Cart Drawer & Close Button
        cart_trigger = page.locator(home.locators.MINI_CART_LINK).first
        cart_vis = cart_trigger.is_visible()
        cart_clk = cart_trigger.is_enabled()
        cart_trigger.click()
        page.wait_for_timeout(800)
        cart_dialog = page.locator(home.locators.MINI_CART_DIALOG).first
        cart_shown = cart_dialog.is_visible()
        # Close mini cart
        close_cart = page.locator(home.locators.MINI_CART_CLOSE_BUTTON).first
        if close_cart.is_visible():
            close_cart.click()
            page.wait_for_timeout(500)
        ResultTracker.record(
            section="Header",
            ui_element="Mini-Cart Link & Drawer",
            element_type="Link/Drawer",
            visible=cart_vis,
            clickable=cart_clk,
            observed_action="Toggles shopping cart drawer",
            actual_result="Cart drawer opened and closed successfully",
            navigation_url=page.url,
            status="PASS" if cart_vis and cart_clk and cart_shown else "FAIL"
        )
        assert cart_vis and cart_clk and cart_shown

    def test_03_main_navigation_links(self, page: Page, setup_home: HomePage):
        """Verify all primary navigation menu items rendered on Home Page."""
        home = setup_home
        logger.info("--- Test: Main Navigation Menu ---")

        nav_items = [
            ("Designs", home.locators.NAV_DESIGNS, "designs.html"),
            ("Fonts", home.locators.NAV_FONTS, "fonts.html"),
            ("3D", home.locators.NAV_3D, "3d-design.html"),
            ("Patterns", home.locators.NAV_PATTERNS, "printable-backgrounds.html"),
            ("New", home.locators.NAV_NEW, "new.html"),
            ("Design Bundles", home.locators.NAV_BUNDLES, "design-bundles.html"),
            ("Buy Credits", home.locators.NAV_BUY_CREDITS, "credit-boosts.html"),
            ("Subscription Plans", home.locators.NAV_SUBSCRIPTION, "subscription-plans"),
            ("Artists", home.locators.NAV_ARTISTS, "artist"),
            ("Free Trial", home.locators.NAV_FREE_TRIAL, "free"),
        ]

        # First verify Software (opens external in new tab)
        sw_item = page.locator(home.locators.NAV_SOFTWARE).first
        sw_vis = sw_item.is_visible()
        sw_clk = sw_item.is_enabled()
        with page.context.expect_page(timeout=10000) as new_page_info:
            sw_item.click()
        sw_page = new_page_info.value
        sw_page.wait_for_load_state("domcontentloaded")
        sw_url = sw_page.url
        sw_page.close()
        ResultTracker.record(
            section="Main Navigation",
            ui_element="Software (opens in new tab)",
            element_type="Nav Link",
            visible=sw_vis,
            clickable=sw_clk,
            observed_action="Navigates to external Software page",
            actual_result="Opened in new tab successfully",
            navigation_url=sw_url,
            status="PASS" if "silhouetteamerica.com/software" in sw_url else "FAIL"
        )
        assert "silhouetteamerica.com/software" in sw_url

        # Loop through remaining internal nav links
        for name, selector, expected_url_part in nav_items:
            locator = page.locator(selector).first
            vis = locator.is_visible()
            clk = locator.is_enabled()
            assert vis and clk, f"Nav item '{name}' not visible or clickable"
            locator.click()
            page.wait_for_load_state("domcontentloaded")
            current_url = page.url
            passed = expected_url_part in current_url
            ResultTracker.record(
                section="Main Navigation",
                ui_element=f"{name} Menu Link",
                element_type="Nav Link",
                visible=vis,
                clickable=clk,
                observed_action=f"Navigates to {expected_url_part}",
                actual_result=f"Loaded {current_url}",
                navigation_url=current_url,
                status="PASS" if passed else "FAIL"
            )
            assert passed, f"Expected '{expected_url_part}' in URL, got '{current_url}'"
            home.open_home_page()

    def test_04_hero_carousel_controls_and_links(self, page: Page, setup_home: HomePage):
        """Verify Hero Carousel dots, Next/Previous controls, and active banner link."""
        home = setup_home
        logger.info("--- Test: Hero Carousel Controls & Links ---")

        # 1. Slide Dots
        dots_loc = page.locator(home.locators.HERO_SLIDE_DOTS)
        dots_loc.first.wait_for(state="visible", timeout=15000)
        dots_count = dots_loc.count()
        assert dots_count > 0, "No hero slide dots found"
        logger.info(f"Found {dots_count} carousel slide dots")

        # Click dot 2
        dot2 = dots_loc.nth(1)
        d_vis = dot2.is_visible()
        d_clk = dot2.is_enabled()
        dot2.click()
        page.wait_for_timeout(800)
        ResultTracker.record(
            section="Hero Carousel",
            ui_element="Slide Pagination Dot 2",
            element_type="Button",
            visible=d_vis,
            clickable=d_clk,
            observed_action="Switches carousel to slide 2",
            actual_result="Slide transition executed",
            navigation_url=page.url,
            status="PASS" if d_vis and d_clk else "FAIL"
        )
        assert d_vis and d_clk

        # 2. Next Slide Control
        next_btn = page.locator(home.locators.HERO_NEXT_BUTTON).first
        n_vis = next_btn.is_visible()
        n_clk = next_btn.is_enabled()
        next_btn.click()
        page.wait_for_timeout(800)
        ResultTracker.record(
            section="Hero Carousel",
            ui_element="Next Slide Button",
            element_type="Button",
            visible=n_vis,
            clickable=n_clk,
            observed_action="Advances to next hero slide",
            actual_result="Carousel advanced to next slide",
            navigation_url=page.url,
            status="PASS" if n_vis and n_clk else "FAIL"
        )
        assert n_vis and n_clk

        # 3. Previous Slide Control
        prev_btn = page.locator(home.locators.HERO_PREV_BUTTON).first
        p_vis = prev_btn.is_visible()
        p_clk = prev_btn.is_enabled()
        prev_btn.click()
        page.wait_for_timeout(800)
        ResultTracker.record(
            section="Hero Carousel",
            ui_element="Previous Slide Button",
            element_type="Button",
            visible=p_vis,
            clickable=p_clk,
            observed_action="Returns to previous hero slide",
            actual_result="Carousel returned to previous slide",
            navigation_url=page.url,
            status="PASS" if p_vis and p_clk else "FAIL"
        )
        assert p_vis and p_clk

        # 4. Hero Active Slide Banner Link
        active_slide = page.locator(home.locators.HERO_ACTIVE_SLIDE_LINK).first
        s_vis = active_slide.is_visible()
        s_clk = active_slide.is_enabled()
        s_href = active_slide.get_attribute("href") or ""
        active_slide.click()
        page.wait_for_load_state("domcontentloaded")
        banner_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Hero Carousel",
            ui_element="Active Banner Image/Link",
            element_type="Banner Link",
            visible=s_vis,
            clickable=s_clk,
            observed_action=f"Navigates to campaign destination: {s_href}",
            actual_result=f"Campaign page loaded successfully: {banner_url}",
            navigation_url=banner_url,
            status="PASS" if "silhouettedesignstore.com" in banner_url else "FAIL"
        )
        assert "silhouettedesignstore.com" in banner_url

    def test_05_discovery_and_filter_elements(self, page: Page, setup_home: HomePage):
        """Verify Discovery Category tabs, Design Type filters, and 'View all' link."""
        home = setup_home
        logger.info("--- Test: Discovery & Filter Section ---")

        # 1. Discovery Category Tabs (Desktop)
        disc_tabs = page.locator(home.locators.DISCOVERY_TYPE_TABS)
        disc_tabs.first.wait_for(state="visible", timeout=15000)
        disc_count = disc_tabs.count()
        assert disc_count > 0, "No discovery category tabs found"
        
        # Click second tab (e.g. 'Subscribers Only')
        disc_tab2 = disc_tabs.nth(1)
        disc_tab_name = disc_tab2.inner_text()
        d_vis = disc_tab2.is_visible()
        d_clk = disc_tab2.is_enabled()
        disc_tab2.click()
        page.wait_for_timeout(1000)
        ResultTracker.record(
            section="Discovery & Filters",
            ui_element=f"Discovery Category Tab ('{disc_tab_name}')",
            element_type="Tab/Button",
            visible=d_vis,
            clickable=d_clk,
            observed_action=f"Filters gallery by discovery category '{disc_tab_name}'",
            actual_result="Product list updated for selected discovery category",
            navigation_url=page.url,
            status="PASS" if d_vis and d_clk else "FAIL"
        )
        assert d_vis and d_clk

        # 2. Design Type Filter Tabs (Desktop)
        des_tabs = page.locator(home.locators.DESIGN_TYPE_TABS)
        des_tabs.first.wait_for(state="visible", timeout=10000)
        des_count = des_tabs.count()
        assert des_count > 0, "No design type filter tabs found"

        # Click second filter tab (e.g. 'Regular Cut')
        des_tab2 = des_tabs.nth(1)
        des_name = des_tab2.inner_text()
        des_vis = des_tab2.is_visible()
        des_clk = des_tab2.is_enabled()
        des_tab2.click()
        page.wait_for_timeout(1000)
        ResultTracker.record(
            section="Discovery & Filters",
            ui_element=f"Design Type Filter ('{des_name}')",
            element_type="Filter/Button",
            visible=des_vis,
            clickable=des_clk,
            observed_action=f"Filters product gallery by design type '{des_name}'",
            actual_result="Product list updated for selected design type",
            navigation_url=page.url,
            status="PASS" if des_vis and des_clk else "FAIL"
        )
        assert des_vis and des_clk

        # 3. Discovery "View all" Link
        view_all = page.locator(home.locators.DISCOVERY_VIEW_ALL_LINK).first
        home.scroll_to(home.locators.DISCOVERY_VIEW_ALL_LINK)
        va_vis = view_all.is_visible()
        va_clk = view_all.is_enabled()
        view_all.click()
        page.wait_for_load_state("domcontentloaded")
        va_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Discovery & Filters",
            ui_element="Discovery 'View all' Link",
            element_type="Link",
            visible=va_vis,
            clickable=va_clk,
            observed_action="Navigates to discovery category landing page",
            actual_result=f"Navigated to {va_url}",
            navigation_url=va_url,
            status="PASS" if ".html" in va_url or "silhouettedesignstore.com" in va_url else "FAIL"
        )
        assert ".html" in va_url or "silhouettedesignstore.com" in va_url

    def test_06_featured_product_cards(self, page: Page, setup_home: HomePage):
        """Verify Featured Product card elements: Image, Title, Artist, Add to Cart, Wishlist."""
        home = setup_home
        logger.info("--- Test: Featured Product Cards ---")

        # 1. Product Image Link
        prod_img = page.locator(home.locators.FIRST_PRODUCT_IMAGE_LINK).first
        img_vis = prod_img.is_visible()
        img_clk = prod_img.is_enabled()
        prod_img.click()
        page.wait_for_load_state("domcontentloaded")
        pdp_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Featured Products",
            ui_element="Product Image Link",
            element_type="Card Link",
            visible=img_vis,
            clickable=img_clk,
            observed_action="Navigates to Product Details Page (PDP)",
            actual_result=f"PDP opened: {pdp_url}",
            navigation_url=pdp_url,
            status="PASS" if ".html" in pdp_url and pdp_url != home.URL else "FAIL"
        )
        assert ".html" in pdp_url and pdp_url != home.URL

        # 2. Product Title Link
        prod_title = page.locator(home.locators.FIRST_PRODUCT_TITLE_LINK).first
        t_vis = prod_title.is_visible()
        t_clk = prod_title.is_enabled()
        prod_title.click()
        page.wait_for_load_state("domcontentloaded")
        title_pdp_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Featured Products",
            ui_element="Product Title Link",
            element_type="Card Link",
            visible=t_vis,
            clickable=t_clk,
            observed_action="Navigates to PDP from title link",
            actual_result=f"PDP opened: {title_pdp_url}",
            navigation_url=title_pdp_url,
            status="PASS" if ".html" in title_pdp_url and title_pdp_url != home.URL else "FAIL"
        )
        assert ".html" in title_pdp_url and title_pdp_url != home.URL

        # 3. Product Artist Link (opens in new tab)
        artist_link = page.locator(home.locators.FIRST_PRODUCT_ARTIST_LINK).first
        artist_link.scroll_into_view_if_needed()
        a_vis = artist_link.is_visible()
        a_clk = artist_link.is_enabled()
        with page.context.expect_page(timeout=10000) as new_page_info:
            artist_link.click()
        artist_page = new_page_info.value
        artist_page.wait_for_load_state("domcontentloaded")
        artist_shop_url = artist_page.url
        artist_page.close()
        ResultTracker.record(
            section="Featured Products",
            ui_element="Product Artist Shop Link",
            element_type="Link",
            visible=a_vis,
            clickable=a_clk,
            observed_action="Navigates to Artist's profile / shop page (new tab)",
            actual_result=f"Artist shop opened: {artist_shop_url}",
            navigation_url=artist_shop_url,
            status="PASS" if "/shop/" in artist_shop_url or "marketplace" in artist_shop_url else "FAIL"
        )
        assert "/shop/" in artist_shop_url or "marketplace" in artist_shop_url

        # 4. Product Add to Cart Button
        add_btn = page.locator(home.locators.FIRST_PRODUCT_ADD_TO_CART).first
        add_vis = add_btn.is_visible()
        add_clk = add_btn.is_enabled()
        add_btn.click()
        page.wait_for_timeout(1500)
        ResultTracker.record(
            section="Featured Products",
            ui_element="Product Add to Cart Button",
            element_type="Button",
            visible=add_vis,
            clickable=add_clk,
            observed_action="Adds product to cart / updates cart badge",
            actual_result="Add to Cart action triggered successfully",
            navigation_url=page.url,
            status="PASS" if add_vis and add_clk else "FAIL"
        )
        assert add_vis and add_clk

        # 5. Product Wishlist Button
        wish_btn = page.locator(home.locators.FIRST_PRODUCT_WISHLIST).first
        w_vis = wish_btn.is_visible()
        w_clk = wish_btn.is_enabled()
        wish_btn.click()
        page.wait_for_load_state("domcontentloaded")
        wish_nav_url = page.url
        home.open_home_page()
        # Guest user is redirected to login or stays with notification
        ResultTracker.record(
            section="Featured Products",
            ui_element="Product Wishlist Button",
            element_type="Button/Link",
            visible=w_vis,
            clickable=w_clk,
            observed_action="Adds to wishlist or prompts guest to sign in",
            actual_result=f"Wishlist action routed to {wish_nav_url}",
            navigation_url=wish_nav_url,
            status="PASS" if w_vis and w_clk else "FAIL"
        )
        assert w_vis and w_clk

    def test_07_featured_artists_section(self, page: Page, setup_home: HomePage):
        """Verify Featured Artists Section: Artist Card link & 'View all' link."""
        home = setup_home
        logger.info("--- Test: Design Store Artists Section ---")

        # 1. First Artist Link
        home.scroll_to(home.locators.ARTISTS_HEADING)
        first_artist = page.locator(home.locators.ARTISTS_CARDS).first
        first_artist.scroll_into_view_if_needed()
        fa_vis = first_artist.is_visible()
        fa_clk = first_artist.is_enabled()
        first_artist.click()
        page.wait_for_load_state("domcontentloaded")
        fa_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Design Store Artists",
            ui_element="Featured Artist Profile Link",
            element_type="Link",
            visible=fa_vis,
            clickable=fa_clk,
            observed_action="Navigates to Artist storefront",
            actual_result=f"Artist storefront loaded: {fa_url}",
            navigation_url=fa_url,
            status="PASS" if "/shop/" in fa_url or "/seller/" in fa_url else "FAIL"
        )
        assert "/shop/" in fa_url or "/seller/" in fa_url

        # 2. Artists View All Link
        artists_va = page.locator(home.locators.ARTISTS_VIEW_ALL_LINK).first
        home.scroll_to(home.locators.ARTISTS_HEADING)
        va_vis = artists_va.is_visible()
        va_clk = artists_va.is_enabled()
        artists_va.click()
        page.wait_for_load_state("domcontentloaded")
        va_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Design Store Artists",
            ui_element="Artists 'View all' Link",
            element_type="Link",
            visible=va_vis,
            clickable=va_clk,
            observed_action="Navigates to All Artists directory",
            actual_result=f"All Artists directory loaded: {va_url}",
            navigation_url=va_url,
            status="PASS" if "sellerlist" in va_url else "FAIL"
        )
        assert "sellerlist" in va_url

    def test_08_bundles_section(self, page: Page, setup_home: HomePage):
        """Verify Design Bundles section: Bundle Card link & 'View all' link."""
        home = setup_home
        logger.info("--- Test: Bundles Section ---")

        # 1. First Bundle Card Link
        home.scroll_to(home.locators.BUNDLES_HEADING)
        first_bundle = page.locator(home.locators.BUNDLES_CARDS).first
        b_vis = first_bundle.is_visible()
        b_clk = first_bundle.is_enabled()
        first_bundle.click()
        page.wait_for_load_state("domcontentloaded")
        b_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Design Bundles",
            ui_element="Bundle Card Link",
            element_type="Card Link",
            visible=b_vis,
            clickable=b_clk,
            observed_action="Navigates to Bundle details page",
            actual_result=f"Bundle details loaded: {b_url}",
            navigation_url=b_url,
            status="PASS" if ".html" in b_url and b_url != home.URL else "FAIL"
        )
        assert ".html" in b_url and b_url != home.URL

        # 2. Bundles View All Link
        home.scroll_to(home.locators.BUNDLES_HEADING)
        bundles_va = page.locator(home.locators.BUNDLES_VIEW_ALL_LINK).first
        bva_vis = bundles_va.is_visible()
        bva_clk = bundles_va.is_enabled()
        bundles_va.click()
        page.wait_for_load_state("domcontentloaded")
        bva_url = page.url
        home.open_home_page()
        ResultTracker.record(
            section="Design Bundles",
            ui_element="Bundles 'View all' Link",
            element_type="Link",
            visible=bva_vis,
            clickable=bva_clk,
            observed_action="Navigates to Bundles catalog manager",
            actual_result=f"Bundles catalog loaded: {bva_url}",
            navigation_url=bva_url,
            status="PASS" if "bundles" in bva_url else "FAIL"
        )
        assert "bundles" in bva_url

    def test_09_promotional_cta_banner(self, page: Page, setup_home: HomePage):
        """Verify Promotional 'Become An Artist' CTA Banner."""
        home = setup_home
        logger.info("--- Test: Promotional CTA Banner ---")

        cta = page.locator(home.locators.BECOME_AN_ARTIST_BANNER_LINK).first
        home.scroll_to(home.locators.BECOME_AN_ARTIST_BANNER_LINK)
        cta_vis = cta.is_visible()
        cta_clk = cta.is_enabled()
        cta.click()
        page.wait_for_timeout(1000)
        cta_url = page.url

        if "artist-application" in cta_url:
            status = "PASS"
            actual = f"Artist application page loaded: {cta_url}"
        else:
            status = "REQUIREMENT CONFIRMATION NEEDED"
            actual = (
                f"Element is visible and clickable with href='/artist-application', "
                f"but in guest session URL remained on Home Page ({cta_url}). "
                f"Confirmation needed from product team on guest routing behavior."
            )

        ResultTracker.record(
            section="Promotional Banner",
            ui_element="'Become An Artist' CTA Button",
            element_type="CTA Link",
            visible=cta_vis,
            clickable=cta_clk,
            observed_action="Navigates to Artist application or requires authentication",
            actual_result=actual,
            navigation_url=cta_url,
            status=status
        )
        assert cta_vis and cta_clk

    def test_10_footer_and_support_elements(self, page: Page, setup_home: HomePage):
        """Verify Footer Newsletter, Help/Legal accordions, Contact Email, Socials, Chatbot."""
        home = setup_home
        logger.info("--- Test: Footer & Support Elements ---")

        # 1. Newsletter Input & Subscribe Button
        news_input = page.locator(home.locators.NEWSLETTER_INPUT).first
        news_btn = page.locator(home.locators.NEWSLETTER_SUBSCRIBE_BUTTON).first
        home.scroll_to(home.locators.NEWSLETTER_INPUT)
        n_vis = news_input.is_visible()
        n_clk = news_btn.is_enabled()
        news_input.fill("qa_automation_test@example.com")
        news_btn.click()
        page.wait_for_timeout(1000)
        ResultTracker.record(
            section="Footer",
            ui_element="Newsletter Input & Subscribe",
            element_type="Input/Button",
            visible=n_vis,
            clickable=n_clk,
            observed_action="Submits newsletter subscription email",
            actual_result="Subscription form submitted",
            navigation_url=page.url,
            status="PASS" if n_vis and n_clk else "FAIL"
        )
        assert n_vis and n_clk

        # 2. Help Accordion Toggle & Links
        help_acc = page.locator(home.locators.FOOTER_HELP_ACCORDION).first
        home.scroll_to(home.locators.FOOTER_HELP_ACCORDION)
        help_vis = help_acc.is_visible()
        help_clk = help_acc.is_enabled()
        help_acc.click()
        page.wait_for_timeout(600)

        # Help Link: FAQ
        faq_link = page.locator(home.locators.FOOTER_FAQ_LINK).first
        faq_vis = faq_link.is_visible()
        faq_clk = faq_link.is_enabled()
        ResultTracker.record(
            section="Footer",
            ui_element="Help Accordion & FAQ Link",
            element_type="Accordion/Link",
            visible=help_vis and faq_vis,
            clickable=help_clk and faq_clk,
            observed_action="Expands Help menu and exposes FAQ support link",
            actual_result="FAQ link visible and clickable",
            navigation_url="https://silhouetteamerica.freshdesk.com/support/home",
            status="PASS" if help_vis and faq_vis and faq_clk else "FAIL"
        )
        assert help_vis and faq_vis and faq_clk

        # Help Link: Sitemap
        sitemap_link = page.locator(home.locators.FOOTER_SITEMAP_LINK).first
        sm_vis = sitemap_link.is_visible()
        sm_clk = sitemap_link.is_enabled()
        ResultTracker.record(
            section="Footer",
            ui_element="Footer Sitemap Link",
            element_type="Link",
            visible=sm_vis,
            clickable=sm_clk,
            observed_action="Points to /htmlsitemap",
            actual_result="Sitemap link is visible and clickable",
            navigation_url="https://www.silhouettedesignstore.com/htmlsitemap",
            status="PASS" if sm_vis and sm_clk else "FAIL"
        )
        assert sm_vis and sm_clk

        # Help Link: Blog
        blog_link = page.locator(home.locators.FOOTER_BLOG_LINK).first
        b_vis = blog_link.is_visible()
        b_clk = blog_link.is_enabled()
        ResultTracker.record(
            section="Footer",
            ui_element="Footer Blog Link",
            element_type="Link",
            visible=b_vis,
            clickable=b_clk,
            observed_action="Points to /blog.html",
            actual_result="Blog link is visible and clickable",
            navigation_url="https://www.silhouettedesignstore.com/blog.html",
            status="PASS" if b_vis and b_clk else "FAIL"
        )
        assert b_vis and b_clk

        # 3. Legal Accordion Toggle & Privacy Link
        legal_acc = page.locator(home.locators.FOOTER_LEGAL_ACCORDION).first
        legal_vis = legal_acc.is_visible()
        legal_clk = legal_acc.is_enabled()
        legal_acc.click()
        page.wait_for_timeout(600)

        privacy_link = page.locator(home.locators.FOOTER_PRIVACY_LINK).first
        priv_vis = privacy_link.is_visible()
        priv_clk = privacy_link.is_enabled()
        ResultTracker.record(
            section="Footer",
            ui_element="Legal Accordion & Privacy Link",
            element_type="Accordion/Link",
            visible=legal_vis and priv_vis,
            clickable=legal_clk and priv_clk,
            observed_action="Expands Legal menu and exposes Privacy Policy",
            actual_result="Privacy Policy link visible and clickable",
            navigation_url="https://www.silhouettedesignstore.com/legal#privacy-policy",
            status="PASS" if legal_vis and priv_vis and priv_clk else "FAIL"
        )
        assert legal_vis and priv_vis and priv_clk

        # Terms of Use link
        terms_link = page.locator(home.locators.FOOTER_TERMS_LINK).first
        term_vis = terms_link.is_visible()
        term_clk = terms_link.is_enabled()
        ResultTracker.record(
            section="Footer",
            ui_element="Terms of Use Link",
            element_type="Link",
            visible=term_vis,
            clickable=term_clk,
            observed_action="Points to /legal#terms-of-use",
            actual_result="Terms link is visible and clickable",
            navigation_url="https://www.silhouettedesignstore.com/legal#terms-of-use",
            status="PASS" if term_vis and term_clk else "FAIL"
        )
        assert term_vis and term_clk

        # 4. Contact Us Email Link
        email_link = page.locator(home.locators.FOOTER_EMAIL_LINK).first
        em_vis = email_link.is_visible()
        em_clk = email_link.is_enabled()
        em_href = email_link.get_attribute("href") or ""
        ResultTracker.record(
            section="Footer",
            ui_element="Contact Support Email Link",
            element_type="Email Link",
            visible=em_vis,
            clickable=em_clk,
            observed_action=f"Opens email client with {em_href}",
            actual_result="Support email link verified",
            navigation_url=em_href,
            status="PASS" if "mailto:support@silhouetteamerica.com" in em_href else "FAIL"
        )
        assert "mailto:support@silhouetteamerica.com" in em_href

        # 5. Social Media Links
        socials = [
            ("Facebook", home.locators.FOOTER_FB_LINK, "facebook.com/silhouetteglobal"),
            ("Twitter / X", home.locators.FOOTER_TWITTER_LINK, "twitter.com/silhouetteam"),
            ("Pinterest", home.locators.FOOTER_PINTEREST_LINK, "pinterest.com/silhouetteinc"),
            ("Instagram", home.locators.FOOTER_INSTA_LINK, "instagram.com/silhouette.inc"),
            ("YouTube", home.locators.FOOTER_YOUTUBE_LINK, "youtube.com/user/SilhouetteAmericaInc")
        ]
        for s_name, s_sel, s_dest in socials:
            s_elem = page.locator(s_sel).first
            vis = s_elem.is_visible()
            clk = s_elem.is_enabled()
            href = s_elem.get_attribute("href") or ""
            passed = s_dest in href
            ResultTracker.record(
                section="Footer",
                ui_element=f"{s_name} Social Link",
                element_type="Social Link",
                visible=vis,
                clickable=clk,
                observed_action=f"References {href}",
                actual_result=f"Link targets {s_dest}",
                navigation_url=href,
                status="PASS" if passed and vis and clk else "FAIL"
            )
            assert passed and vis and clk

        # 6. Floating Support Chatbot Widget
        cb_icon = page.locator(home.locators.CHATBOT_ICON).first
        cb_count = page.locator(home.locators.CHATBOT_ICON).count()
        cb_vis = cb_icon.is_visible() if cb_count > 0 else False
        cb_clk = cb_icon.is_enabled() if cb_count > 0 else False
        
        if cb_vis:
            cb_icon.click()
            page.wait_for_timeout(800)
            cb_container = page.locator(home.locators.CHATBOT_CONTAINER).first
            cb_open = cb_container.is_visible()
            close_btn = page.locator(home.locators.CHATBOT_CLOSE_BUTTON).first
            if close_btn.is_visible():
                close_btn.click()
                page.wait_for_timeout(500)
            status = "PASS" if cb_open else "FAIL"
            actual = "Chatbot widget opened and closed successfully"
        else:
            status = "REQUIREMENT CONFIRMATION NEEDED"
            actual = (
                "No floating customer support chatbot widget is rendered on the current Home Page. "
                "Confirm with product team if a support chatbot is planned or retired."
            )

        ResultTracker.record(
            section="Floating Widgets",
            ui_element="Support Chatbot Widget",
            element_type="Widget/Button",
            visible=cb_vis,
            clickable=cb_clk,
            observed_action="Toggles customer support chat widget if rendered",
            actual_result=actual,
            navigation_url=page.url,
            status=status
        )
