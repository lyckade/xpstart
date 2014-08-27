class GithubUpdater:
    def __init__(self):

        self.git_user = ""
        self.git_repository = ""
        self.git_branch = "master"
        self.ini_file = "updater.txt"
        self.no_update = False
        self.files = []
        self.folders = []
        self._ini_file_delimiter = ":"

    def _get_file_path(self, line):
        return line.split(self._ini_file_delimiter)[0].strip()

    def _get_md5_value(self, line):
        return line.split(self._ini_file_delimiter)[1].strip()

    def _make_git_raw_base_url(self):
        return "https://raw.githubusercontent.com/%s/%s/%s/" % (self.git_user, self.git_repository, self.git_branch)

    def add_folder(self, path):
        """
        ads a folder which needs to exist before the files are downloaded.
        :param path:
        :return:
        """
        import os

        if path not in self.folders:
            self.folders.append(path)
        if not os.path.exists(path):
            os.makedirs(path)

    def echo(self, txt):
        print txt

    def load_conf(self):
        """
        Loads the configuration file
        :return:
        """

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
        if self.no_update:
            return False
        import urllib

        remote_base_url = self._make_git_raw_base_url()
        remote_url = "%s%s" % (remote_base_url, file_path)
        self.echo("Loading %s from github" % (file_path))
        web_file = urllib.URLopener()
        web_file.retrieve(remote_url, file_path)
        web_file.close()
        return True

    def make_md_hash(self, file_path):
        import hashlib
        import os.path

        if not os.path.exists(file_path):
            return ""
        include_line = ""
        m = hashlib.md5()
        try:
            fd = open(file_path, "rb")
        except IOError:
            print "Unable to open the file in readmode:", file_path
            return
        content = fd.readlines()
        fd.close()
        for eachLine in content:
            m.update(eachLine)
        m.update(include_line)
        return m.hexdigest()

    def update(self):
        self.load_conf()
        for file_line in self.files:
            md5_value = self._get_md5_value(file_line)
            file_path = self._get_file_path(file_line)
            if md5_value == self.make_md_hash(file_path):
                self.echo("%s is up to date" % (file_path))
                continue
            self.load_file(file_path)

    def update_ini_file(self):
        no_update_val = self.no_update
        self.no_update = True
        self.echo("Loading conf file")
        self.load_conf()
        ini_file = open(self.ini_file, "w")
        self.echo("Updating conf file:")
        for file_line in self.files:
            f = self._get_file_path(file_line)
            md_hash = self.make_md_hash(f)
            new_line = self._ini_file_delimiter.join([f, md_hash])
            ini_file.write("%s\n" % (new_line))
            self.echo(new_line)
        ini_file.close()
        self.no_update = no_update_val


updater = GithubUpdater()
updater.git_user = "lyckade"
updater.git_repository = "xpstart"
updater.git_branch = "master"
updater.ini_file = "xpstart/updater.txt"
updater.add_folder("xpstart")
updater.update_ini_file()
raw_input("Update is completed. Press Enter to exit this window.")

