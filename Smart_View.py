from sv import svTest

# Starting Up
VMnum = input("Which VM are you running?\n")
thisSession = svTest(VMnum)

f = False; t = True

# Create Folder -> Num, inSDL, infoSDL, infoUDL
thisSession.createFolder(1, t, t, t)
thisSession.createFolder(2, t, t, f)
thisSession.createFolder(3, t, f, t)
thisSession.createFolder(4, f, t, t)
thisSession.createFolder(5, f, f, t)
thisSession.createFolder(6, f, t, f)

# Other Smart View Tests
thisSession.checkFilters(t)
thisSession.checkFilters(f)
thisSession.checkFolder()

del thisSession