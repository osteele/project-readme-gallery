# GitHub Project Gallery Builder

Create a [Reveal.js](http://lab.hakim.se/reveal-js/) slide show
for the forks of a GitHub repo.

Each fork's README.md is examined for the presence of an image.

If the README contains an image, a slide for that repo is added to the slide show.

## Installation

    $ pip3 install -r requirements.txt

## Usage

    $ python3 create-slideshow.py GITHUB_REPO

where GITHUB_REPO is of the form owner/repo.

    $ python3 create-slideshow.py --help

for a more complete description and to see command-line options.
