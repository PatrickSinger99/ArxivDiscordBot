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

    submissions_links = paper_div.find_all("dt")
    submissions_content = paper_div.find_all("dd")
    title_replacements = [["Title: ", ""], ["\n", ""], ["  ", " "]]  # Clean text by removing double spaces, new lines
    all_submissions = []

    # Fetch infos for every submission
    for i, submission in enumerate(submissions_content):
        sub_dict = {}

        # Get Title
        try:
            title = submission.find("div", class_="list-title mathjax").text
            for old, new in title_replacements:
                title = title.replace(old, new)
            sub_dict["title"] = title
        except:
            print("[Error] Could not get title of paper")
            continue  # Dont add paper when title cant be fetched

        # Get Authors
        try:
            authors_div = submission.find("div", class_="list-authors")
            authors_names = [link.text for link in authors_div.find_all("a")]
            authors_links = [base_url + link.get("href") for link in authors_div.find_all("a")]
            sub_dict["author_names"] = authors_names
            sub_dict["author_links"] = authors_links
        except:
            print("[Error] Could not get title of paper")
            continue  # Dont add paper when authors cant be fetched

        # Get Links
        try:
            paper_link = submissions_links[i].find("a", title="Abstract").get("href")
            sub_dict["paper_link"] = base_url + paper_link
        except:
            print("[Error] Could not get arxiv link of paper")
        try:
            pdf_link = submissions_links[i].find("a", title="Download PDF").get("href")
            sub_dict["pdf_link"] = base_url + pdf_link
        except:
            print("[Error] Could not get pdf link of paper")

        # Add fetched info to return list
        all_submissions.append(sub_dict)

        # Break loop if desired number of papers has been reached
        if len(all_submissions) >= num:
            break

    return all_submissions


if __name__ == "__main__":
    cats = get_categories()
    print(cats)

    recents = get_recent('astrophysics', num=5)
    print(recents)
