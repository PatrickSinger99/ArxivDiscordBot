import requests
from bs4 import BeautifulSoup


base_url = "https://arxiv.org"


def get_categories():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    categories = {}

    content_div = soup.find(id="content")
    uls = content_div.find_all("ul")

    for ul in uls:
        lis = ul.find_all("li")
        for li in lis:
            cat_title_link = li.find("a", id=True)  # id=True because links of "About arXiv" dont have ids (is a filter)
            if cat_title_link is not None:
                categories[cat_title_link.text] = cat_title_link.get("href")

    return categories


if __name__ == "__main__":
    cats = get_categories()
    print(cats)
