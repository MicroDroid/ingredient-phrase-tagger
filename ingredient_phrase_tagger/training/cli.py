import optparse
import sys

from . import labelled_data
from . import translator


class Cli(object):

    def __init__(self, argv):
        self.opts = self._parse_args(argv)

    def run(self):
        """
        Generates training data in the CRF++ format for the ingredient
        tagging task
        """
        with open(self.opts.data_path, encoding='utf-8') as data_file:
            data_reader = labelled_data.Reader(data_file)
            for row in data_reader:
                sys.stdout.buffer.write(
                    (translator.translate_row(row) + '\n').encode('utf8'))

    def _parse_args(self, argv):
        """
        Parse the command-line arguments into a dict.
        """

        opts = optparse.OptionParser()

        opts.add_option(
            "--data-path",
            default="nyt-ingredients-snapshot-2015.csv",
            help="(%default)")

        (options, args) = opts.parse_args(argv)
        return options
