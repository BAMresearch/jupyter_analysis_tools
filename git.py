# -*- coding: utf-8 -*-
# git.py

import os

def isRepo(path):
    return os.path.exists(os.path.join(path, ".git"))
	
def isNBstripoutInstalled():
    out = !nbstripout --status
    return len(out) and "not recognized" not in out[0]

def isNBstripoutActivated():
    out = !nbstripout --status
    return len(out) and "is installed" in out[0]
	
def checkRepo():
    if not isRepo("."):
        print("Not a repo.")
        return
    if not isNBstripoutInstalled():
        print("nbstripout not found!")
        print("Please run the 'Anaconda Update Script'.")
    if not isNBstripoutActivated():
        print("nbstripout not active in this repo!")
        print("Jupyter output will be added to GIT (which is bad).")
    # check the repository in detail
    try:
        import git
    except ImportError:
        return
    from IPython.display import display, HTML
    repo = git.Repo('.')
#    currentNB = os.path.basename(currentNBpath())
    editedOn = repo.git.show(no_patch=True, format="%cd, version %h by %cn", date="iso")
    editedOn = editedOn.split(', ')
    display(HTML('<h3>Document updated on {}</h3><h4>({})</h4>'.format(*editedOn)))
    if repo.is_dirty():
        edits = repo.git.diff(stat=True)
        import re
        edits = re.sub(r" (\++)", r' <span style="color: green;">\1</span>', edits)
        edits = re.sub(r"(\+)?(-+)(\s)", r'\1<span style="color: red;">\2</span>\3', edits)
        display(HTML(
            '<div style="border-style: solid; border-color: darkred; border-width: 1px; padding: 0em 1em 1em 1em; margin: 1em 0em;">'
            '<h4 style="color: darkred;">There are changes in this repository:</h4>'
            "<pre>"+edits+"</pre>"
            '</div>'
        ))
    return
    try:
        return [int(num) for num in edits.split()[:2]]
    except:
        pass
    edits = nbModified()
    if edits is not None and len(edits):
        print("{} lines added, {} removed".format(*edits))
    else:
        print("no changes")
