#!/bin/python2.7
# getyourbots.com

# Wordpress bruteforcer
# Tool for pentesting wordpress CMS using the xmlrpc interface

# GNU 3 license
# Read the DISCLAIMER before use !

from argumentparser import ArgumentParser as AP
from controller import Controller
from view import View

def main():
    View.banner()

    # validate arguments
    try:
        args_p = AP()
        args = args_p.args()
    except Exception, ex:
        View.error(ex)
        return

    c = Controller(args)        # init controller with arguments provided by user

    c.start()                   # start that bomboklat

if __name__ == "__main__":
    main()
