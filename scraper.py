import requests
from bs4 import BeautifulSoup
from helper_functions import *


base_url = "https://arxiv.org"
categories = {}


@info_print("Fetching categories")
def get_categories():
    # Fetch html of base arxiv url
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    global categories
    categories = {}  # Dictionary storing category names and corresponding links

    # Get all unordered lists of the content div
    content_div = soup.find(id="content")
    ul_elements = content_div.find_all("ul")

    # Iterate over every ul and check for valid category links
    for ul in ul_elements:
        li_elements = ul.find_all("li")
        for li in li_elements:
            cat_title_link = li.find("a", id=True)  # id=True because links of "About arxiv" dont have ids
            if cat_title_link is not None:
                categories[cat_title_link.text.lower()] = li.find("a", string="recent").get("href")

    return categories


@info_print("Fetching recents")
def get_recent(category, num=5):
    # Fetch html of recent site for category
    response = requests.get(base_url + categories[category.lower()] + "/recent")
    soup = BeautifulSoup(response.content, "html.parser")

    # get dive of recent submissions
    paper_div = soup.find("dl")
    submissions = paper_div.find_all("dd")
    title_replacements = [["Title: ", ""], ["\n", ""], ["  ", " "]]  # Clean text by removing double spaces, new lines
    all_submissions = []

    # for every submission do...TODO
    for submission in submissions:
        title = submission.find("div", class_="list-title mathjax").text
        for old, new in title_replacements:
            title = title.replace(old, new)
        all_submissions.append({"title": title})

    return all_submissions[:5]  # TEMP FIX


if __name__ == "__main__":
    cats = get_categories()
    print(cats)

    recents = get_recent('astrophysics')
    print(recents)
