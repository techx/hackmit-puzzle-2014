#!/usr/bin/python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catgif/")

from catgif import app as application
application.secret_key = '875E4801CECD99E0895C7A1BB972DE16055A81F7E4FB0E643DBD1AF835544D9A'