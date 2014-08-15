class GithubUpdater:
    def __init__(self):

        self.git_user = ""
        self.git_repository = ""
        self.git_branch = "master"
        self.ini_file = "updater.txt"
        self.files = []

    def _make_git_raw_base_url(self):
        return "https://raw.githubusercontent.com/%s/%s/%s/" % (self.git_user, self.git_repository, self.git_branch)

    def echo(self, txt):
        print txt

    def load_conf(self):
        """
        Loads the configuration file
        :return:
        """
        import os

        if not os.path.exists("xpstart"):
            os.makedirs("xpstart")
        self.load_file(self.ini_file)
        self.files = []
        conf_file = open(self.ini_file, "r")
        for l in conf_file:
            self.files.append(l.strip())
        conf_file.close()

    def load_file(self, file_path):
        """
        Loads one file from the gihub directory
        :param file_path:
        :return:
        """
        import urllib

        remote_base_url = self._make_git_raw_base_url()
        remote_url = "%s%s" % (remote_base_url, file_path)
        self.echo("Loading %s from github" % (file_path))
        web_file = urllib.URLopener()
        web_file.retrieve(remote_url, file_path)
        web_file.close()

    def update(self):
        self.load_conf()
        for file_path in self.files:
            self.load_file(file_path)


updater = GithubUpdater()
updater.git_user = "lyckade"
updater.git_repository = "xpstart"
updater.git_branch = "development"
updater.ini_file = "xpstart/updater.txt"
updater.update()
