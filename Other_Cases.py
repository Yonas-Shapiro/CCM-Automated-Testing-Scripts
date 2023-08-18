from bw import businessWorkspace

# Starting Up
VMnum = input("Which VM are you running?\n")
thisSession = businessWorkspace(VMnum)

f = False; t = True

# Business Workspace -> Created in Classic View: Num, inSDL, NameSDL, NameUDL, AttSDL, AttUDL, Pause
thisSession.multilingualizeWorkspace()
thisSession.classicBW(1, f, t, t, f, t, f)
thisSession.classicBW(2, f, t, t, f, t, f)
thisSession.classicBW(3, f, f, t, f, t, f)
thisSession.classicBW(4, f, f, t, f, t, f)
thisSession.classicBW(5, f, t, t, t, t, f)
thisSession.classicBW(6, f, t, t, t, t, f)
thisSession.classicBW(7, f, t, t, t, f, f)
thisSession.classicBW(8, f, t, t, t, f, f)
thisSession.classicBW(9, f, t, f, t, f, f)
thisSession.classicBW(10, f, t, f, t, f, f)
thisSession.classicBW(11, t, t, t, t, f, f)
thisSession.classicBW(12, t, t, t, t, f, f)
thisSession.classicBW(13, t, t, f, t, f, f)
thisSession.classicBW(14, t, t, f, t, f, f)
thisSession.classicBW(15, t, t, t, t, t, f)
thisSession.classicBW(16, t, t, t, t, t, f)
thisSession.classicBW(17, t, t, t, f, t, f)
thisSession.classicBW(18, t, t, t, f, t, f)
thisSession.classicBW(19, t, f, t, f, t, f)
thisSession.classicBW(20, t, f, t, f, t, f)

# Pausing between Classic and Smart View BWs
thisSession.askCont()

# Business Workspace -> Created in Smart View: Num, inSDL, NameSDL, NameUDL, Pause
thisSession.smartBW(21, f, t, t, f)
thisSession.smartBW(22, f, f, t, f)
thisSession.smartBW(23, f, t, f, f)
thisSession.smartBW(24, t, t, t, f)
thisSession.smartBW(25, t, f, t, f)
thisSession.smartBW(26, t, t, f, f)

# Pausing between BW Creation and Search Query Testing
thisSession.askCont()

# Search Query: inSDL, searchTerm, Pause
thisSession.searchQuery(t, "Joueur B", f)
thisSession.searchQuery(f, "Player A", f)

# Pausing between Search Query Testing and BW in WF Creation
thisSession.askCont()

# Business Workspace -> Created in Workflow: Num, inSDL, Pause
thisSession.prepareForWorkflow()
thisSession.createWorkflowForBW()
thisSession.createBWWF(1, t, f)
thisSession.createBWWF(2, f, f)

# Deleting the Object to End
del thisSession