from . import git_functions
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
        self.called = {}

    def check_help(self):
        """If help requested, print it and exit"""
        if self._print_help():
            sys.exit(0)

    def exit(self):
        sys.exit(self.code)

    def error_and_exit(self, *messages):
        self.error(*messages)
        self.exit()

    def error_and_usage_and_exit(self, *messages):
        self.error(*messages)
        print(self.usage, file=sys.stderr)
        self.exit()

    def error(self, *messages):
        self._print(messages, 'error')

    def warning(self, *messages):
        self._print(messages, 'warning')

    def info(self, *messages):
        self._print(messages)

    def _print(self, messages, category=None):
        caption = self.program + ':'
        if category:
            self.called[category] = True
            caption = category.upper() + ':' + caption
            print(caption, *messages, file=sys.stderr)
        else:
            print(caption, *messages)

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

    def check_git(self):
        if not util.find_git_root():
            self.error(_ERROR_NOT_GIT_REPOSITORY)
            self.exit()

    def check_clean_workspace(self):
        self.check_git()
        if git_functions.is_workspace_dirty():
            self.error(_ERROR_CHANGES_OVERWRITTEN)
            self.exit()
