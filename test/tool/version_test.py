import unittest


class VersionTest(unittest.TestCase):
    def test_version_is_defined(self):
        # assert version can be imported
        from fiduceo.tool.version import __version__
        # assert version is a string
        self.assertTrue(isinstance(__version__, str))
