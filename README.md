# GitHub Project Gallery Builder

Create a [Reveal.js](http://lab.hakim.se/reveal-js/) slide show
for the forks of a GitHub repo.

Each fork's README.md is examined for the presence of an image.

If the README contains an image, a slide for that repo is added to the slide show.

## Installation

    $ pip3 install -r requirements.txt

Optionally [create a personal GitHub API token](https://github.com/blog/1509-personal-api-tokens).
Set the `GITHUB_API_TOKEN` environment variable to this value.
This will increase the [GitHub API rate limit](https://developer.github.com/v3/#rate-limiting).


## Usage

    $ python3 create-slideshow.py GITHUB_REPO

where GITHUB_REPO is of the form owner/repo.

    $ python3 create-slideshow.py --help

for a more complete description and to see command-line options.
