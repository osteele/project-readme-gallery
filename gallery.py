"""
Create a Reveal.js slide show from the README images of the forks of a repository.

Author: Oliver Steele
Date: 2017-01-26
License: MIT
"""

import base64
import os
import re

import mistune
from github import Github  # , GithubException
from jinja2 import Environment

# Globals
#

BUILD_DIR = './build'
TEMPLATE_PATH = 'gallery.tmpl.html'
ORIGIN_REPO_NAME = 'olinlibrary/htl-lab1'
FORCE_DOWNLOAD = False

GH_TOKEN = os.environ['GITHUB_API_TOKEN']
gh = Github(GH_TOKEN)

# Helper functions
#


def local_image_path_for(images):
    return os.path.join('images', image.repository.owner.login, os.path.split(image.path)[1])


class ImageCaptureRenderer(mistune.Renderer):
    def __init__(self):
        self.image_links = []
        super().__init__()

    def image(self, src, title, text):
        self.image_links.append(src)
        return super().image(src, title, text)


def get_markdown_image_urls(markdown_text):
    renderer = ImageCaptureRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    markdown(markdown_text)
    return renderer.image_links


def get_repo_content_text(repo, path):
    content = repo.get_contents(path)
    return base64.b64decode(content.content).decode()


# Find all the repos
#

origin_repo = gh.get_repo(ORIGIN_REPO_NAME)
repos = list(origin_repo.get_forks())

# `repos.txt` is an optional list of repos. Add any that weren't already found (that aren't forks).
SURVEY_REPO_LIST_PATH = './repos.txt'
if os.path.exists(SURVEY_REPO_LIST_PATH):
    more_gitub_repos = re.findall(r'https?:\/\/github.com\/([^\/\s]+\/[^\/\s]+)', open(SURVEY_REPO_LIST_PATH).read())
    repos += [gh.get_repo(repo_name) for repo_name in set(more_gitub_repos) - set(repo.full_name for repo in repos)]


# Downlaod and parse the READMEs
#

# these next two lists are implicitly indexed by repos
repo_readmes = [get_repo_content_text(repo, 'README.md') for repo in repos]
repo_readme_image_urls = [get_markdown_image_urls(readme) for readme in repo_readmes]

# {string -> [github.Content]}
owner_image_dict = {repo.owner.login: [repo.get_contents(re.sub(r'\.\/', '', u)) for u in urls]
                    for repo, urls in zip(repos, repo_readme_image_urls)
                    if urls}


# download images
#

images = [image for images in owner_image_dict.values() for image in images]

for image in images:
    local_path = os.path.join(BUILD_DIR, local_image_path_for(image))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if FORCE_DOWNLOAD or not os.path.exists(local_path):
        print('downloading', local_path)
        with open(local_path, 'wb') as f:
            f.write(base64.b64decode(image.repository.get_git_blob(image.sha).content))


# Create the HTML
#

env = Environment()
tpl = env.from_string(open(TEMPLATE_PATH).read())

output_path = os.path.join(BUILD_DIR, 'gallery.html')
with open(output_path, 'w') as f:
    entries = [{'title': owner, 'image_srcs': [local_image_path_for(image) for image in images]}
               for owner, images in owner_image_dict.items()]
    f.write(tpl.render(entries=entries, pycode=open('gallery.py').read()))
print('wrote {} slides and {} images to {}'.format(len(owner_image_dict), len(images), output_path))
