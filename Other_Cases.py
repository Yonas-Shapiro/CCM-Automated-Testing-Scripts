from bw import businessWorkspace
import time

#
VMnum = input("Which VM are you running?\n")
thisSession = businessWorkspace(VMnum)

# Num, SDL, NameSDL, NameUDL, AttSDL, AttUDL, Pause
thisSession.classicBW(1, False, True, True, False, True, True)
thisSession.classicBW(2, False, True, True, False, True, False)




thisSession.quit()
del thisSession