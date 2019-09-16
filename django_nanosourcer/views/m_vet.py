# -*- coding: UTF-8 -*-
import logging
import re
from StringIO import StringIO
from random import randrange

import requests
from PIL import Image
from django.conf import settings
from django.utils import timezone

from django_nanosourcer.models import *

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

logger_main = logging.getLogger("main")



