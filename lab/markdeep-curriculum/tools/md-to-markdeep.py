#!/usr/local/bin/python3

import codecs
import re
import sys


def main():
    # Main Program Entry Point

    setStdioUTF8()

    lines = sys.stdin.readlines()

    # Collect all deferred link definitions (usually at the bottom of the page).
    linkPatterns = getLinkDefinitions(lines)

    printHeader()

    for line in lines:
        processLine(line, linkPatterns)

    printFooter()

    return 0


#-----------------------------------------------------------------------------------------------------------------------
def setStdioUTF8():
    # Set input & output streams to use UTF-8 encoding.
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    if sys.stdin.encoding != 'utf-8':
        sys.stdin = codecs.getreader('utf-8')(sys.stdin.buffer, 'strict')


#-----------------------------------------------------------------------------------------------------------------------
def printHeader():
    print ("<meta charset='utf-8'>\n\n")


#-----------------------------------------------------------------------------------------------------------------------
def printFooter():
    print ("\n\n<!-- " + (91 * "~") + " -->")
    print ("<style class='fallback'>body{visibility:hidden;white-space:pre;font-family:monospace}</style>")
    print ("<script src='markdeep.min.js'></script>")
    print ("<script src='https://casual-effects.com/markdeep/latest/markdeep.min.js'></script>")
    print ("<script>window.alreadyProcessedMarkdeep||(document.body.style.visibility='visible')</script>")


#-----------------------------------------------------------------------------------------------------------------------

linkDefPattern = re.compile(r'\[[^\]]+\]: ')

def getLinkDefinitions(lines):
    # Scan through all lines and find link definitions (usually at the bottom of the page). Store these as regular
    # expressions to match later.

    linkDefPattern = re.compile(r'\[[^\]]+\]: ')
    linkPatterns = []

    for line in lines:
        matchedLinkDef = linkDefPattern.match(line)
        if matchedLinkDef != None:
            linkRegExp = r'[^\]]\[' + line[1:matchedLinkDef.end()-3] + r'\][^:\[]'
            linkPatterns.append (re.compile(linkRegExp))

    return linkPatterns


#-----------------------------------------------------------------------------------------------------------------------

literalBracketPattern = re.compile(r'\\\[[^\]]+\\\]')    # Match "\[thing\]"
mdLinkImmediate = re.compile(r'\.md[\)\]]')              # Match ".md" in "[foo](bar.md)" or "[foo.md]"
mdLinkDefined = re.compile(r'\[[^\]]+\]: .*\.md$')       # Match ".md" in "[foo]: bar/baz/qux.md"

def processLine (line, linkPatterns):
    line = line.rstrip()

    # Convert deferred link definitions to use empty trailing square brackets. For example, "see the [foo] page"
    # (GitHub Markdown) would be converted to "see the [foo][] page" (Markdeep).

    # The link regular expression ensures that some leading and trailing characters are not present. Because of this,
    # the regular expression can fail if the pattern is at the very beginning or end of the line. To handle this case,
    # we prefix and postfix the line with temporary characters, which we'll strip back off later.

    line = "X" + line + "X"

    for linkPattern in linkPatterns:
        while True:
            match = linkPattern.search(line)
            if match == None: break
            linkEndPosition = match.end() - 1
            line = line[:linkEndPosition] + '[]' + line[linkEndPosition:]

    line = line[1:-1]   # Strip off the temporary extension characters.

    # In Markdeep, if you have text in square brackets not followed by parentheses or square brackets, then it's not
    # considered to be a link, therefore you should not escape it.
    while True:
        match = literalBracketPattern.search(line)
        if match == None: break
        line = line[:match.start()] + '[' + line[match.start()+2 : match.end()-2] + ']' + line[match.end():]

    # Look for immediate links to .md files, and convert those to .md.html. Also for links with a name
    # that ends in ".md".
    while True:
        match = mdLinkImmediate.search(line)
        if match == None: break
        line = line[:match.start()+3] + '.html' + line[match.end()-1:]

    # Look for defined links to .md files, and convert those to .md.html.
    match = mdLinkDefined.fullmatch(line)
    if match != None:
        line = line + '.html'

    print (line)


#-----------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    sys.exit (main())
