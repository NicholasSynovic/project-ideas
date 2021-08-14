import argparse
from argparse import Namespace

from json import dump

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import get


def args() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="Programming Languages",
        description="A Python project to get a list of programming languages from Wikipedia. The default behavior prints a random programming language to the console.",
    )

    parser.add_argument(
        "-d",
        "--download-only",
        action="store_true",
        required=False,
        help="Flag to download only a JSON file of the list of programming languages",
    )

    return parser.parse_args()


def getPage(wikipediaPage: str) -> BeautifulSoup:
    page = get(url=wikipediaPage).text

    return BeautifulSoup(markup=page, features="lxml")


def getProgrammingLanguage(soup: BeautifulSoup) -> dict:
    data: dict = {}

    letters: ResultSet = soup.findChildren(name="div", attrs={"class": "div-col"})

    letter: Tag
    for letter in letters:

        languages: ResultSet = letter.findAll("li")

        language: Tag
        for language in languages:
            url: str
            try:
                url = "https://en.wikipedia.org" + language.findChild("a").get(
                    key="href"
                )
            except AttributeError:
                url = ""
            data[language.text] = url

    return data


def exportProgrammingLanguages(data: dict) -> None:
    with open(file="languages.json", mode="w") as file:
        dump(obj=data, fp=file)
        file.close()


if __name__ == "__main__":
    soup: BeautifulSoup = getPage(
        wikipediaPage="https://en.wikipedia.org/wiki/List_of_programming_languages"
    )

    languages: set = getProgrammingLanguage(soup=soup)

    exportProgrammingLanguages(data=languages)
