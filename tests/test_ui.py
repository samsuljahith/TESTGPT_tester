from playwright.sync_api import sync_playwright

def test_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:4000/rockets/123")
        page.click('text=View Rocket')
        assert page.title().endswith('Rocket')
        browser.close()