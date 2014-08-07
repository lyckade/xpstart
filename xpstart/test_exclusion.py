from unittest import TestCase

import exclusion

__author__ = 'lyckade'
xplanepath = "PathToXPlaneFolder"


class TestExclusion(TestCase):
    def test_extract_scenery(self):
        test = exclusion.Exclusion(xplanepath)
        test.open_archive()
        test.extract_scenery("EDDH")
        test.close_archive()
        # self.fail()