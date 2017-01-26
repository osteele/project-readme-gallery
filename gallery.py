import base64
import os
import re

import mistune
from github import Github  # , GithubException
from jinja2 import Environment

GH_TOKEN = os.environ['GITHUB_API_TOKEN']
origin_repo_name = 'olinlibrary/htl-lab1'

gh = Github(GH_TOKEN)


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


origin_repo = gh.get_repo(origin_repo_name)
repos = list(origin_repo.get_forks())

more_gitub_logins = re.findall(r'https?:\/\/github.com\/([^\/]+)', open('./repos.txt').read())
assert not set(more_gitub_logins) - set(repo.owner.login for repo in repos)

repo_readmes = [get_repo_content_text(repo, 'README.md') for repo in repos]
repo_readme_image_urls = [get_markdown_image_urls(readme) for readme in repo_readmes]
owner_image_dict = {repo.owner.login: repo.get_contents(urls[0])
                    for repo, urls in zip(repos, repo_readme_image_urls)
                    if urls}


# download images
#


def local_image_path_for(repo_owner, image_path):
    return os.path.join('images', owner + os.path.splitext(image_path)[1])


os.makedirs('images', exist_ok=True)
for owner, image in owner_image_dict.items():
    with open(local_image_path_for(owner, image.path), 'wb') as f:
        f.write(base64.b64decode(repos[0].get_git_blob(image.sha).content))

env = Environment()
tpl = env.from_string(open('gallery.tmpl.html').read())

output_path = 'gallery.html'
with open(output_path, 'w') as f:
    entries = [{'title': login, 'image_src': local_image_path_for(owner, image.path)}
               for login, image in owner_image_dict.items()]
    f.write(tpl.render(entries=entries))
print('wrote', len(owner_image_dict), 'slides to', output_path)
