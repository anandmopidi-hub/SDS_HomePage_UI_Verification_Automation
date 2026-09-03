import os
from playwright.sync_api import sync_playwright

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
report_path = os.path.join(project_root, "reports", "home_page_report.html")
report_url = f"file:///{report_path.replace(chr(92), '/')}"
print(f"Opening report URL: {report_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(report_url, wait_until="load")
    
    title = page.title()
    print(f"Page Title: {title}")
    assert "Silhouette Design Store" in title
    
    # Check Dashboard Cards
    cards = page.locator(".card-val").all_text_contents()
    print(f"Dashboard KPI Card Values: {cards}")
    
    # Check Test Cases Table rows count
    tc_rows = page.locator("tbody tr td span.tc-id").all_text_contents()
    print(f"Test Case IDs in report: {tc_rows}")
    assert len(tc_rows) == 10
    
    # Check UI elements count
    ui_rows = page.locator("tr.ui-row").count()
    print(f"Total UI rows rendered: {ui_rows}")
    assert ui_rows == 52
    
    # Verify Modal Lightbox opening on View Screenshot button
    btn = page.locator("button.view-btn").first
    btn.click()
    page.wait_for_timeout(500)
    modal = page.locator("#screenshotModal")
    assert modal.is_visible()
    print(f"Modal Lightbox successfully opened! Modal visible: {modal.is_visible()}")
    
    # Close modal
    close_btn = page.locator(".close-modal-btn")
    close_btn.click()
    page.wait_for_timeout(300)
    assert not modal.is_visible()
    print("Modal Lightbox successfully closed!")
    
    # Take screenshot of report
    screenshot_path = os.path.join(project_root, "screenshots", "dashboard_report_visual_verification.png")
    page.screenshot(path=screenshot_path, full_page=False)
    print(f"Report visual screenshot saved to: {screenshot_path}")
    
    browser.close()

print("ALL REPORT VERIFICATIONS PASSED SUCCESSFULLY!")
