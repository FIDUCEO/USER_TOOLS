import unittest

from fiduceo.tool import get_plugins


class PluginTest(unittest.TestCase):
    def test_test_plugins(self):

        plugins = get_plugins()

        self.assertIsNotNone(plugins)
        self.assertTrue(len(plugins) >= 3)

        self.assertIn('test1', plugins)
        self.assertIn('test2', plugins)
        self.assertIn('test3', plugins)

        self.assertIsNone(plugins['test1']['problem'])

        self.assertIsNotNone(plugins['test2']['problem'])
        self.assertEqual(plugins['test2']['problem']['detail'],
                         'intentional failure')

        self.assertIsNotNone(plugins['test3']['problem'])
        self.assertEqual(plugins['test3']['problem']['detail'],
                         "module 'fiduceo.tool.plugin' has no attribute 'test_plugin_3'")


