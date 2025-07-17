from playwright.sync_api import sync_playwright

def test_rocket_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:4000/rockets/123")
        assert "Rocket" in page.title() or "Falcon" in page.content()
        browser.close()