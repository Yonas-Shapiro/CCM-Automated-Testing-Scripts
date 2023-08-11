from bw import businessWorkspace
import time

#
VMnum = input("Which VM are you running?\n")
thisSession = businessWorkspace(VMnum)

f = False; t = True

# Num, SDL, NameSDL, NameUDL, AttSDL, AttUDL, Pause
thisSession.classicBW(1, f, t, t, f, t, f)
thisSession.classicBW(2, f, t, t, f, t, f)
thisSession.classicBW(3, f, f, t, f, t, f)
thisSession.classicBW(4, f, f, t, f, t, f)
thisSession.classicBW(5, f, t, t, t, t, f)
thisSession.classicBW(6, f, t, t, t, t, f)
thisSession.classicBW(7, f, t, t, t, f, t)
thisSession.classicBW(8, f, t, t, t, f, f)
thisSession.classicBW(9, f, t, f, t, f, f)
thisSession.classicBW(10, f, t, f, t, f, t)
thisSession.classicBW(11, t, t, t, t, f, f)
thisSession.classicBW(12, t, t, t, t, f, f)
thisSession.classicBW(13, t, t, f, t, f, f)
thisSession.classicBW(14, t, t, f, t, f, f)
thisSession.classicBW(15, t, t, t, t, t, f)
thisSession.classicBW(16, t, t, t, t, t, f)
thisSession.classicBW(17, t, t, t, f, t, f)
thisSession.classicBW(18, t, t, t, f, t, f)
thisSession.classicBW(19, t, f, t, f, t, f)
thisSession.classicBW(20, t, f, t, f, t, t)



thisSession.quit()
del thisSession