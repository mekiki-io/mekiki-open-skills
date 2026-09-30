import sys

from catalog.argv_command import ArgvCommand

if __name__ == "__main__":
    try:
        ArgvCommand(sys.argv[1:]).run()
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)
