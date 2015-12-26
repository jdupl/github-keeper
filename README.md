# github-keeper

Syncs your starred repositories in Github. Should be used for backup purposes and not on live repos.

## Requirements
* Python 3, pip and virtualenv
* Git
* [A Github API token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)

## Installation
* Clone the repository and cd in the cloned repo
* Recommended: `virtualenv env && . env/bin/activate`
* `pip install -r requirements.txt`

## Usage

### Manual usage
Use --help

### Wrapper (for cron and virtualenv)

Example for every hour:
`0 * * * * /path/to /github-keeper/github-keeper-cron-wrapper "my github token" "path to store cloned repos"`
