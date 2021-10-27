#!/usr/bin/env python3

# PackageFetcher.py

import json
import os
import requests
from bs4 import BeautifulSoup
from validators import url as is_valid_url

from Models.Package import Package


class PackageFetcher:
    # Static Variables
    GITHUB_URL_IDENT_KEY = "github.com"
    NPM_URL_IDENT_KEY = "npmjs.com"

    # Instance Variables
    urlString: str

    # Init
    def __init__(self, urlString: str) -> None:
        # TODO: Check that assert fails init
        assert isinstance(urlString, str)
        assert is_valid_url(urlString)
        self.urlString = urlString.strip()

    def fetchPackage(self) -> Package:
        # Fetch GitHub package
        if PackageFetcher.GITHUB_URL_IDENT_KEY in self.urlString:
            return self.__fetchGitHubPackage(self.urlString)
        elif PackageFetcher.NPM_URL_IDENT_KEY in self.urlString:
            return self.__fetchNPMPackage()
        else:
            raise Exception("Unexpected URL")

    @staticmethod
    def __fetchGitHubPackage(urlString: str) -> Package:
        # Split URL to get repository owner and name
        url_components = urlString.split("/")
        base_url_index = url_components.index(
            PackageFetcher.GITHUB_URL_IDENT_KEY)
        repository_owner = url_components[base_url_index + 1]
        repository_name = url_components[base_url_index + 2]

        github_api_url = "https://api.github.com/repos/{}/{}".format(
            repository_owner, repository_name
        )

        # Get Package
        auth_token = os.environ["GITHUB_TOKEN"]
        auth_header = {"Authorization": "token {}".format(auth_token)}
        req = requests.get(
            github_api_url.strip(), headers=auth_header
        )  # strip() needed because `%0A` gets added to the end of the string
        repository_dict = json.loads(req.text)
        return Package(**repository_dict)

    def __fetchNPMPackage(self) -> Package:
        req = requests.get(self.urlString)

        soup = BeautifulSoup(req.text, features="html.parser")
        github_html_component = soup.find(
            "a", href=True, attrs={"aria-labelledby": "repository"}
        )
        github_url = github_html_component["href"]

        assert github_url is not None
        return self.__fetchGitHubPackage(github_url)
