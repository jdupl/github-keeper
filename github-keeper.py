#!/usr/bin/env python3
import sys
import os

from os import path

import requests


def keeper(token):
    next_page = handle_page('https://api.github.com'
                            '/user/starred?access_token=%s' % token)
    while True:
        if not next_page:
            break
        next_page = handle_page(next_page)


def handle_page(url):
    r = requests.get(url)
    next_page = None

    if r.status_code != 200:
        if r.json()['message']:
            print(r.json()['message'])
        else:
            print(r.json())
        exit(1)

    for repo in r.json():
        handle_repo(repo['clone_url'])

    for e in [l.split(';') for l in r.headers['link'].split(',')]:
        if e[1].split('=')[1] == '"next"':
            next_page = e[0][1:-1]

    return next_page


def handle_repo(repo_url):
    for e in [repo_url.split('://')[1].split('/')]:
        repo_org = e[1]
        repo_name = e[2][:-4]

        repo_path = '%s/%s' % (repo_org, repo_name)
        if path.isdir(repo_path):
            pull_repo(repo_path)
        else:
            clone_repo(repo_path, repo_url)


def clone_repo(path, url):
    pass


def pull_repo(path):
    pass

if __name__ == '__main__':
    keeper(sys.argv[1])
