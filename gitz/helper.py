class Helper:
    def __init__(self, USAGE='', HELP='', SUMMARY='', EXAMPLES='', **kwds):
        self.usage = USAGE
        self.help = HELP
        self.summary = SUMMARY
        self.examples = EXAMPLES

    def print_help(self):
        print(self.usage.rstrip())
        print(self.help.rstrip())
