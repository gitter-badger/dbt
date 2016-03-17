import pprint
import os

from git import Repo

class InstallTask:
    def __init__(self, args, project):
        self.args = args
        self.project = project

        self.deps_path = os.path.join(os.path.expanduser('~'), '.dbt/deps')

    def __clone_repo(self, repo_url, version, dest_path):
        """
        clone a repo from remote to configured package directory
        repo_url : path to remote repository
        version  : git branch name or tag
        dep_name : identifier for this dependency
        """

        repo = Repo.clone_from(repo_url, dest_path, branch=version)

    def __download_deps(self):
        for dep in self.project.cfg.get('deps', []):
            dest_path = os.path.join(self.deps_path, dep['name'])
            self.__clone_repo(dep['url'], dep['version'], dest_path)

    def run(self):
        self.__download_deps()
