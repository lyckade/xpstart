class Exclusion():
    def __init__(self):
        self.exclusions_archive_file = "ExclusionScenery.zip"
        self.exclusions_archive = False

    def close_archive(self):
        if self.exclusions_archive:
            self.exclusions_archive.close()

    def extract_scenery(self, icao):
        if not self.exclusions_archive:
            return False
        icao_exists = False
        path = "ExclusionScenery/Exclusion_%s/" % (icao)

        nl = self.exclusions_archive.namelist()
        for f in nl:
            if f.startswith(path):
                icao_exists = True
                print f
                self.exclusions_archive.extract(f)
        return icao_exists

    def open_archive(self, filename=""):
        import zipfile

        if filename == "":
            filename = self.exclusions_archive_file
        self.exclusions_archive = zipfile.ZipFile(filename, "r")


# test = Exclusion()
# test.open_archive()
# test.extract_scenery("EDDH")
# test.close_archive()
