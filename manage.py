#!/usr/bin/env python
from __future__ import print_function

import sys

from flask.ext.script.commands import InvalidCommand

from igor_rest_api import management


if __name__ == '__main__':
    try:
        management.manager.run()
    except InvalidCommand as err:
        print(err, file=sys.stderr)
        sys.exit(1)
