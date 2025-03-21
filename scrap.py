from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(
        "https://web.archive.org/web/*/https://www.gmtgames.com/m-2-gmt-games.aspx"
    )

    # Locate all year elements
    locator = page.locator("#year-labels > .sparkline-year-label")
    locator.first.wait_for(state="attached", timeout=10000)  # Wait for at least one
    year_elements = locator.all()

    valid_years = {"2020", "2021", "2022", "2023", "2024", "2025"}

    # Filter year_elements where inner text is in valid_years
    filtered_year_elements = [
        element
        for element in year_elements
        if element.evaluate("el => el.innerText") in valid_years
    ]

    link_dictionary = {}

    # Print the page title
    for year_element in filtered_year_elements:
        year_element.click()

        locator = page.locator(".calendar-grid .calendar-day")
        locator.first.wait_for(state="attached", timeout=10000)  # Wait for at least one
        day_elements = locator.all()

        for day_element in day_elements:
            print("here")
            day_element.hover(force=True)
            popup_title = page.locator(".popup-of-day .day-tooltip-title").inner_text()

            popup_link_link = page.locator(
                ".popup-of-day ul li:last-child a"
            ).get_attribute("href")

            if popup_title:
                link_dictionary[popup_title] = popup_link_link
            else:
                raise ValueError("No title found", day_element.inner_text())

        print("yo")

    browser.close()
