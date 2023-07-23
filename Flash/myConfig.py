import os
PATH_TO_CODE = r"C:\Users\Dell\Desktop\AndroidFlash\Flash\key.txt"

PATH_TO_APP_DIR = ""
IP_MASK = ""
WORD_FOR_CONNECT = []
CODE = ""
RANGE = []


with open(PATH_TO_CODE) as fileWithCode:
    CODE = fileWithCode.read()

PATH_TO_CFG = r"C:\Users\Dell\Desktop\AndroidFlash\Flash\cfg.txt"

for cfg in open(PATH_TO_CFG):
    option = cfg.rstrip().split(" ")
    if option[0] == "ip":
        IP_MASK = option[-1]
    elif option[0] == "PATH_TO_APP_DIR":
        PATH_TO_APP_DIR = option[-1]
    elif option[0] == "WORD_FOR_CONNECT":
         WORD_FOR_CONNECT.extend(option[-1].split(","))
    elif option[0] == "RANGE":
        value = option[-1]
        if value.find(",") != -1:
            numbs = value.split(",")
            numbs = [int(n) for n in numbs]
            RANGE.extend(numbs)
        else:
            RANGE.append(int(value))

TV_BOX = {
    "X96 mini": "",
    "X96 Q": """adb uninstall com.vanced.android.youtube
adb uninstall ua.youtv.androidtv.new
adb uninstall com.vanced.android.apps.youtube.music
adb uninstall com.google.android.youtube.tvkids
adb uninstall com.megogo.application""",
    "X96 Max+": "",
    "X96 MATE": "",
    "Інший": ""
}


if __name__ == "__main__":
    print(PATH_TO_CFG)
    print(IP_MASK)
    print(WORD_FOR_CONNECT)
    print(RANGE)

