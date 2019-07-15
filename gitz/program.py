from . import git
from . import util
from pathlib import Path
import argparse
import sys

_ERROR_CHANGES_OVERWRITTEN = 'Your local changes would be overwritten'
_ERROR_NOT_GIT_REPOSITORY = (
    'fatal: not a git repository (or any of the parent directories): .git'
)
_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'


class Program:
    def __init__(self, usage, help, code=-1):
        self.usage = usage
        self.help = help
        self.code = code
        self.program = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]
        self.error_called = False

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
        self.error_called = True
        print('ERROR:', self.program + ':', *messages, file=sys.stderr)

    def parse_args(self, add_arguments):
        if self._print_help():
            print()
            print('Full ', end='')
        parser = argparse.ArgumentParser()
        add_arguments(parser)
        self.args = parser.parse_args(self.argv)
        return self.args

    def _print_help(self):
        if '-h' in self.argv or '--h' in self.argv:
            print(self.usage.rstrip())
            print(self.help.rstrip())
            return True

    def require_git(self):
        if not util.find_git_root():
            self.error(_ERROR_NOT_GIT_REPOSITORY)
            self.exit()

    def require_clean_workspace(self):
        self.require_git()
        if git.is_workspace_dirty():
            self.error(_ERROR_CHANGES_OVERWRITTEN)
            self.exit()
