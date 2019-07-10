from pathlib import Path
import argparse
import sys


class Program:
    def __init__(self, usage, help, code=-1):
        self.usage = usage
        self.help = help
        self.code = code
        self.program = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]

    def check_help(self):
        """If help requested, print it and exit"""
        if self._print_help():
            sys.exit(0)

    def error_and_exit(self, *messages):
        self.error(*messages)
        print(self.usage, file=sys.stderr)
        self.exit()

    def exit(self):
        sys.exit(self.code)

    def error(self, *messages):
        print('ERROR:', self.program + ':', *messages, file=sys.stderr)

    def parse_args(self, add_arguments):
        if self._print_help():
            print()
            print('Full ', end='')
        parser = argparse.ArgumentParser()
        add_arguments(parser)
        return parser.parse_args(self.argv)

    def _print_help(self):
        if '-h' in self.argv or '--h' in self.argv:
            print(self.usage.rstrip())
            print(self.help.rstrip())
            return True
