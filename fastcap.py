import os
import win32com.client
import win32api

FastCap2 = win32com.client.Dispatch("FasterCap.Document")
pathStr = "C:/Users/alexa/OneDrive/Documents/PhD/PHD Phase/Year 1/Resonator Designs"

s = ["sphere0.txt", "sphere1.txt", "sphere2.txt", "sphere3.txt"]

for sphere in s:
    FastCap2.Run(pathStr+"/" +sphere)
    print(FastCap2.Run(pathStr+"/" +sphere))
    print(FastCap2.IsRunning())
    while FastCap2.IsRunning() is True:
        print(FastCap2.IsRunning())
        win32api.Sleep(10000)

    cap = FastCap2.GetCapacitance()
    print(cap)

FastCap2.Quit()
