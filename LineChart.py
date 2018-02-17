import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
import pyqtgraph as pg
import numpy as np
import time

today_count = 0                                                 #储存今日计数
temp_current_date = (time.strftime("%d"))                       #获得系统日期(天)
if int(temp_current_date) <= 16:                                #检查是不是下一个月
    buff_time = 28
else:
    buff_time = 0
current_date = int(temp_current_date) + buff_time                       
read_data_txt = []                                              #List读到的出击数据
time_txt = []                                                   #List读到的日期数据

class Chart(QWidget):

    def __init__(self):
        super().__init__()
         
        self.ChartUI()

    def  text_save(content, filename, mode = 'a'):              #保存txt函数
        file = open(filename, mode)
        for i in range(len(content)):
            file.write(str(content[i])+'\n')
        file.close

    def  text_read(filename, mode = 'r'):                       #读取txt函数
        try:
            file = open(filename, 'r')
        except IOError:
            error = []
            return error
        content = file.readlines()
        for i in range(len(content)):
            content[i] = content[i][:len(content[i])-1]
        file.close()
        return content

    global time_txt                                             #判断储存的日期有无变化
    time_txt = text_read('Time.txt')
    if  int(time_txt[-1]) != int(current_date):
        old_time_text = [current_date]
        text_save(old_time_text, 'Time.txt')
        text_save('0', 'Data.txt')
    

    def Increase(self):                                         #Increase动作
        global today_count
        today_count = today_count + 1
        str_today_count = str(today_count)
        for i in range(len(str_today_count)):
            open('Count.txt', mode = 'w').write(str(str_today_count[i])+'\n')

    def Decrease(self):                                         #Decrease动作
        global today_count
        today_count = today_count - 1
        str_today_count = str(today_count)
        for i in range(len(str_today_count)):
            open('Count.txt', mode = 'w').write(str(str_today_count[i])+'\n')

    def Show(self):                                             #Show动作
        global array
        global time_txt
        d = open('Data.txt','r+')
        dlist = d.readlines()
        list1 = np.array(time_txt, dtype = int)
        list1 = np.array(list1, dtype = int)
        list2 = np.array(dlist, dtype = int)
        list2 = np.array(list2, dtype = int)
        pg.plot(list1,list2,title='Chart').setAspectLocked()
        

    def Save(self):                                             #Save动作
        global today_count
        global current_date
        global time_txt
        str_today_count = str(today_count)
        t = open('Time.txt','r+')
        tlist = t.readlines()
        tlistlast = tlist[-1]
        tlist_str = ''.join(tlistlast)
        tlist_str = tlist_str.strip()
        if int(current_date) == int(tlist_str):                 #判断当日是否多次输入数据
            d = open('Data.txt','r+')                           #把Data.txt提取为List，修改最后一行数据后以写方式写入
            dlist = d.readlines()
            dtempStorage = dlist[-1]
            dtempStorageInt = int (dtempStorage)
            dtempCalculateInt = dtempStorageInt + int(today_count)
            dlist[-1] = str(dtempCalculateInt)
            d_write = open('Data.txt','w')
            d_write.writelines(dlist)
            #Debug Goes Here

            #Debug Ends Here
        for i in range(len(str_today_count)):                   #将Count.txt中保存好的数据清空
            open('Count.txt', mode = 'w').write('\n'+str(0)+'\n')
            today_count = 0


    def ChartUI(self):

        btn_increase = QPushButton('Increase', self)            #Increase按钮
        btn_increase.resize(91,31)
        btn_increase.move(10, 10)
        btn_increase.clicked.connect(self.Increase)

        btn_decrease = QPushButton('Decrease', self)            #Decrease按钮
        btn_decrease.resize(91,31)
        btn_decrease.move(110, 10)  
        btn_decrease.clicked.connect(self.Decrease)

        btn_save = QPushButton('Save', self)                    #Save按钮
        btn_save.resize(91,31)
        btn_save.move(210, 10)  
        btn_save.clicked.connect(self.Save)

        btn_show = QPushButton('Show', self)                    #Show按钮
        btn_show.resize(91,31)
        btn_show.move(310, 10)  
        btn_show.clicked.connect(self.Show)

        self.resize(410,51)                                     #主窗体
        self.setWindowTitle('Console')   
        self.show()

         
if __name__ == '__main__':                                      #Blablabla    
    app = QApplication(sys.argv)
    ex = Chart()
    sys.exit(app.exec_())