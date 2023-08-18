from sv import svTest

# Starting Up
VMnum = input("Which VM are you running?\n")
thisSession = svTest(VMnum)

f = False; t = True

# Create Folder -> Num, inSDL, infoSDL, infoUDL, Pause
thisSession.createFolder(1, t, t, t, f)
thisSession.createFolder(2, t, t, f, f)
thisSession.createFolder(3, t, f, t, f)
thisSession.createFolder(4, f, t, t, f)
thisSession.createFolder(5, f, f, t, f)
thisSession.createFolder(6, f, t, f, f)

# Other Smart View Tests
#thisSession.checkFilters(t)
#thisSession.checkFilters(f)
#thisSession.checkFolder()

del thisSession