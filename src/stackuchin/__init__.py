import argparse
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

class StackuchinCLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='CLI tool to automatically create, update and delete AWS CloudFormation '
                        'stacks in multiple AWS accounts and regions at the same time',
            usage='''stackuchin <command> [<args>]

To see help text, you can run:
    stackuchin help
    stackuchin version
''')
        parser.add_argument('command', help='Command to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    # noinspection PyMethodMayBeStatic
    def version(self):
        print("0.0.1")



def main():
    StackuchinCLI()


if __name__ == '__main__':
    StackuchinCLI()
