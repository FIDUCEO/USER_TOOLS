import unittest

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor


class RadPropProcessorTest(unittest.TestCase):

    def test_create_cmd_line_parser(self):
        processor = RadPropProcessor()

        parser = processor._create_cmd_line_parser()
        self.assertIsNotNone(parser)
        self.assertEqual("Radiance Uncertainty Propagation Tool", parser.description)
        self.assertEqual(4, len(parser._positionals._actions))

        self.assertEqual(['-h', '--help'] , parser._positionals._actions[0].option_strings)
        self.assertEqual("help" , parser._positionals._actions[0].dest)

        self.assertEqual([] , parser._positionals._actions[1].option_strings)
        self.assertEqual("input_file" , parser._positionals._actions[1].dest)

        self.assertEqual(['-a', '--algorithm'] , parser._positionals._actions[2].option_strings)
        self.assertEqual("algorithm" , parser._positionals._actions[2].dest)
        self.assertEqual("available algorithms are:\n"
                         "- AVHRR_SST_NAIVE\n"
                         "- AVHRR_SST_SIMPLE\n"
                         "- AVHRR_NDVI\n" , parser._positionals._actions[2].help)

        self.assertEqual(['-o', '--out_dir'] , parser._positionals._actions[3].option_strings)
        self.assertEqual("out_dir" , parser._positionals._actions[3].dest)
        self.assertEqual("The processing output directory, defaults to ." , parser._positionals._actions[3].help)
        self.assertEqual("." , parser._positionals._actions[3].default)

