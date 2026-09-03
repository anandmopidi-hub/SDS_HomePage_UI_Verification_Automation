class HomeLocators:
    """
    Locators for Silhouette Design Store Home Page UI elements.
    Uses stable Playwright locator strategies.
    """

    # 1. Cookie Bar
    COOKIE_BAR = "aside.amgdprjs-bar-template"
    COOKIE_CLOSE_BUTTON = "aside.amgdprjs-bar-template button.action-close"
    COOKIE_PRIVACY_LINK = "aside.amgdprjs-bar-template a[href*='privacy-policy']"
    COOKIE_AGREE_BUTTON = "aside.amgdprjs-bar-template button[data-amgdprcookie-js='accept']"
    COOKIE_CUSTOM_BUTTON = "aside.amgdprjs-bar-template button[data-amgdprcookie-js='settings']"
    COOKIE_DECLINE_BUTTON = "aside.amgdprjs-bar-template button[data-amgdprcookie-js='decline']"

    # 2. Header Elements
    STORE_LOGO = "a.logo-white"
    SILHOUETTE_AMERICA_LOGO_LINK = "a:has-text('Silhouette America')"
    SEARCH_INPUT = "input#search"
    HEADER_WISHLIST = "div.hfavourite a.account-fav"
    SIGN_IN_REGISTER_DROPDOWN = "a.user-link-dropdown.lm"
    MODAL_SIGN_IN_LINK = "a.signin_link"
    MODAL_REGISTER_LINK = "a.blue-link[href*='/customer/account/create/']"
    MINI_CART_LINK = "a.action.showcart"
    MINI_CART_CLOSE_BUTTON = "button#btn-minicart-close, .action.close"
    MINI_CART_DIALOG = "div.block-minicart"

    # 3. Main Navigation Menu
    NAV_SOFTWARE = "nav.menusecmain a[href*='silhouetteamerica.com/software']"
    NAV_DESIGNS = "nav.menusecmain > ul > li > a[href*='/designs.html']"
    NAV_FONTS = "nav.menusecmain > ul > li > a[href*='/fonts.html']"
    NAV_3D = "nav.menusecmain > ul > li > a[href*='/3d-design.html']"
    NAV_PATTERNS = "nav.menusecmain > ul > li > a[href*='/printable-backgrounds.html']"
    NAV_NEW = "nav.menusecmain > ul > li > a[href*='/new.html']"
    NAV_BUNDLES = "nav.menusecmain > ul > li > a[href*='/design-bundles.html']"
    NAV_BUY_CREDITS = "nav.menusecmain > ul > li > a[href*='/credit-boosts.html']"
    NAV_SUBSCRIPTION = "nav.menusecmain > ul > li > a[href*='/subscription-plans']"
    NAV_ARTISTS = "nav.menusecmain > ul > li > a[href*='/artist']"
    NAV_FREE_TRIAL = "a#free-trial-btn, li.freetrial-menu a"

    # 4. Hero Carousel
    HERO_SLIDE_DOTS = ".swiper-pagination-bullet, [aria-label^='Go to slide']"
    HERO_PREV_BUTTON = ".swiper-button-prev, [aria-label='Previous slide']"
    HERO_NEXT_BUTTON = ".swiper-button-next, [aria-label='Next slide']"
    HERO_ACTIVE_SLIDE_LINK = ".swiper-slide-active a, .swiper-slide-visible a, .hero-slider a"

    # 5. Discovery & Filters Section
    DISCOVERY_TYPE_TABS = ".discoverytype-li a, a.discovery-type"
    DESIGN_TYPE_TABS = ".designtype-li a, a.design-type"
    DISCOVERY_VIEW_ALL_LINK = ".filterprosec a:has-text('View all')"

    # 6. Featured Products Section
    PRODUCT_CARDS = "div.product-item-info"
    FIRST_PRODUCT_IMAGE_LINK = "div.product-item-info a[href*='.html']:has(img)"
    FIRST_PRODUCT_TITLE_LINK = "div.product-item-info strong a"
    FIRST_PRODUCT_ARTIST_LINK = "div.product-item-info a[href*='/marketplace/seller/profile/shop/']"
    FIRST_PRODUCT_ADD_TO_CART = "div.product-item-info button.action.tocart"
    FIRST_PRODUCT_WISHLIST = "div.product-item-info a.action.towishlist, div.product-item-info a[href*='/wishlist/index/add/']"

    # 7. Design Store Artists Section
    ARTISTS_HEADING = ".featuredart-sec .hl, .featuredart-sec"
    ARTISTS_CARDS = ".featuredart-sec a[href*='/marketplace/seller/profile/shop/']"
    ARTISTS_VIEW_ALL_LINK = ".featuredart-sec a:has-text('View all'), .featuredart-sec a[href*='/sellerlist']"

    # 8. Bundles Section ("Bundles of Joy for Every Occasion")
    BUNDLES_HEADING = ".custom-container.bundles .heading, .custom-container.bundles"
    BUNDLES_CARDS = ".custom-container.bundles a.product-item-link"
    BUNDLES_VIEW_ALL_LINK = ".custom-container.bundles a:has-text('View all'), .custom-container.bundles a[href*='/bundles-manager.html']"

    # 9. Promotional CTA Banner
    BECOME_AN_ARTIST_BANNER_LINK = "a.register-artist[href*='/artist-application']"

    # 10. Footer Section
    NEWSLETTER_INPUT = "footer.page-footer input#newsletter, footer.page-footer .input-text"
    NEWSLETTER_SUBSCRIBE_BUTTON = "footer.page-footer button.fill-btn, footer.page-footer button.action.subscribe"
    
    FOOTER_HELP_ACCORDION = "footer.page-footer p.label.tm:has-text('Help'), p.label:has-text('Help')"
    FOOTER_FAQ_LINK = "footer.page-footer a[href*='freshdesk.com/support/home']"
    FOOTER_BECOME_ARTIST_LINK = "footer.page-footer a[href*='/register-as-an-artists']"
    FOOTER_SITEMAP_LINK = "footer.page-footer a[href*='/htmlsitemap']"
    FOOTER_BLOG_LINK = "footer.page-footer a[href*='/blog.html']"

    FOOTER_LEGAL_ACCORDION = "footer.page-footer p.label.tm:has-text('Legal'), p.label:has-text('Legal')"
    FOOTER_PRIVACY_LINK = "footer.page-footer a[href*='/legal#privacy-policy']"
    FOOTER_TERMS_LINK = "footer.page-footer a[href*='/legal#terms-of-use']"
    FOOTER_POLICIES_LINK = "footer.page-footer a[href*='/legal']:has-text('Policies')"

    FOOTER_EMAIL_LINK = "footer.page-footer a[href^='mailto:support@silhouetteamerica.com']"
    FOOTER_FB_LINK = "footer.page-footer a.fb, footer.page-footer a[href*='facebook.com']"
    FOOTER_TWITTER_LINK = "footer.page-footer a.twt, footer.page-footer a.tw, footer.page-footer a[href*='twitter.com']"
    FOOTER_PINTEREST_LINK = "footer.page-footer a.pinterest, footer.page-footer a.pi, footer.page-footer a[href*='pinterest.com']"
    FOOTER_INSTA_LINK = "footer.page-footer a.insta, footer.page-footer a[href*='instagram.com']"
    FOOTER_YOUTUBE_LINK = "footer.page-footer a.youtube, footer.page-footer a.ytube, footer.page-footer a[href*='youtube.com']"

    # 11. Floating Chatbot Widget (if rendered)
    CHATBOT_ICON = "div.chatbot-icon, #chat-widget-container, iframe[title*='chat' i]"
    CHATBOT_CONTAINER = "div.chatbot-container, .chat-widget-window"
    CHATBOT_CLOSE_BUTTON = "div.chatbot-header .close-btn, button[aria-label*='Close' i]"
