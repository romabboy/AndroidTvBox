import os
import sys
import tkinter as tk
import subprocess
import threading


BG_LEFT_SIDE = "#82846D"
BTN_LEFT_SIDE = "#646165"
BG_RIGHT_SIDE = "#EBEBEB"

FONT_BTN = ["Arial", 15]

class MyProgram():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("900x600")
        self.window.resizable(0,0)

        self.leftFrame, self.rightFrame = self.create_frame()


        self.create_button()
        self.textRightFrame = "Загрузка"



    def create_frame(self):
        leftFrame = tk.Frame(self.window,bg=BG_LEFT_SIDE,pady=20,padx=7)
        rightFrame = tk.Frame(self.window, bg="black",pady=20)
        leftFrame.columnconfigure(0,minsize=250)

        leftFrame.pack(side=tk.LEFT, fill=tk.BOTH)
        rightFrame.pack(side=tk.LEFT,fill=tk.BOTH)
        #
        # leftFrame.grid(row=0, column=0, sticky=tk.NSEW)
        # rightFrame.grid(row=0, column=1, sticky=tk.NSEW)


        return [leftFrame,rightFrame]

    def create_button(self):

        buttonAuto = tk.Button(
            self.leftFrame,
            text="Автоматичний",
            bg=BTN_LEFT_SIDE,
            fg=BG_RIGHT_SIDE,
            font=FONT_BTN,
            borderwidth=0,
            pady=5,
            padx=5
        )

        buttonManual = tk.Button(
            self.leftFrame,
            text="Ручний",
            bg=BTN_LEFT_SIDE,
            fg=BG_RIGHT_SIDE,
            font=FONT_BTN,
            borderwidth=0,
            pady=5,
            padx=5,
            command=self.create_input()
        )

        buttonAuto.grid(row=0,column=0, sticky=tk.EW,)
        buttonManual.grid(row=1,column=0, sticky=tk.EW,pady=20)

    def create_input(self):
        show = False
        inputFrame = tk.Frame(self.leftFrame,borderwidth=0,bg=BG_LEFT_SIDE)
        inputEnrty = tk.Entry(inputFrame,font=["Arial", 15])
        inputButton = tk.Button(
            inputFrame,
            text="Запуск",
            bg=BTN_LEFT_SIDE,
            fg=BG_RIGHT_SIDE,
            font=FONT_BTN,
            borderwidth=0,
            command=self.run_adb

        )
        self.inputFrame = inputFrame
        self.inputEntry = inputEnrty

        def innerFunc():
            nonlocal show
            show = not show

            if show: inputFrame.grid(column=0, row=2, sticky=tk.EW)
            else: self.hide_vidget(inputFrame)

        inputEnrty.insert(0,"192.168.1.")
        inputEnrty.pack(fill=tk.BOTH, pady=5)
        inputButton.pack(fill=tk.BOTH)

        return innerFunc

    def create_loading(self):
        label = tk.Label(self.rightFrame,font=FONT_BTN,text=self.textRightFrame,bg=BG_RIGHT_SIDE)
        self.label_loading = label
        label.grid(column=0,row=0,sticky=tk.NSEW)

    def update_text(self):
        self.label_loading.config(text=self.textRightFrame)

    def run_adb(self):
        ip = self.inputEntry.get()
        if not self.validation_input(ip):
            self.wrong_ip()
            return

        print(threading.enumerate())
        if threading.active_count() > 1:
            return

        thr = threading.Thread(target=self.thread_for_adb, args=[ip], name="adb_run")
        thr.start()




    def thread_for_adb(self,ip):
        outputCmd = os.popen(f"adb connect {ip}:5555", "r")
        self.create_loading()

        for a in outputCmd:
            self.textRightFrame = ""
            self.textRightFrame = a
            self.update_text()

    def hide_vidget(self,vidget):
        vidget.grid_forget()


    def validation_input(self,ip):
        ipValid = ""

        for row in open("cfg.txt"):
            if row.find("ip") != -1:
                ipValid = row
                break
        else:
            print("Validation_input, False")
            return False

        ipValid = ipValid.rstrip()
        ipValid = ipValid.split(" ")
        ipValid = ipValid[-1]

        return True if ip.find(ipValid) != -1 else False



    def wrong_ip(self):
        print("Wrong")

    def run(self):
        self.window.mainloop()

prog = MyProgram()
prog.run()