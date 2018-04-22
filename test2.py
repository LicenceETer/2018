
#!/usr/bin/env python
# coding:utf-8
import psutil
import time
import tkinter

syslist = []
warn = 70


def Sysinfo():
    Boot_Start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
    syslist.append(Boot_Start)
    time.sleep(0.5)
    Cpu_usage = psutil.cpu_percent()
    syslist.append(Cpu_usage)
    RAM = int(psutil.virtual_memory().total / (1027 * 1024))
    syslist.append(RAM)
    RAM_percent = psutil.virtual_memory().percent
    syslist.append(RAM_percent)
    Swap = int(psutil.swap_memory().total / (1027 * 1024))
    syslist.append(Swap)
    Swap_percent = psutil.swap_memory().percent
    syslist.append(Swap_percent)
    Net_sent = psutil.net_io_counters().bytes_sent
    Net_recv = psutil.net_io_counters().bytes_recv
    Net_spkg = psutil.net_io_counters().packets_sent
    Net_rpkg = psutil.net_io_counters().packets_recv
    BFH = r'%'
    print " \033[1;32m开机时间：%s\033[1;m" % Boot_Start
    print " \033[1;32m当前CPU使用率：%s%s\033[1;m" % (Cpu_usage, BFH)
    print " \033[1;32m物理内存：%dM\t使用率：%s%s\033[1;m" % (RAM, RAM_percent, BFH)
    print " \033[1;32mSwap内存：%dM\t使用率：%s%s\033[1;m" % (Swap, Swap_percent, BFH)
    print " \033[1;32m发送：%d Byte\t发送包数：%d个\033[1;m" % (Net_sent, Net_spkg)
    print " \033[1;32m接收：%d Byte\t接收包数：%d个\033[1;m" % (Net_recv, Net_rpkg)
    for i in psutil.disk_partitions():
        print " \033[1;32m盘符: %s 挂载点: %s 使用率: %s%s\033[1;m" % (i[0], i[1], psutil.disk_usage(i[1])[3], BFH)


def show_reminder():
    root = Tk()
    root.withdraw()
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight() - 100
    root.resizable(False, False)
    root.title("警告!")
    frame = Frame(root, relief=RIDGE, borderwidth=3)
    frame.pack(fill=BOTH, expand=1)
    label = Label(frame, text="CPU，内存，或磁盘超出警戒!", font="Monotype\ Corsiva -20 bold")
    label.pack(fill=BOTH, expand=1)
    button = Button(frame, text="OK", font="Cooper -25 bold", fg="red", command=root.destroy)
    button.pack(side=BOTTOM)
    root.update_idletasks()
    root.deiconify()
    root.withdraw()
    root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 20, root.winfo_height() + 20,
                                   (screenwidth - root.winfo_width()) / 2,
                                   (screenheight - root.winfo_height()) / 2))
    root.deiconify()
    root.lift(aboveThis=None)
    root.mainloop()


if __name__ == "__main__":
    while True:
        Sysinfo()
        sysfile = open("information.txt", "a+")
        sysfile.write('-----------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                    time.localtime(time.time())) + '----------' + '\n')
        sysfile.write("开机时间：" + syslist[0] + '\n')
        sysfile.write("当前CPU使用率：" + str(syslist[1]) + '\n')
        sysfile.write("物理内存使用率：" + str(syslist[3]) + '\n')
        sysfile.write("Swap内存使用率：" + str(syslist[5]) + '\n')
        for i in psutil.disk_partitions():
            sysfile.write("盘符:" + i[0] + '挂载点:' + i[1] + '使用率:' +
                          str(psutil.disk_usage(i[1])[3]) + '\n')
        sysfile.close()
        if syslist[3] > warn:
            show_reminder()
        time.sleep(30)
