import sys
import getopt

from .announcer import post_message
from .sonar_connector import get_measure
from .constants import module_dict


def execute(argv):

    project_key = ''

    try:
        opts, args = getopt.getopt(argv, "hp:", ["p=", ])
    except getopt.GetoptError as ge:
        print('Plz check arguments' + ge)
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('test.py -p <project_key>')
            sys.exit()
        elif opt in ("-p", "--project_key"):
            project_key = arg.strip()

    sonar_measure = get_measure(module_dict[project_key])

    post_message(module_dict[project_key], sonar_measure)


if __name__ == '__main__':
    execute(sys.argv[1:])
