from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(
        "https://web.archive.org/web/*/https://www.gmtgames.com/m-2-gmt-games.aspx"
    )

    year_elements = page.locator("#year-labels > sparkline-year-label")
    valid_years = {"2020", "2021", "2022", "2023", "2024", "2025"}

    # Collect valid year elements into a list
    valid_years = []
    for i in range(year_elements.count()):
        year_text = year_elements.nth(i).inner_text().strip()
        if year_text in valid_years:
            valid_years.append(year_text)
        else:
            print(f"Excluding element with text: {year_text}")

    # Print the filtered list of valid years
    print("Valid years:", valid_years)
    print(page.title())
