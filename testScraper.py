from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys
import re
from email_validator import validate_email, EmailNotValidError


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
    email: str = None  # New field to hold email addresses

    facebook: str = None  # Field to hold Facebook username
    instagram: str = None  # Field to hold Instagram username
    twitter: str = None  # Field to hold Twitter username
    linkedin: str = None  # Field to hold LinkedIn username

@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"output/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

def extract_coordinates_from_url(url: str) -> tuple[float,float]:
    """helper function to extract coordinates from url"""
    
    coordinates = url.split('/@')[-1].split('/')[0]
    # return latitude, longitude
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])


def extract_emails_from_page(page):
    """Extracts valid email addresses from a webpage"""
    email = extract_email_from_page_content(page.content())
    if email:
        # Check if the extracted email matches any placeholder pattern indicating a form
        form_email_placeholders = ["youremail@email.com", "example@emailcom"]
        if email.lower() in form_email_placeholders:
            return "no official email found. there was a form"
        
        # Validate the extracted email address
        try:
            email_info = validate_email(email, check_deliverability=True)
            return email_info.normalized
        except EmailNotValidError as e:
            # If the email address is not valid or deliverable, return None
            return "None"
    
    # If no valid email is found, search on other pages
    other_pages = ["contact", "contact-us"]
    for page_name in other_pages:
        page.goto(f"{page.url}/{page_name}")
        page.wait_for_load_state("networkidle")
        email = extract_email_from_page_content(page.content())
        if email:
            # Check if the extracted email matches any placeholder pattern indicating a form
            form_email_placeholders = ["youremail@email.com", "example@emailcom"]
            if email.lower() in form_email_placeholders:
                return "no official email found. there was a form"
            
            # Validate the extracted email address
            try:
                email_info = validate_email(email, check_deliverability=True)
                return email_info.normalized
            except EmailNotValidError as e:
                # If the email address is not valid or deliverable, return None
                return None
    
    # If no valid email is found, return "None" as a string
    return "None"



def extract_email_from_page_content(content):
    """Extracts a valid email address from webpage content"""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, content)
    # Find the first valid email
    for email in emails:
        if "@" in email:
            return email
    
    # Extract the first email from mailto links
    mailto_pattern = r"mailto:([^\s@]+@[^\s@]+\.[^\s@]+)"
    mailto_emails = re.findall(mailto_pattern, content)
    valid_mailto_email = validate_email(mailto_emails)

    if valid_mailto_email:
        return valid_mailto_email
    
    return None


def extract_social_media_links(page):
    """Extracts social media links from a webpage"""
    social_media_links = {
        "Facebook": None,
        "Instagram": None,
        "Twitter": None,
        "LinkedIn": None
    }
    
    # Search for social media links
    for platform in social_media_links.keys():
        pattern = rf"https?:\/\/(www\.)?{platform.lower()}\.com\/(\w+)\/?"
        match = re.search(pattern, page.content())
        if match:
            social_media_links[platform] = match.group(0)
        else:
            social_media_links[platform] = "None"

    # LinkedIn may have different patterns for personal and company profiles
    # Search for both patterns and prioritize company profiles
    linkedin_pattern_company = r"https?://(www\.)?linkedin\.com/company/([\w-]+)/?"
    linkedin_pattern_personal = r"https?://(www\.)?linkedin\.com/in/([\w-]+)/?"

    match_company = re.search(linkedin_pattern_company, page.content())
    match_personal = re.search(linkedin_pattern_personal, page.content())

    if match_company:
        social_media_links["LinkedIn"] = match_company.group(0)
    elif match_personal:
        social_media_links["LinkedIn"] = match_personal.group(0)

    return social_media_links


def main():
    # # read search from input.txt file
    # input_file_name = 'input.txt'
    # # Get the absolute path of the file in the current working directory
    # input_file_path = os.path.join(os.getcwd(), input_file_name)
    # # Check if the file exists
    # if os.path.exists(input_file_path):
    #     # Open the file in read mode
    #     with open(input_file_path, 'r') as file:
    #         # Read the first line as the search term
    #         search_term = file.readline().strip()
    #         if not search_term:
    #             print('Error occurred: The input.txt file is empty or does not contain a search term.')
    #             sys.exit()
    # else:
    #     print('Error occurred: The input.txt file does not exist.')
    #     sys.exit()

    ###########
    # scraping
    ###########

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=6000)
        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(5000)

        print(f"-----\n{search_term}".strip())

        page.locator('//input[@id="searchboxinput"]').fill(search_term)
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

            if (
                page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()
                >= total
            ):
                listings = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).all()[:total]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Scraped: {len(listings)}")
                break
            else:
                # logic to break from loop to not run infinitely
                # in case arrived at all available listings
                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    == previously_counted
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    print(
                        f"Currently Scraped: ",
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count(),
                    )

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

                if len(listing.get_attribute(name_attibute)) >= 1:
                    business.name = listing.get_attribute(name_attibute)
                else:
                    business.name = ""
                if page.locator(address_xpath).count() > 0:
                    business.address = page.locator(address_xpath).all()[0].inner_text()
                else:
                    business.address = ""
                if page.locator(website_xpath).count() > 0:
                    website = page.locator(website_xpath).all()[0].inner_text()
                    if not website.startswith("http"):
                        website = "https://" + website
                    business.website = website
                else:
                    business.website = ""
                if page.locator(phone_number_xpath).count() > 0:
                    business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
                else:
                    business.phone_number = ""
                if page.locator(review_count_xpath).count() > 0:
                    business.reviews_count = int(
                        page.locator(review_count_xpath).inner_text()
                        .split()[0]
                        .replace(',','')
                        .strip()
                    )
                else:
                    business.reviews_count = ""

                if page.locator(reviews_average_xpath).count() > 0:
                    business.reviews_average = float(
                        page.locator(reviews_average_xpath).get_attribute(name_attibute)
                        .split()[0]
                        .replace(',','.')
                        .strip())
                else:
                    business.reviews_average = ""

                business.latitude, business.longitude = extract_coordinates_from_url(page.url)

                # Open a new tab and navigate to the business website
                new_page = browser.new_page()
                new_page.goto(business.website)
                new_page.wait_for_load_state("networkidle")

                # Extract email addresses from the website
                business.email = extract_emails_from_page(new_page)

                # Extract social media usernames from the website
                social_media_links = extract_social_media_links(new_page)
                business.facebook = social_media_links["Facebook"]
                business.instagram = social_media_links["Instagram"]
                business.twitter = social_media_links["Twitter"]
                business.linkedin = social_media_links["LinkedIn"]

                # Close the new tab
                new_page.close()

                business_list.business_list.append(business)
            except Exception as e:
                print(f'Error occurred: {e}')

        #########
        # output
        #########
        business_list.save_to_excel(f"google_maps_data_{search_term}".replace(' ', '_'))
        business_list.save_to_csv(f"google_maps_data_{search_term}".replace(' ', '_'))

        browser.close()




if __name__ == "__main__":
    total = 1_000_000
    search_term = input("What to search: ")
    main()
