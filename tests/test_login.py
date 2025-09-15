#Part 1:
#3. Write the corrected version with proper waits, error handling, and reliability improvements

import pytest
from playwright.sync_api import sync_playwright, expect

def test_user_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://app.workflowpro.com/login")

        
        page.fill("#email", "admin@company1.com")
        page.fill("#password", "password123")
        page.click("#login-btn")


        expect(page).to_have_url("**/dashboard", timeout=10000)
        expect(page.locator(".welcome-message")).to_be_visible()

        browser.close()


def test_multi_tenant_access():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://app.workflowpro.com/login")
        page.fill("#email", "user@company2.com")
        page.fill("#password", "password123")
        page.click("#login-btn")

       
        expect(page.locator(".project-card").first).to_be_visible(timeout=10000)

        projects = page.locator(".project-card")
        for i in range(projects.count()):
            assert "Company2" in projects.nth(i).inner_text()

        browser.close()
