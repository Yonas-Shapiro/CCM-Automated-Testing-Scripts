from session import session
import time

VMnum = input("Which VM are you running?\n")
thisSession = session(VMnum)



#thisSession.multilingualizeWorkspace()
thisSession.createBW(1, True, 1, 1, 1, 1, 1)