#Part 3: API + UI Integration Test 
import requests
from playwright.sync_api import sync_playwright

BASE_URL = "https://jsonplaceholder.typicode.com"   #this is base url

def test_project_creation_flow():
    # 1 Create a project via API
    headers = {
        "Authorization": "Bearer test-token",
        "X-Tenant-ID": "company123"
    }
    data = {
        "name": "Test Project",
        "description": "this is data realated to test project API",
        "team_members": ["qualityassurace@example.com", "devlopmentteam@example.com", "projectmanager@example.com"]
    }

#sending http request using post method    
    response = requests.post(f"{BASE_URL}/posts", headers=headers, json=data)
    project = response.json()
    print("API Response:", project)  #print response in terminal 

    assert response.status_code == 201  # this is status code created
    assert project["name"] == "Test Project" # project name 
    

    # 2 Verify project appears correctly in web UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #launch chrome browse.
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/") # Webpage url
        page.fill("#user-name", "standard_user") # locator for username
        page.fill("#password", "secret_sauce") ## locator for password
        page.click("#login-button") #locator for login button
        assert page.locator(".inventory_list").is_visible() # check visibility
        browser.close()

    # 3 Check project is accessible on mobile
    with sync_playwright() as p:
        iphone = p.devices["iPhone 12"] #mobile device
        browser = p.webkit.launch(headless=False) #launch webkit browse in headed  mode that able to see UI.
        context = browser.new_context(**iphone)
        page = context.new_page()
        page.goto("https://www.saucedemo.com/") # Webpage url
        page.fill("#user-name", "standard_user")# locator for username
        page.fill("#password", "secret_sauce")# locator for password
        page.click("#login-button")#locator for login button
        assert page.locator(".inventory_list").is_visible()# check visibility
        browser.close()

    # 4 Validate proper tenant isolation (project only visible to correct company)
    wrong_headers = {
        "Authorization": "Bearer test-token",
        "X-Tenant-ID": "companyXX"
    }
    wrong_company = requests.get(f"{BASE_URL}/{id}", headers=wrong_headers)
    assert wrong_company.status_code == 404

    print("project only visible to correct company")

