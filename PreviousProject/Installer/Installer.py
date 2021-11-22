#!/usr/bin/env python3

# # Installer.py
# Created by Jason Lei
# October 1, 2021
import pip
import subprocess
import sys


# Installs given package through pip
def install(package):
    subprocess.check_call(["pip3", "install", "--user", package])


# Installs the gitpython dependency. It will check if it is already
# installed first.
def install_gitpython():
    try:
        import git

        return 0
    except BaseException:
        install("gitpython")
        return 1


# Installs the validators dependency. It will check if it is already
# installed first.
def install_validators():
    try:
        import validators

        return 0
    except BaseException:
        install("validators")
        return 1


# Installs the requests dependency. It will check if it is already
# installed first.
def install_requests():
    try:
        import requests

        return 0
    except BaseException:
        install("requests")
        return 1


# Installs the json dependency. It will check if it is already installed first.
def install_json():
    try:
        import json

        return 0
    except BaseException:
        install("json")
        return 1


# Installs the bs4 dependency. It will check if it is already installed first.
def install_beautifulsoup4():
    try:
        import bs4

        return 0
    except BaseException:
        install("beautifulsoup4")
        return 1


# Installs the abc dependency. It will check if it is already installed first.
def install_abc():
    try:
        import abc

        return 0
    except BaseException:
        install("abc")
        return 1


# Installs the dataclasses dependency. It will check if it is already
# installed first.
def install_dataclasses():
    try:
        import dataclasses

        return 0
    except BaseException:
        install("dataclasses")
        return 1


# Installs the typing dependency. It will check if it is already installed
# first.
def install_typing():
    try:
        import typing

        return 0
    except BaseException:
        install("typing")
        return 1


# Installs the datetime dependency. It will check if it is already
# installed first.
def install_datetime():
    try:
        import datetime

        return 0
    except BaseException:
        install("datetime")
        return 1


# Installs the datetime dependency. It will check if it is already
# installed first.
def install_unittest():
    try:
        import datetime

        return 0
    except BaseException:
        install("unittest")
        return 1


# Installs all dependencies required for this project
def install_dependencies():
    dependencies_downloaded = 0
    dependencies_downloaded += install_gitpython()
    dependencies_downloaded += install_validators()
    dependencies_downloaded += install_requests()
    dependencies_downloaded += install_json()
    dependencies_downloaded += install_beautifulsoup4()
    dependencies_downloaded += install_abc()
    dependencies_downloaded += install_dataclasses()
    dependencies_downloaded += install_typing()
    dependencies_downloaded += install_datetime()
    dependencies_downloaded += install_unittest()
    return dependencies_downloaded
