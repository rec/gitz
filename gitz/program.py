from . import log
from . import runner
from . import util
from pathlib import Path
import argparse
import sys

_ERROR_CHANGES_OVERWRITTEN = 'Your local changes would be overwritten'
_ERROR_NOT_GIT_REPOSITORY = (
    'fatal: not a git repository (or any of the parent directories): .git'
)
_ERROR_PROTECTED_BRANCHES = 'The branches %s are protected'


class _Program:
    def __init__(self):
        self.code = -1
        self.executable = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]
        self.called = {}

    def initialize(self, usage, help, add_arguments=None):
        self.usage = usage
        self.help = help
        if self._print_help():
            print()
            print('Full ', end='')

        parser = argparse.ArgumentParser()
        log.add_arguments(parser)
        add_arguments and add_arguments(parser)

        # If -h/--help are set, this next call terminates the program
        self.args = parser.parse_args(self.argv)
        self.log = log.Log(self.args)
        self.run = runner.Runner(self.log)
        self.git = self.run.git
        return self.args

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

    def message(self, *messages):
        self.log.message(*messages)

    def _print(self, messages, category):
        caption = self.executable + ':'
        self.called[category] = True
        caption = category.upper() + ':' + caption
        self.log.error(caption, *messages, file=sys.stderr)

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
        from . import git_functions

        self.check_git()
        if git_functions.is_workspace_dirty():
            self.error(_ERROR_CHANGES_OVERWRITTEN)
            self.exit()


PROGRAM = _Program()
