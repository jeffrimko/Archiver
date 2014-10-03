"""This script provides a library for working with Asciidoc markup."""

##==============================================================#
## DEVELOPED 2014, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def format_doc(title, body, date="", author=""):
    """Formats the document text as Asciidoc.

    :param title: (str) Title of the document.
    :param body: (str) Body of the document.
    :param date: (str) Date stamp for the document.
    :param author: (str) Author of the document.
    """
    if not title:
        title = "Untitled"
    doc = "%s\n" % title
    doc += "".join(["=" for i in title])
    doc += "\n"
    if author:
        doc += ":author: %s\n" % author
    if date:
        doc += ":date: %s\n" % date
    doc += "\n"
    doc += body
    return doc

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    print format_doc("Hello world!", "some test here\nmore text")
