#!/usr/bin/env python3
from os.path import abspath, isdir
from subprocess import call

import argparse
import requests


def keeper(token, path):
    global base_path
    base_path = abspath(path)
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
        url = repo['git_url'].replace('git://github.com/', 'git@github.com:')
        handle_repo(url)

    for e in [l.split(';') for l in r.headers['link'].split(',')]:
        if e[1].split('=')[1] == '"next"':
            next_page = e[0][1:-1]

    return next_page


def handle_repo(repo_url):
    e = repo_url.split(':')[1].split('/')

    repo_org = e[0]
    repo_name = e[1][:-4]
    repo_path = '%s/%s/%s' % (base_path, repo_org, repo_name)

    if isdir(repo_path):
        pull_repo(repo_path)
    else:
        clone_repo(repo_path, repo_url)


def clone_repo(path, url):
    call(['git', 'clone', url, path])


def pull_repo(path):
    print('Pulling %s' % path)
    call(['git', 'fetch', 'origin'], cwd=path)
    call(['git', 'reset', '--hard', 'HEAD'], cwd=path)


if __name__ == '__main__':
    description = 'Syncs your starred repositories in Github. ' \
                  'Should be used for backup purposes and not on live repos.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--token', '-t', required=True,
                        help='Your Github API auth token.')
    parser.add_argument('--destination', '-d', default='repos',
                        help='The output folder for cloned repositories.')

    args = parser.parse_args()
    token = args.token
    path = args.destination
    keeper(token, path)
