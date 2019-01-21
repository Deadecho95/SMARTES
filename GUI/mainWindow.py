# --------------------------------------------------------------------------- #
# the window
# --------------------------------------------------------------------------- #
from tkinter import *
from time import *
import numpy as np
"""
from Cloud.driveManager import DriveManager
from Controller.controller import Controller
from Modbus.clientModBus import ClientModBus
from Controller.localDataBase import LocalDataBase
"""

class MainWindow:
    """
    create a GUI
    """

    def __init__(self, ):
        """
        init a window
        """
        self.is_running = 0
        self.is_quit = 0

        """client_modbus = ClientModBus("153.109.14.172", 502)  # the clientmodbus
        client_cloud = DriveManager()  # the client cloud
        database = LocalDataBase()
        self.controller = Controller(client_modbus, client_cloud, database)  # create new controller with clients

        """
        self.window = Tk()
        self.window.configure(background='white')
        self.window.protocol('WM_DELETE_WINDOW')
        self.window.title("SMARTES")

        frame1 = Frame(self.window, borderwidth=0, background='white')
        frame1.pack(side=TOP, padx=50, pady=0)

        label = Label(frame1, text="Smartes Manager", background='white')
        label.pack(side=TOP, padx=0, pady=0, )

        frame2 = Frame(self.window, borderwidth=0, background='white')
        frame2.pack(side=TOP, padx=50, pady=0)

        photo = PhotoImage(file="Files/smartes.png")
        photo = photo.zoom(2)  # with 250, I ended up running out of memory
        photo = photo.subsample(6)
        w = Label(frame2, image=photo, background='white')
        w.photo = photo
        w.pack()

        frame3 = Frame(self.window, borderwidth=0, background='white')
        frame3.pack(side=TOP, padx=0, pady=0)

        self.label2 = Label(frame3, text="Power Consumption: 0", background='white')
        self.label2.pack(side=LEFT, padx=0, pady=0)

        self.label3 = Label(frame3, text="Power Grid: 0", background='white')
        self.label3.pack(side=LEFT, padx=10, pady=0)

        self.label4 = Label(frame3, text="Power PV: 0", background='white')
        self.label4.pack(side=LEFT, padx=10, pady=0)

        self.label5 = Label(frame3, text="soc battery: 0", background='white')
        self.label5.pack(side=LEFT, padx=0, pady=0)

        button = Button(self.window, text="Run program", command=self.run, height=2, width=15)
        button2 = Button(self.window, text="Stop program", command=self.stop, height=2, width=15)
        button3 = Button(self.window, text="Quit program", command=self.quit, height=2, width=15)
        button.pack(side=LEFT, padx=5, pady=5)
        button3.pack(side=RIGHT, padx=5, pady=5)
        button2.pack(side=TOP, padx=5, pady=5)

    def start(self):
        """
        the program make cycles
        :return:
        """
        while self.is_quit == 0:  # quit if isquit
            while self.is_running == 1:  # stop run if !is running

                self.controller.start_cycle()   # run the program
                self.data()
                old_time = new_time = time()

                while new_time-old_time <= 30 and self.is_running == 1:  # wait for 30sc
                    self.window.update_idletasks()  # update GUI
                    self.window.update()
                    new_time = time()
            self.window.update_idletasks()  # update GUI if program is not running
            self.window.update()

    def run(self):
        """
        run program
        :return:
        """
        self.is_running = 1

    def stop(self):
        """
        stop the program
        :return:
        """
        self.is_running = 0
        self.label2.configure(text="Power Consumption: 0")
        self.label3.configure(text="Power Grid: 0")
        self.label4.configure(text="Power PV: 0")
        self.label5.configure(text="soc battery: 0")

    def quit(self):
        """
        quit the program
        :return:
        """
        if self.is_running == 0:
            self.is_quit = 1
            self.window.quit()

    def data(self):
        """
        data to show in the GUI
        :return:
        """
        data = self.controller.return_values()
        self.label2.configure(text="Power Consumption: "+np.str(data[1]))
        self.label3.configure(text="Power Grid: "+np.str(data[0]))
        self.label4.configure(text="Power PV: "+np.str(data[2]))
        self.label5.configure(text="soc battery: "+np.str(data[3]))
