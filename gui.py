from tkinter import *
from customtkinter import *
import keyboard
from config import Config

set_appearance_mode("dark")
set_default_color_theme("blue")

class Gui(CTk):
    def __init__(self, client, dualsense):
        super().__init__()
        self.client = client
        self.dualsense = dualsense
        
        self.title("Robot Controller")
        self.setup_ui()
        self.bind("<KeyRelease>", self.key_clicked)
        self.protocol("WM_DELETE_WINDOW", dontclosewindow)
        self.handle_key_presses()

    def setup_ui(self):
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        self.lbl_speed = CTkLabel(self.main_frame, text="Geschwindigkeit (in %)")
        self.lbl_speed.pack()
        self.speed = IntVar(value="10")
        self.sb_speed = CTkEntry(self.main_frame, textvariable=self.speed)
        self.sb_speed.pack(pady=10)
        
        self.buttom_frame = CTkFrame(self.main_frame)
        self.buttom_frame.pack(expand=True, fill=BOTH)
        
        self.lbl_p_value = CTkLabel(self.buttom_frame, text="P-Regler")
        self.lbl_p_value.pack()
        self.p_value = StringVar(value=Config.KP)
        self.sb_p_value = CTkEntry(self.buttom_frame, textvariable=self.p_value, justify=CENTER)
        self.sb_p_value.pack(pady=0)
        
        self.lbl_i_value = CTkLabel(self.buttom_frame, text="I-Regler")
        self.lbl_i_value.pack()
        self.i_value = StringVar(value=Config.KI)
        self.sb_i_value = CTkEntry(self.buttom_frame, textvariable=self.i_value, justify=CENTER)
        self.sb_i_value.pack(pady=0)
        
        self.lbl_d_value = CTkLabel(self.buttom_frame, text="D-Regler")
        self.lbl_d_value.pack()
        self.d_value = StringVar(value=Config.KD)
        self.sb_d_value = CTkEntry(self.buttom_frame, textvariable=self.d_value, justify=CENTER)
        self.sb_d_value.pack(pady=0)
        
        self.btn_save = CTkButton(self.buttom_frame, text="Save", command=self.update_variables)
        self.btn_save.configure(fg_color="Grey")
        self.btn_save.pack(fill=BOTH, expand=1, pady=10)

        self.btn_stop_all = CTkButton(self.main_frame, text="Kompletter Stop", command=self.btn_stop_all_clicked)
        self.btn_stop_all.configure(fg_color="Red")
        self.btn_stop_all.pack(fill=BOTH, expand=1, pady=10)
        
        self.btn_start = CTkButton(self.main_frame, text="Linienfollower Start", command=self.start_clicked)
        self.btn_start.configure(fg_color="Green")
        self.btn_start.pack(fill=BOTH, expand=1, pady=10)
        
        self.btn_controller_input = CTkButton(self.main_frame, text="Controller Input", command=self.controller_input_clicked)
        self.controller_input_value = BooleanVar(value="False")
        self.btn_controller_input.configure(fg_color="Orange")
        self.btn_controller_input.pack(fill=BOTH, expand=1, pady=10)

    # Placeholder-Method for event managment
    def key_clicked(self, event):
        pass

    def handle_key_presses(self):
        pass

    def btn_stop_all_clicked(self):
        self.client.sendCommand(Config.STOPALL)
        self.dualsense.controller_input = False
        self.btn_controller_input.configure(fg_color="Red")

    def start_clicked(self):
        self.client.sendCommand(Config.STARTPID)
    
    def controller_input_clicked(self):
        self.controller_input_value = not self.controller_input_value
        if (self.controller_input_value):
            self.btn_controller_input.configure(fg_color="Green")
            self.dualsense.controller_input = True
        else:
            self.btn_controller_input.configure(fg_color="Red")
            self.dualsense.controller_input = False
    
    def update_variables(self):
        pass

def dontclosewindow():
    print("Dont close this window, stop the program :(")

