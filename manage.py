#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'
import os
import sys

path = '/Users/mccookpv/dev/workspace/django/django_nanosourcer'

if path not in sys.path:
    sys.path.append(path)

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_nanosourcer.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
