import xpstart


class Exclusion(xpstart.Base):
    def __init__(self, xp_path, gui=None):
        xpstart.Base.__init__(self, gui)

        self.gui = gui

        if xp_path.endswith("/") or xp_path.endswith("\\"):
            xp_path = xp_path[:-1]
        self.xp_path = xp_path

        self.scenery_path = "%s/Custom Scenery" % (self.xp_path)

        self.exclusions_archive_file = "xpstart/ExclusionScenery.zip"
        self.exclusions_archive = False


    def close_archive(self):
        if self.exclusions_archive:
            self.exclusions_archive.close()

    def extract_scenery(self, icao):
        import os.path

        if not self.exclusions_archive:
            return False
        icao_exists = False
        path = "Exclusion_%s/" % (icao)
        if os.path.exists("%s/%s" % (self.scenery_path, path)):
            self.echo("Exclusion scenery for %s already exists." % (icao))
            return True
        nl = self.exclusions_archive.namelist()
        for f in nl:
            if f.startswith(path):
                icao_exists = True
                self.exclusions_archive.extract(f, self.scenery_path)
                self.echo("Copying %s to scenery folder." % (f))
        if not icao_exists:
            self.echo("No exclusion scenery availiable for %s" % (icao))
        return icao_exists

    def open_archive(self, filename=""):
        import zipfile

        if filename == "":
            filename = self.exclusions_archive_file
        self.exclusions_archive = zipfile.ZipFile(filename, "r")


