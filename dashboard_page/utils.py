#utils
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""

    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None


@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

def extract_coordinates_from_url(url: str) -> tuple[float,float]:
    """helper function to extract coordinates from url"""
    
    coordinates = url.split('/@')[-1].split('/')[0]
    # return latitude, longitude
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

def main(keyword, location, quantity):
    """Scrape Google Maps data using the provided keyword, location, and quantity."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(5000)

        search_input = f"{keyword} {location}"
        search_box = page.locator('//input[@id="searchboxinput"]')
        search_box.fill(search_input)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        # scrolling
        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        # this variable is used to detect if the bot
        # scraped the same number of listings in the previous iteration
        previously_counted = 0
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

            listings_count = page.locator(
                '//a[contains(@href, "https://www.google.com/maps/place")]'
            ).count()

            if listings_count >= quantity:
                listings = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).all()[:quantity]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Scraped: {len(listings)}")
                break
            else:
                # logic to break from loop to not run infinitely
                # in case arrived at all available listings
                if listings_count == previously_counted:
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = listings_count
                    print(f"Currently Scraped: {listings_count}")

        business_list = BusinessList()

        # scraping
        for listing in listings:
            try:
                listing.click()
                page.wait_for_timeout(5000)

                name_attibute = 'aria-label'
                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                review_count_xpath = '//button[@jsaction="pane.reviewChart.moreReviews"]//span'
                reviews_average_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'

                business = Business()

                name_attibute = 'aria-label'
                business_name = listing.get_attribute(name_attibute)
                business.name = business_name if business_name else ""


                if page.locator(address_xpath).count() > 0:
                    business.address = page.locator(address_xpath).all()[0].inner_text()
                else:
                    business.address = ""

                if page.locator(website_xpath).count() > 0:
                    business.website = page.locator(website_xpath).all()[0].inner_text()
                else:
                    business.website = ""

                if page.locator(phone_number_xpath).count() > 0:
                    business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
                else:
                    business.phone_number = ""

                if page.locator(review_count_xpath).count() > 0:
                    reviews_count_text = page.locator(review_count_xpath).inner_text().split()[0].replace(',', '').strip()
                    business.reviews_count = int(reviews_count_text) if reviews_count_text.isdigit() else None
                else:
                    business.reviews_count = ""

                if page.locator(reviews_average_xpath).count() > 0:
                    reviews_average_text = page.locator(reviews_average_xpath).get_attribute('aria-label')
                    business.reviews_average = float(reviews_average_text.split()[0].replace(',', '.')) if reviews_average_text else None
                else:
                    business.reviews_average = ""

                business.latitude, business.longitude = extract_coordinates_from_url(page.url)

                business_list.business_list.append(business)
            except Exception as e:
                print(f'Error occurred: {e}')

        browser.close()

        return business_list  # Instead of saving, return the business_list object



        # #########
        # # output
        # #########
        
        # browser.close()

        # return business_list  # Instead of saving, return the business_list object


