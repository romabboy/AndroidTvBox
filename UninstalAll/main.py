with open("1.txt") as file:
    with open("uninstall.bat", "w") as fileW:
        for raw in file:
            fileW.write(f"adb uninstall {raw}")