#!/usr/bin/python3

activate_this = '/Volumes/Blue S/ZONE/PycharmProjects/legalised/zenv/bin/activate_this.py'
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/html/legalised')
import os

os.environ['OPENAI_API_KEY'] = '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'

from app import app as application
