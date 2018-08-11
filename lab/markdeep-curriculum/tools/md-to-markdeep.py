#!/usr/local/bin/python3

import codecs
import re
import sys


def main():
    # Main Program Entry Point

    # Set output stream to use UTF-8 encoding.
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    printHeader()

    for line in sys.stdin:
        processLine (line.rstrip())

    printFooter()

    return 0


#-----------------------------------------------------------------------------------------------------------------------
def printHeader():
    print ("<meta charset='utf-8'>")
    print ("<!-- " + ("=" * 91) + " -->\n")


#-----------------------------------------------------------------------------------------------------------------------
def printFooter():
    print ("\n\n<!-- Markdeep: -->")
    print ("<style class='fallback'>body{visibility:hidden;white-space:pre;font-family:monospace}</style>")
    print ("<script src='markdeep.min.js'></script>")
    print ("<script src='https://casual-effects.com/markdeep/latest/markdeep.min.js'></script>")
    print ("<script>window.alreadyProcessedMarkdeep||(document.body.style.visibility='visible')</script>")


#-----------------------------------------------------------------------------------------------------------------------
def processLine(line):
    print (line)


#-----------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    sys.exit (main())
