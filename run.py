import requests
import argparse
from bs4 import BeautifulSoup


def scrape_mail(query):
    BASE = "http://lists.infradead.org/pipermail/linux-mtd/"
    resp = requests.get(BASE)
    # print(resp.text)
    # soup = BeautifulSoup(open('mtd.html'), "html.parser")
    soup = BeautifulSoup(resp.content, "html.parser")
    # print(soup.prettify())

    rows = soup.find("table", border=3).find_all("tr")

    subject_links = []
    for row in rows:
        cells = row.find_all("td")
        if cells[1].find("a"):
            links = cells[1].find_all("a")
            subject_links.insert(0, links[1].get('href'))

    # print(subject_links)

    # query = 'jffs3'
    for link in subject_links:
        resp = requests.get(BASE + link)
        soup = BeautifulSoup(resp.content, "html.parser")
        if query in soup.get_text().lower():
            print('Find {} in {}'.format(query, link))
            # print(soup.get_text())
            # break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', required=True, help='Search key word')

    args = parser.parse_args()
    print(args)

    scrape_mail(args.query)
