import os
import time
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.screenshot_manager import ScreenshotManager
from utils.result_tracker import ResultTracker
from utils.report_generator import ReportGenerator
from utils.logger import get_logger

logger = get_logger("Conftest")

TEST_METADATA = {
    "test_01_cookie_bar_elements": {
        "test_id": "TC_HOME_001",
        "section": "Cookie Consent",
        "test_case": "Cookie Bar Verification",
        "observation": "Verified 5 cookie bar elements (Close button, Privacy link, Custom settings, Decline cookies, I agree)"
    },
    "test_02_header_elements": {
        "test_id": "TC_HOME_002",
        "section": "Header",
        "test_case": "Header Verification",
        "observation": "Verified 6 header elements (Store Logo, Silhouette America link, Search Enter submission, Wishlist prompt, Sign In dropdown, Mini-cart drawer)"
    },
    "test_03_main_navigation_links": {
        "test_id": "TC_HOME_003",
        "section": "Main Navigation",
        "test_case": "Navigation Verification",
        "observation": "Verified all 11 main menu links (Software, Designs, Fonts, 3D, Patterns, New, Bundles, Buy Credits, Subscription Plans, Artists, Free Trial)"
    },
    "test_04_hero_carousel_controls_and_links": {
        "test_id": "TC_HOME_004",
        "section": "Hero Carousel",
        "test_case": "Hero Carousel Verification",
        "observation": "Verified Swiper pagination bullets, prev/next navigation arrows, and active slide promotion link"
    },
    "test_05_discovery_and_filter_elements": {
        "test_id": "TC_HOME_005",
        "section": "Discovery & Filters",
        "test_case": "Discovery & Category Filters",
        "observation": "Verified horizontal category tabs, vertical design type filters, and discovery View all catalog link"
    },
    "test_06_featured_product_cards": {
        "test_id": "TC_HOME_006",
        "section": "Featured Products",
        "test_case": "Product Cards Verification",
        "observation": "Verified 5 product card components (Image PDP link, Title PDP link, Artist shop link in new tab, Add to Cart, Wishlist)"
    },
    "test_07_featured_artists_section": {
        "test_id": "TC_HOME_007",
        "section": "Design Store Artists",
        "test_case": "Artists Section Verification",
        "observation": "Verified featured artist storefront link and View all artists directory link"
    },
    "test_08_bundles_section": {
        "test_id": "TC_HOME_008",
        "section": "Design Bundles",
        "test_case": "Bundles Section Verification",
        "observation": "Verified featured bundle card link and View all bundles directory link"
    },
    "test_09_promotional_cta_banner": {
        "test_id": "TC_HOME_009",
        "section": "Promotional Banner",
        "test_case": "Promotional CTA Banner Verification",
        "observation": "Visible & clickable CTA button verified. Guest click retention on Home Page logged for product team clarification."
    },
    "test_10_footer_and_support_elements": {
        "test_id": "TC_HOME_010",
        "section": "Footer & Support",
        "test_case": "Footer Elements Verification",
        "observation": "Verified 13 footer elements (Newsletter input & subscribe, Help accordion & links, Legal accordion & links, Support email, 5 Social media links, Support Chatbot)"
    }
}

def pytest_sessionstart(session):
    """Initializes execution session start time."""
    start_dt = datetime.now()
    ResultTracker.set_start_time(start_dt)
    logger.info(f"Pytest session started at {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(
        headless=True,
        args=["--start-maximized", "--no-sandbox", "--disable-dev-shm-usage"]
    )
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

def pytest_runtest_setup(item):
    item._test_start_time = time.time()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        duration = time.time() - getattr(item, "_test_start_time", time.time())
        meta = TEST_METADATA.get(item.name, {
            "test_id": f"TC_HOME_{item.name[:7].upper()}",
            "section": "General",
            "test_case": item.name.replace("_", " ").title(),
            "observation": "Test execution completed"
        })

        error_msg = ""
        stack_trace = ""
        failed_url = ""
        page = item.funcargs.get("page")
        if page:
            try:
                failed_url = page.url
            except Exception:
                pass

        if report.failed:
            status = "FAIL"
            if call.excinfo:
                error_msg = str(call.excinfo.value)
                stack_trace = str(call.excinfo.traceback)
        elif report.skipped:
            status = "SKIPPED"
        else:
            # Check if any element in this test was marked REQUIREMENT CONFIRMATION NEEDED
            # (e.g. TC_HOME_009)
            has_req = any(r.status == "REQUIREMENT CONFIRMATION NEEDED" and (r.section.lower() in meta["section"].lower() or meta["section"].lower() in r.section.lower()) for r in ResultTracker.results)
            if has_req:
                status = "REQUIREMENT CONFIRMATION NEEDED"
            else:
                status = "PASS"

        # Capture execution screenshot with execution-specific timestamp
        screenshot_path = ""
        screenshot_b64 = ""
        if page:
            clean_func = item.name.replace("test_", "")
            screenshot_path, screenshot_b64 = ScreenshotManager.capture(
                page=page,
                name=f"{meta['test_id']}_{clean_func}",
                status=status
            )
            if screenshot_path and os.path.exists(screenshot_path):
                # Attach to pytest-html extras if plugin loaded
                try:
                    import pytest_html
                    if screenshot_b64:
                        extras.append(pytest_html.extras.image(screenshot_b64))
                    elif screenshot_path:
                        extras.append(pytest_html.extras.image(screenshot_path))
                except Exception as e:
                    logger.warning(f"Could not attach screenshot to html report: {e}")

        # Attach screenshot to section elements in ResultTracker
        ResultTracker.attach_screenshot_to_section(meta["section"], screenshot_path, screenshot_b64)

        # Record test case result
        ResultTracker.record_test_case(
            test_id=meta["test_id"],
            test_name=item.name,
            section=meta["section"],
            test_case=meta["test_case"],
            observation=meta["observation"],
            status=status,
            duration_sec=duration,
            screenshot_path=screenshot_path,
            screenshot_b64=screenshot_b64,
            error_message=error_msg,
            stack_trace=stack_trace,
            failed_url=failed_url
        )

    report.extras = extras

def pytest_sessionfinish(session, exitstatus):
    """Sets session end time and prints console summary table."""
    end_dt = datetime.now()
    ResultTracker.set_end_time(end_dt)
    logger.info("Test session finished. Generating element verification table.")
    ResultTracker.print_table()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Called after all test reporting is complete.
    Generates the custom, self-contained dashboard report in reports/home_page_report.html.
    """
    report_file = ReportGenerator.generate_html_report(output_path="reports/home_page_report.html")
    if report_file and os.path.exists(report_file):
        logger.info(f"Custom SDS Dashboard Report successfully generated at: {report_file}")
