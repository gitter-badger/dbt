import pprint
import os
import shutil

from git import Repo

class InstallTask:
    def __init__(self, args, project):
        self.args = args
        self.project = project

        self.deps_path = os.path.join(os.path.expanduser('~'), '.dbt/deps')

    def __clean_deps(self):
        # just in case -- don't want to blow up anyone's home dir!
        if '/.dbt/' in self.deps_path:
            shutil.rmtree(self.deps_path, True)

    def __clone_repo(self, repo_url, version, local_repo_path):
        repo = Repo.clone_from(repo_url, local_repo_path, branch=version)

    def __download_deps(self):
        for dep in self.project.cfg.get('deps', []):
            local_repo_path = os.path.join(self.deps_path, dep['name'])
            self.__clone_repo(dep['url'], dep['version'], local_repo_path)

    def run(self):
        self.__clean_deps()
        self.__download_deps()
