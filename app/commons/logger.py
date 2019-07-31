#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/ai-chatbot-framework/app/core/chain.py
# Author: Hai Liang Wang
# Date: 2018-01-24:14:01:29
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2018-01-24:14:01:29"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)
sys.path.append(os.path.join(curdir, os.path.pardir, os.path.pardir))

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

import logging.handlers
import json_log_formatter
formatter = json_log_formatter.JSONFormatter()

logger = logging.getLogger("query")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logFilePath = os.path.join(curdir, os.path.pardir, os.path.pardir, "logs", "root.log")
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=logFilePath, when='midnight', backupCount=30)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
