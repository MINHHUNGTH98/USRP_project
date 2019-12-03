#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Usrp Nogui
# Generated: Sat Nov 10 14:20:55 2018
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from wifi_phy_hier import wifi_phy_hier  # grc-generated hier_block
import ConfigParser
import foo
import ieee802_11
import pmt
import time
import threading
import serial
from Tkinter import*
import tkMessageBox
import ttk
import MySQLdb
from datetime import datetime
from firebase import firebase
import time

import MySQLdb

#db = MySQLdb.connect(host = "localhost",user = "root", passwd = "417hust",db ="usrp")
#cursor = db.cursor()

firebase = firebase.FirebaseApplication('https://usrp-project-3.firebaseio.com',None)
#file1 = open("rssi.txt","w+");

class usrp_nogui(gr.top_block,Frame):

    def __init__(self, parent):
        gr.top_block.__init__(self, "Usrp Nogui")
        #Frame.__init__(self);

        ##################################################
        # Variables
        ##################################################
        Frame.__init__(self)
        self.parent = parent
        self.rx_power = -50
        self.check = True
        self.file_save = StringVar()
        self.tx_gain = tx_gain = 5
        self.samp_rate = samp_rate = 20e6
        self.pdu_length = pdu_length = 1
        self.out_buf_size = out_buf_size = 96000
        self.lo_offset = lo_offset = 11e6
        self.interval = interval = 200
        self.freq = freq = 2472000000.0
        self.max_tx_gain = 30
        self.min_tx_gain = 0
        self.max_rx_power = -40
        self.min_rx_power = -60
        self.run_thread = True
        #self.var_slider = DoubleVar()

        self.initUI()
        #self.tx_gain = 20


        ##################################################
        # Gui
        ##################################################
        '''
        super(usrp_nogui,self).__init__()
        self.title("usrp_project")
        self.minsize(500,500)
        self.configure(background = "#4D4D4D")
        self.canvas = Canvas(self, bg = "white", bd = 2, height = 400, width = 30, relief = GROOVE)
        self.canvas.place(x=40, y =20)
        self.sliderBar = Scale(self, from_=0, to = 30, orient = VERTICAL, length = 400, bg = "white", resolution = 5)
        self.sliderBar.place(x=300, y =20)
        '''

        ##################################################
        # Blocks
        ##################################################

        self.wifi_phy_hier_0 = wifi_phy_hier(
            bandwidth=20e6,
            chan_est=ieee802_11.LS,
            encoding=ieee802_11.BPSK_1_2,
            frequency=freq,
            sensitivity=0.56,
        )
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	'packet_len',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(freq, rf_freq = freq - lo_offset, rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.tao_goi_tin = blocks.message_strobe(pmt.intern("".join("x" for i in range(pdu_length))), interval)
        self.ieee802_11_mac_0 = ieee802_11.mac(([0x23, 0x23, 0x23, 0x23, 0x23, 0x23]), ([0x42, 0x42, 0x42, 0x42, 0x42, 0x42]), ([0xff, 0xff, 0xff, 0xff, 0xff, 0xff]))
        self.foo_packet_pad2_0 = foo.packet_pad2(False, False, 0.01, 100, 1000)
        (self.foo_packet_pad2_0).set_min_output_buffer(96000)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.6, ))    

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))
        self.msg_connect((self.tao_goi_tin, 'strobe'), (self.ieee802_11_mac_0, 'app in'))
        self.msg_connect((self.wifi_phy_hier_0, 'mac_out'), (self.ieee802_11_mac_0, 'phy in'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.foo_packet_pad2_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.wifi_phy_hier_0, 0))
        self.connect((self.foo_packet_pad2_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_pdu_length(self):
        return self.pdu_length

    def set_pdu_length(self, pdu_length):
        self.pdu_length = pdu_length
        self.tao_goi_tin.set_msg(pmt.intern("".join("x" for i in range(self.pdu_length))))

    def get_out_buf_size(self):
        return self.out_buf_size

    def set_out_buf_size(self, out_buf_size):
        self.out_buf_size = out_buf_size

    def get_lo_offset(self):
        return self.lo_offset

    def set_lo_offset(self, lo_offset):
        self.lo_offset = lo_offset
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.freq, rf_freq = self.freq - self.lo_offset, rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)

    def get_interval(self):
        return self.interval

    def set_interval(self, interval):
        self.interval = interval
        self.tao_goi_tin.set_period(self.interval)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.wifi_phy_hier_0.set_frequency(self.freq)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.freq, rf_freq = self.freq - self.lo_offset, rf_freq_policy=uhd.tune_request.POLICY_MANUAL), 0)

    def initUI(self):  
        self.parent.title("Project")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self, background = '#4D4D4D', width = 300, padx = 5, pady = 5)
        frame1.pack(fill = BOTH, side = LEFT)

        self.canvas = Canvas(frame1,bd = 2, bg = "white", height = 400, width = 30, relief = GROOVE)
        self.canvas.place(x=60,y=50)
        self.rect = self.canvas.create_rectangle(0,-self.rx_power*4,35,400, fill="red", outline = "white")
        self.canvas.create_line(0,240,35,240, fill="black", width = 2)
        self.canvas.create_line(0,160,35,160, fill="black", width = 2)
        self.text = self.canvas.create_text(18,-self.rx_power*4-5, text = "%d" % self.rx_power,fill = 'black', font = ("",10))

        self.sliderBar = Scale(frame1, from_ = 0, to = 30, orient=VERTICAL, length = 400, bg = 'white', resolution =1, command = self.change_tx_slider)
        self.sliderBar.set(self.tx_gain)
        self.sliderBar.config(state = 'disabled')
        self.sliderBar.place(x=200,y=50)

        self.check = Checkbutton(frame1,text = 'Auto', background = "#4D4D4D", activebackground = "#4D4D4D",foreground = 'white', selectcolor="gray",command = self.change_state)
        self.check.place(x = 230, y = 5)
        self.check.select()
        #label1 = Label(frame1, text = "Auto", background = '#4D4D4D', foreground = 'white')
        #label1.place(x = 260, y = 7)

        label1 = Label(frame1, text = "Rx_Power and Tx_Gain", background = '#4D4D4D', foreground = 'white')
        label1.place(x=10,y=5)

        label_rxPower = Label(frame1,text = "rx_power",background ="#4D4D4D", foreground = "white", font=("",10))
        label_rxPower.place(x = 50, y = 460)

        label_100dBm = Label(frame1,text = "-100dBm",background ="#4D4D4D", foreground = "white", font=("",10))
        label_100dBm.place(x = 100, y = 440)

        label_0dBm = Label(frame1,text = "0dBm",background ="#4D4D4D", foreground = "white", font=("",10))
        label_0dBm.place(x = 100, y = 40)

        label_60dBm = Label(frame1,text = "-60dBm",background ="#4D4D4D", foreground = "white", font=("",10))
        label_60dBm.place(x = 100, y = 280)

        label_40dBm = Label(frame1,text = "-40dBm",background ="#4D4D4D", foreground = "white", font=("",10))
        label_40dBm.place(x = 100, y = 200)

        label_rxPower = Label(frame1,text = "rx_power",background ="#4D4D4D", foreground = "white", font=("",10))
        label_rxPower.place(x = 50, y = 460)
        
        label_txGain = Label(frame1,text = "tx_gain",background ="#4D4D4D", foreground = "white", font=("",10))
        label_txGain.place(x = 195, y = 460)

        #button_test = Button(frame1, text = "tang", command = self.tang)
        #button_test.place(x = 50, y = 475)
        #button_test = Button(frame1, text = "giam", command = self.giam)
        #button_test.place(x = 150, y = 475)

        # frame2 = Frame(self, background = 'white', padx = 5, pady = 5)
        # frame2.pack(fill = BOTH, side = LEFT, expand = True)

        # self.tree = ttk.Treeview(frame2, height = 17, columns = ("time","latitude","longitude","hdop","rx_power"))
        # #self.tree.grid(row=100, column=0, columnspan=100)

        # self.tree.column("#0", width=40, minwidth=40, stretch= NO)
        # self.tree.column("time", width=150, minwidth=150, stretch= NO)
        # self.tree.column("latitude", width=150, minwidth=150, stretch= NO)
        # self.tree.column("longitude", width=150, minwidth=150, stretch= NO)
        # self.tree.column("hdop", width=150, minwidth=150, stretch= NO)
        # self.tree.column("rx_power", width=150, minwidth=150, stretch= NO)

        # self.tree.heading("#0",text="STT",anchor= W)
        # self.tree.heading("time",text="time",anchor= W)
        # self.tree.heading("latitude",text="latitude",anchor= W)
        # self.tree.heading("longitude",text="longitude",anchor= W)
        # self.tree.heading("hdop",text="hdop",anchor= W)
        # self.tree.heading("rx_power",text="rx_power",anchor= W)

        # self.load_data()

        # self.tree.pack(fill = BOTH, side = TOP)

        # label_location = Label(frame2, text = "Nhom Nghien Cuu Bo Mon Mach va Xu Ly Tin Hieu", background = 'white')
        # label_location.place(x = 0, y = 370)

        self.button_start = Button(frame1, text = "start", width = 5,state = 'normal', command = lambda: self.start_thread())
        self.button_start.place(x = 40, y = 525)

        self.button_stop = Button(frame1, text = "stop", width = 5,state = 'disabled', command = lambda: self.stop_thread())
        self.button_stop.place(x = 180, y = 525)

        # button_save = Button(frame2, text = "save", width = 5, command = lambda: self.save_data())
        # button_save.place(x = 90, y = 400)
        # entry_fileSave = Entry(frame2, width = 10, textvariable = self.file_save)
        # entry_fileSave.place(x = 160, y = 404)

        # button_delete = Button(frame2, text = "delete",width = 5, command = lambda: self.delete_data())
        # button_delete.place(x = 90, y = 435)

        # button_quit = Button(frame2, text = "quit",width = 5, command = lambda: self.quit())
        # button_quit.place(x = 180, y = 435)

        # self.label_wifi = Label(frame2, text = "802.11g, channel 13(2.472 Ghz), 20Mhz",background = "#4D4D4D", foreground = 'white', font = 10)
        # self.label_wifi.pack(fill = X, side = BOTTOM)

    def control_tx_gain(self,rx_power):  
        if rx_power< self.min_rx_power:
            self.tx_gain = self.tx_gain + 5
            #print "rx_power <", self.min_rx_power, "increase tx_gain:"
            if self.tx_gain > self.max_tx_gain:
                self.tx_gain = self.max_tx_gain
            self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
            #print "\t tx_gain = ", self.tx_gain
        if rx_power>self.max_rx_power:
            self.tx_gain = self.tx_gain - 5
            #print "rx_power >",self.max_rx_power,"decrease tx_gain:"
            if self.tx_gain < self.min_tx_gain:
                self.tx_gain = self.min_tx_gain
            self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
            #print "\t tx_gain = ", self.tx_gain

    def change_tx_gain(self):
            while True:
                if self.run_thread:
                    try:
                        self.rx_power = self.get_data()
                        #file1.writelines(self.rx_power)
                        self.update_bar()
                        self.canvas.update()
                        print "rx_power = ",self.rx_power,"dBm\n"
                        if self.check:
                        	self.control_tx_gain(self.rx_power)
                                self.sliderBar.config(state = 'normal')
                        	self.sliderBar.set(self.tx_gain)
                                self.sliderBar.config(state = 'disabled')
                    except:
                        print "No Internet"
                    time.sleep(5)
                else:
                    break   
    
    def change_tx_slider(self, event):
        self.tx_gain = self.sliderBar.get()    
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def start_thread(self):
        print "start"
        self.run_thread = True
    	self.change_tx_gain_thread = threading.Thread(target = self.change_tx_gain)
        self.change_tx_gain_thread.daemon = True
        self.change_tx_gain_thread.start()
        self.button_start.config(state = 'disabled')
        self.button_stop.config(state = 'normal')

    def stop_thread(self):
        print "stop"
        self.run_thread = False
        self.button_start.config(state = 'normal')
        self.button_stop.config(state = 'disabled')

    def update_bar(self):
    	self.canvas.coords(self.rect,0,-self.rx_power*4,35,400)
    	self.canvas.itemconfig(self.text, text = "%d" % self.rx_power)
        if self.rx_power != 0:
            self.canvas.coords(self.text,18,-self.rx_power*4-5)
        else:
            self.canvas.coords(self.text,18,-self.rx_power*4+10)

    # def load_data(self):
    #     sql = """SELECT * FROM usrp"""
    #     cursor.execute(sql)
    #     data = cursor.fetchall()
    #     for row in data:
    #         self.tree.insert("",0,text = "%d"%row[0],value = (row[1],row[2],row[3],row[4],row[5]))
    #     try:
    #         self.count = data.index(row) + 1
    #     except:
    #         self.count = 0

    # def insert_data(self,time,latitude,longitude,hdop,rx_power):
    #     #time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     date = datetime.now().strftime('%Y-%m-%d ')
    #     time = date + time
    #     self.tree.insert("",0,text = "%d"%self.count,value = (time,latitude,longitude,hdop,rx_power))
    #     sql = """INSERT INTO usrp(stt, time,latitude, longitude, hdop, rx_power)
    #                 VALUES (%d, '%s', %f, %f, %f, %f)"""%(self.count, time, latitude, longitude, hdop, rx_power)
    #     try:
    #         cursor.execute(sql)
    #         db.commit()
    #     except:
    #         db.rollback()
    #     self.count = self.count + 1

    # def save_data(self):
    #     sql = """SELECT *
    #     FROM usrp
    #     INTO OUTFILE '/var/lib/mysql-files/%s.csv'
    #     FIELDS TERMINATED BY ','
    #     ENCLOSED BY '"'
    #     LINES TERMINATED BY '\n';"""%self.file_save.get()
    #     try:
    #        cursor.execute(sql)
    #        db.commit()
    #     except:
    #        db.rollback()

    # def delete_data(self):
    #     sql = """ DELETE FROM usrp"""
    #     try:
    #         cursor.execute(sql)
    #         db.commit()
    #     except:
    #         db.rollback()
    #     for i in self.tree.get_children():
    #         self.tree.delete(i)
    #     self.count = 0

    def cal_distance(lat_1,lon_1,lat_2,lon_2):
        R = 6373.0
        lat1 = radians(lat_1*10**-6)
        lon1 = radians(lon_1*10**-6)
        lat2 = radians(lat_2*10**-6)
        lon2 = radians(lon_2*10**-6)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance*10**3
    
    def change_state(self):
        self.check = not self.check
        if self.check:
            self.sliderBar.config(state = 'disabled')
        else:
            self.sliderBar.config(state = 'normal')

    def get_data(self):
        data = firebase.get('/data',None)
        data_str =  "time: {0},latitude: {1}, longitude: {2}, hdop: {3}".format(data['time'],data['latitude'],data['longitude'],data['hdop'])
        print "\n"+data_str
        #distance = cal_distance()
        #self.insert_data(data['time'],data['latitude'],data['longitude'],data['hdop'],data['rx_power']) 
        return data['rx_power']

    def quit(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.parent.destroy()
            # db.close()

root = Tk()
root.geometry("300x600+50+100")
tb = usrp_nogui(parent = root)

tb.start()
root.protocol("WM_DELETE_WINDOW", tb.quit)
root.mainloop()

