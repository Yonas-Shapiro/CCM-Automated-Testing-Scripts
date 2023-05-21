from session import session

VMnum = input("Which VM are you running?\n")
thisSession = session(VMnum)

thisSession.multilingualizeWorkspace()