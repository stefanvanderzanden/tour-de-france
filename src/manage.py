#!/usr/bin/env python
import os
import sys

IMPORT_HOME = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
#sys.path.append(os.path.join(IMPORT_HOME, 'src'))
sys.path.append(os.path.join(IMPORT_HOME, 'src/apps'))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
