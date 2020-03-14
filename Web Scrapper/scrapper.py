#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests as rq
import csv

with open("page.html", "r") as html_file:
    page_html = html_file.read()

with open("articles.csv", "w") as file:
    pen = csv.writer(file)

    pen.writerow(['Article Heading', 'Image', 'Content'])
    
    page = bs(page_html, "html.parser")

    title = page.head.title.text
    print(title)

    articles = page.find_all("div", class_='article')

    for article in articles:
        heading = article.h2.text
        print(heading)

        image = article.img["alt"]
        print(image)

        content = article.p.text
        print(content)

        print()

        pen.writerow([heading, image, content])