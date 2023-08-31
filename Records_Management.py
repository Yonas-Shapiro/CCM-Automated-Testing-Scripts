from rm import recordsManagement

# Starting up
VMnum = input("Which VM are you running?\n")
thisSession = recordsManagement(VMnum)

f = False; t = True

# Create Set -> Num, inSDL, infoSDL, infoUDL
# Table Run -> inSDL, infoSDL, infoUDL, infoOther
thisSession.toggleEMLC(f)
if False:
    thisSession.createSet(1, t)
    thisSession.askCont()
    thisSession.createSet(2, f)
    thisSession.askCont()
thisSession.tableRun(t, 1)
thisSession.tableRun(f, 2)
#thisSession.toggleEMLC(t)
