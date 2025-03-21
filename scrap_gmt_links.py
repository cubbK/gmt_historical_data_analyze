from playwright.sync_api import sync_playwright
import pandas as pd


def scrape_titles_with_playwright(links: list):
    # Create a DataFrame from the links
    df = links
    df["Date"] = df["Title"]
    df["Title"] = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Iterate over the DataFrame rows
        for index, row in df.iterrows():
            print(f"Scraping {row['Date']} - {row['Link']}...")
            date = row["Date"]
            link = row["Link"]
            for attempt in range(3):  # Try up to 3 times
                try:
                    page.goto(
                        "https://web.archive.org" + link,
                        timeout=60000,
                        wait_until="domcontentloaded",
                    )  # Open the link
                    extracted = scrape_gmt_page(page)
                    break  # Exit the loop if successful
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == 2:  # If it's the last attempt, re-raise the exception
                        raise e

            for item in extracted:
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            [
                                {
                                    "Date": date,
                                    "Link": link,
                                    "Title": item["title"],
                                    "IsOutOfStock": item["isOutOfStock"],
                                    "IsP500": item["isP500"],
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

        browser.close()

    # Return the updated DataFrame
    return df


def scrape_gmt_page(page, extracted=[]):
    page.wait_for_selector(
        ".CssLoaderAnimation", state="hidden", timeout=60000
    )  # Wait until the loader is hidden
    next_button = page.locator(
        ".PageNumberLinks .NextPrevLink"
    ).last  # Select the first matching element

    # Retrieve the 'onclick' attribute text
    next_button_onclick_text = next_button.get_attribute("onclick")

    if next_button_onclick_text and "NextPage()" in next_button_onclick_text:
        scrapped_articles = scrape_gmt_page_articles(page)

        extracted.extend(scrapped_articles)

        print("next page")
        next_button.click()
        scrape_gmt_page(page, extracted)
    else:
        scrapped_articles = scrape_gmt_page_articles(page)
        extracted.extend(scrapped_articles)
        print("last page")

    return extracted


def scrape_gmt_page_articles(page):
    articles = page.locator("#Results > li").all()

    info_list = []

    for article in articles:
        info = {}
        info["title"] = article.locator("h2").inner_text()

        description = article.locator(".description").inner_text()
        info["isP500"] = "P500" in description
        info["isOutOfStock"] = "OUT OF STOCK" in description

        info_list.append(info)

    return info_list


def run():
    print("Fetching links from CSV...")
    # Read the links from the CSV file
    links_df = pd.read_csv("output/internet_archive_links.csv")

    print("Scraping titles from links...")
    result_df = scrape_titles_with_playwright(links_df)

    # Save the result to a CSV file for further analysis
    result_df.to_csv("output/gmt_links.csv", index=False)
    print("Scraping completed. Results saved to 'output/gmt_links.csv'.")


if __name__ == "__main__":
    run()
