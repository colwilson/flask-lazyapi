#!/usr/bin/env python

import sys

def main ():
    print 'Hello world!'


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
