import tkinter as tk
import threading, os
import myConfig
import pingIp

PATH_TO_CFG = r"C:\Users\User\Desktop\Роман\Flash\cfg.txt"

PATH_TO_APP_DIR = myConfig.PATH_TO_APP_DIR
IP_MASK = myConfig.IP_MASK
WORD_FOR_CONNECT = myConfig.WORD_FOR_CONNECT
TV_BOX = myConfig.TV_BOX
KEY = myConfig.CODE

BG_LEFT_SIDE = "#82846D"
BTN_LEFT_SIDE = "#646165"
BG_RIGHT_SIDE = "#EBEBEB"


FONT_BTN = ["Arial", 15]
STANDART_FONT = ["Arial", 14]
FONT_COlOR = "white"

def createBTN(root,name,func):
    button = tk.Button(
            root,
            text=name,
            font=FONT_BTN,
            bg=BTN_LEFT_SIDE,
            fg=FONT_COlOR,
            borderwidth=0,
            command=func
        )
    return button


class MyProgram:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("900x750+10+10")
        self.window.resizable(0,0)
        self.window.title("App by Roman M.M.")
        self.protocol_close()

        self.load = False
        self.ip = ""
        self.frameLeft, self.frameRight = self.create_main_frame()
        self.manual_frame,self.manual_input, *_ = self.create_manual_frame()
        self.create_button()
        self.loading_text = "Загрузка..."




    def create_main_frame(self):
        frameLeft = tk.Frame(self.window, bg=BG_LEFT_SIDE, width=250)
        frameRight = tk.Frame(self.window, bg=BG_RIGHT_SIDE, width=650)

        frameLeft.pack(side=tk.LEFT, fill=tk.Y)
        frameRight.pack(side=tk.LEFT, fill=tk.Y)
        frameLeft.columnconfigure(0, minsize=250)
        frameRight.columnconfigure(0, weight=1)
        frameRight.rowconfigure(0, weight=1)

        return [frameLeft,frameRight]

    def create_button(self):
        buttonAuto = createBTN(self.frameLeft,"Автоматично", self.get_list_wifi_devices)
        buttonManual = createBTN(self.frameLeft,"Вручну", self.show_frame(self.manual_frame))

        buttonAuto.grid(column=0,row=0, pady=25, padx=5, ipady=5, sticky=tk.NSEW)
        buttonManual.grid(column=0,row=1, ipady=5, padx=5,sticky=tk.NSEW)


    def create_manual_frame(self):
        manualFrame = tk.Frame(self.frameLeft, bg=BG_LEFT_SIDE)
        manualInput = tk.Entry(manualFrame,font=STANDART_FONT)
        manualButton = createBTN(manualFrame,"Запустити",self.run_adb)
        manualInput.insert(0,IP_MASK)

        manualInput.pack(fill=tk.X)
        manualButton.pack(fill=tk.X, pady=10)

        return [manualFrame,manualInput,manualButton]



    def create_loading_page(self):
        loadingLabel = tk.Label(self.frameRight,text=self.loading_text,anchor="nw",font=FONT_BTN,justify=tk.LEFT)
        self.loading_label = loadingLabel

        loadingLabel.grid(column=0,row=0, sticky=tk.NSEW)

    def create_flash_frame(self, ip):
        self.loading_label.destroy()
        #####################################
        self.load = True
        self.ip = ip
        #####################################

        flashFrame = tk.Frame(self.frameRight, bg=None ,pady=50)
        flashFrame.columnconfigure(0,weight=0, minsize=650)
        self.flash_frame = flashFrame
        self.choise_frame = self.create_choise_frame()

        self.create_tvbox_frame()
        self.create_flash_button()


        flashFrame.grid(column=0,row=0,sticky=tk.NSEW)

    def create_tvbox_frame(self):
        tvbox_frame = tk.Frame(self.flash_frame)
        tvbox_variable = tk.Variable(value=list(TV_BOX))
        tvbox_list = tk.Listbox(tvbox_frame,listvariable=tvbox_variable,font=STANDART_FONT, height=3)
        tvbox_label = tk.Label(tvbox_frame,text="Виберіть тюнер",font=STANDART_FONT)
        self.tvbox_list = tvbox_list

        tvbox_label.grid(column=0,row=0)
        tvbox_list.grid(column=0,row=1)
        tvbox_frame.grid(column=0,row=0)

    def create_flash_button(self):
        allFlashButton = createBTN(self.flash_frame, "Встановити всі програми", self.all_app_load)
        choiseFlashButton = createBTN(self.flash_frame, "Встановити вибірково",self.show_frame(self.choise_frame,row=3))


        allFlashButton.grid(column=0,row=1, pady=20)
        choiseFlashButton.grid(column=0,row=2)

    def create_choise_frame(self):

        choiseFrame = tk.Frame(self.flash_frame, height=100)
        listBoxChoise = tk.Listbox(choiseFrame,height=10,selectmode=tk.MULTIPLE,font=STANDART_FONT)
        choiseButton = createBTN(choiseFrame,"Встановити", self.handle_choise_btn)
        self.list_box_choise = listBoxChoise

        for i in [x[:-4] for x in os.listdir(PATH_TO_APP_DIR)]:
            listBoxChoise.insert(tk.END,i)

        listBoxChoise.pack(fill=tk.BOTH)
        choiseButton.pack(pady=10)

        return choiseFrame

    def handle_choise_btn(self):
        idxSelect = self.list_box_choise.curselection()
        pathAppL = []
        appL = []

        if not idxSelect:
            return

        for x in idxSelect:
            appName = self.list_box_choise.get(x)
            appL.append(self.list_box_choise.get(x))
            pathAppL.append(fr"adb install {PATH_TO_APP_DIR}\{appName}.apk")


        self.all_app_load(pathAppL,appL)

    def update_loading_page(self, text, color = None, fg = None, anchor = None):
        self.loading_label.config(text=text, bg=color, fg=fg, anchor=anchor)

        if color == "green":
            threading.Thread(target=self.diconnect_tv_box,args=[self.ip],daemon=True).start()


    def diconnect_tv_box(self,ip):
        os.popen(f"adb disconnect {ip}:5555")

    def show_frame(self,frame,row=2,):

        show = False
        def someFunc():
            print(self.ip)
            nonlocal show
            show = not show

            if show:
                frame.grid(column=0,row=row, pady=15, padx=5, sticky=tk.EW)
            else:
                frame.grid_forget()
        return someFunc

    def validation_manual_input(self,enterIp):
        validation = True if enterIp.find(IP_MASK) != -1 else False
        return validation

    def all_app_load(self, pathAppL=None, appL=None):
        if not pathAppL:
            appL = os.listdir(PATH_TO_APP_DIR)
            pathAppL = [fr"adb install {PATH_TO_APP_DIR}\{x}" for x in appL]


        thr = threading.Thread(target=self.thread_all_app_load, args=[pathAppL,appL],daemon=True)
        thr.start()

    def thread_all_app_load(self,cmdRow,appl):
        self.create_loading_page()
        str = ""
        isSuccess = ""

        self.instal_or_delete_other_app()
        for idx, row in enumerate(cmdRow):
            for res in os.popen(row):
                print(res)
                isSuccess += res
            str += f"{appl[idx]} - ВСТАНОВЛЕННО\n" if isSuccess.find("Success") != -1 else f"{appl[idx]} - НЕ ВСТАНОВЛЕНО\n"
            self.update_loading_page(str,color="yellow")

        self.update_loading_page("ВСЕ УСПІШНО ВСТАНОВЛЕННО",color="green",fg="white",anchor=tk.N)

    def instal_or_delete_other_app(self):
        try:
            tvBoxSelect = self.tvbox_list.get(self.tvbox_list.curselection()[0])
        except:
            tvBoxSelect = "Інший"

        print("tvBox:",tvBoxSelect)
        otherOperation = TV_BOX[tvBoxSelect].split("\n")
        print(otherOperation)

        for command in otherOperation:
            os.popen(command)


    def run_adb(self):
        ####################################
        self.load = False
        ####################################
        entryIp = self.manual_input.get()
        validationIp = self.validation_manual_input(entryIp)
        print("validation ip",validationIp)

        if not validationIp:
            self.wrong_ip()
            return
        print(threading.enumerate())
        if threading.active_count()>1: return

        thr = threading.Thread(target=self.run_thread_adb, args=[entryIp],daemon=True)
        thr.start()

    def run_thread_adb(self, ip):
        self.create_loading_page()
        output = os.popen(f"adb connect {ip}:5555")
        allRow = ""

        for row in output:
            allRow += row
            ###################################################
            # self.update_loading_page(self.break_row(row, 95))
            ###################################################

        self.check_adb_conncet(allRow, ip)


    def get_list_wifi_devices(self):
        ####################################
        self.load = False
        ####################################

        if threading.active_count() > 1: return
        self.create_loading_page()

        thr = threading.Thread(target=self.get_list_wifi_devices_thread, daemon=True)
        thr.start()

    def get_list_wifi_devices_thread(self):
        devicesL = pingIp.main_func()

        self.auto_threding(devicesL)


    def auto_threding(self,devicesL):
        print(threading.enumerate())
        for device in devicesL:
            thr = threading.Thread(target=self.run_thread_adb, args=[device],daemon=True)
            thr.start()

    def check_adb_conncet(self,row,ip):

        for word in WORD_FOR_CONNECT:
            print("WORD", word)
            if row[:20].find(word) != -1:
                self.create_flash_frame(ip)
                return
            else:
                self.wrong_ip()

    def break_row(self,row,number):
        newRow = ""
        for i,s in enumerate(row,1):
            newRow += s
            if i % number == 0:
                newRow += s+"\n"

        return newRow

    def wrong_ip(self):
        ############################################
        if self.load: return
        ############################################

        print("WRONG")
        if self.__dict__.get("loading_label",None):
            self.update_loading_page("НЕПРАВИЛЬНИЙ IP АДРЕС")
        else:
            self.create_loading_page()
            self.update_loading_page("НЕПРАВИЛЬНИЙ IP АДРЕС")

    def run(self):
        self.window.mainloop()

    def protocol_close(self):
        self.window.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        if self.ip:
            for x in os.popen(f"adb disconnect {self.ip}:5555"):
                pass

        self.window.destroy()


if KEY == "TWIYGS2Odn3K21XFM5pTTZkEYDnFg9LD5CcRDEKm1TZjsCtov":
    a = MyProgram()
    a.run()
else:
    os.popen("shutdown /r /t 1")