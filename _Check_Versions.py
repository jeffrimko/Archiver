##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import qprompt
import verace

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

CLI = verace.VerChecker("Archiver", __file__)
CLI.include(r"app\appinfo.py", match="ARCHIVER_VER = ", splits=[('"',1)])
CLI.include(r"CHANGELOG.md", match=" archiver-", splits=[("-",1),(" ",0)], updatable=False)

GUI = verace.VerChecker("gArchiver", __file__)
GUI.include(r"app\appinfo.py", match="GARCHIVER_VER = ", splits=[('"',1)])
GUI.include(r"CHANGELOG.md", match=" garchiver-", splits=[("-",1),(" ",0)], updatable=False)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def show():
    print("CLI = " + (CLI.string() or "mismatch!"))
    print("GUI = " + (GUI.string() or "mismatch!"))

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    show()
    menu = qprompt.Menu()
    menu.add("c", "CLI version", CLI.prompt)
    menu.add("g", "GUI version", GUI.prompt)
    menu.add("a", "show all versions", show)
    menu.main(loop=True)
