#!/usr/bin/python3.5

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import tkinter
from tkinter import ttk
from tkinter import filedialog

def openFile(fname):
    fin = open(fname, 'r')
    lines = []
    xrr, yrr = [], []
    lent = 40
    for i in fin:
        j = i
        i = i.split()
        if (len(i) < 2) or (len(i) > 2):
            lines.append(j)
            continue
        try:
            x = float(i[0])
            y = float(i[1])
            xrr.append(x)
            yrr.append(y)
            lent = len(j)-1
        except ValueError:
            lines.append(j)
    fin.close()
    return lines, lent, xrr, yrr

def function(x, xrr, yrr):
    if x < xrr[0]:
        return yrr[0]
    if x > xrr[-1]:
        return yrr[-1]
    i = 0
    while i < len(xrr):
        if xrr[i] == x:
            return yrr[i]
        if x < xrr[i]:
            break
        i += 1
    return yrr[i-1]+(yrr[i]-yrr[i-1])*(x-xrr[i-1])/(xrr[i]-xrr[i-1])

def rolling(length, divide, f, x0, xN, text, info, progress):
    rxrr, ryrr = [], []
    step = length/divide
    start = x0 - length/2
    i = start
    S = 0
    while i < (x0 + length/2):
        j = i
        i += step
        S += (f(j)+f(i))*step/2
    end = i
    length = end - start
    progress['value'] = end
    progress['maximum'] = xN
    while end < xN:
        rxrr.append((end+start)/2)
        ryrr.append(S/length)
        S -= (f(start)+f(start+step))*step/2
        S += (f(end)+f(end+step))*step/2
        start += step
        end += step
        text.set("Прошло {} из {} секунд".format(end, xN))
        progress['value'] = end
        info.update()
    return rxrr, ryrr

def off():
    print("HELL")

class Window():
    
    def __init__(self, master):
        self.master = master
        self.master.wm_title("Graphic")
        self.graphic = []
        self.fig = plt.figure(figsize=(5, 4))
        self.master.protocol("WM_DELETE_WINDOW", self.closefigure)
        self.plot = self.fig.add_subplot("111")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        try:
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        except NameError:
            self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        self.toolbar.update()
        drawFrame = tkinter.Frame(self.master)
        
        optionFrame = tkinter.Frame(drawFrame)
        
        periodFrame = tkinter.Frame(optionFrame)
        txt = tkinter.StringVar()
        txt.set("Период:   ")
        period = tkinter.Label(periodFrame, font="Consolas 14", textvariable=txt)
        period.pack(side=tkinter.LEFT)
        self.period = tkinter.Entry(periodFrame, state=tkinter.DISABLED, font="Consolas 14")
        self.period.pack(side=tkinter.LEFT)
        periodFrame.pack(side=tkinter.TOP)
        
        divideFrame = tkinter.Frame(optionFrame)
        txt = tkinter.StringVar()
        txt.set("Разбиение:")
        divide = tkinter.Label(divideFrame, font="Consolas 14", textvariable=txt)
        divide.pack(side=tkinter.LEFT)
        self.divide = tkinter.Entry(divideFrame, state=tkinter.DISABLED, font="Consolas 14")
        self.divide.pack(side=tkinter.LEFT)
        self.divide.insert(0, "100")
        divideFrame.pack(side=tkinter.TOP)
        
        self.countbutton = tkinter.Button(optionFrame, text="Посчитать", font="Consolas 14", state=tkinter.DISABLED, command=self.count)
        self.countbutton.pack(side=tkinter.TOP)
        
        optionFrame.pack(side=tkinter.LEFT)
        
        self.lst = tkinter.Listbox(drawFrame)
        self.lst.insert(0, 'root')
        self.lst.delete(0, 0)
        self.lst.pack(side=tkinter.LEFT)
        
        self.drawbutton = tkinter.Button(drawFrame, text="Нарисовать", state=tkinter.DISABLED, font="Consolas 14", command=self.draw)
        self.drawbutton.pack()
        
        self.clearbutton = tkinter.Button(drawFrame, text="Очистить", font="Consolas 14", command=self.clearPlot)
        self.clearbutton.pack()
        
        drawFrame.pack(side=tkinter.TOP)

        filebutton = tkinter.Frame(self.master)
        self.openbutton = tkinter.Button(filebutton, text="Открыть фaйл...", font="Consolas 14", command=self.openFile)
        self.openbutton.pack(side=tkinter.LEFT)
        self.savebutton = tkinter.Button(filebutton, text="Сохранить файл...", state=tkinter.DISABLED, font="Consolas 14", command=self.saveFile)
        self.savebutton.pack(side=tkinter.LEFT)
        filebutton.pack(side=tkinter.TOP)
        #period = tkinter.Label(self.master, font="Consolas 14", textvariable=txt)
        #period.pack(side=LEFT)
        #self.period = tkinter.Entry(self.master, font="Consolas 14")
        #self.period.pack(side=tkinter.LEFT)
        #self.entry = tkinter.Entry(self.master, font="Consolas 14")
        #self.entry.pack(side=tkinter.LEFT)
        #self.openbutton = tkinter.Button(self.master, text="Открыть файл...", font="Consolas 14", command=self.openFile)
        #self.openbutton.pack(side=tkinter.LEFT)
        #self.text = tkinter.StringVar()
        #self.text.set("Прювет :)")
        #self.label = tkinter.Label(self.master, font="Consolas 14", textvariable=self.text)
        #self.label.pack(side=tkinter.BOTTOM)
        self.text = tkinter.StringVar()
        self.info = tkinter.Label(self.master, font="Consolas 14", textvariable=self.text)
        self.info.pack(side=tkinter.BOTTOM)
        self.progress = ttk.Progressbar(self.master)
        self.progress.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
        self.text.set("Прювет :)")
    
    def closefigure(self):
        plt.close(self.fig)
    
    def openFile(self):
        self.fname = filedialog.askopenfilename()
        self.lines, self.lent, self.xrr, self.yrr  = openFile(self.fname)
        self.lst.delete(0,len(self.graphic)-1)
        self.graphic = []
        self.graphic.append(((self.xrr, self.yrr), 'root'))
        self.lst.insert(0, 'root')
        self.savebutton['state'] = tkinter.ACTIVE
        self.drawbutton['state'] = tkinter.ACTIVE
        self.countbutton['state'] = tkinter.ACTIVE
        self.period.configure(state="normal")
        self.divide.configure(state="normal")
        self.text.set("Файл открыт!")
    
    def count(self):
        if not self.lst.curselection():
            self.text.set("Выберите график...")
            return
        length = eval(self.period.get())
        self.period.delete(0, 'end')
        self.period.insert(0, str(length))
        length = float(length)
        divide = int(self.divide.get())
        graphic = self.graphic[self.lst.curselection()[0]]
        i = len(self.graphic)
        f = lambda x: function(x, *graphic[0])
        name = '{}n{}'.format(graphic[1], divide)
        self.countbutton['state'] = tkinter.DISABLED
        fk = rolling(length, divide, f, self.xrr[0], self.xrr[-1], self.text, self.info, self.progress)
        if not fk:
            self.text.set("Расчёт графика остановлен")
        self.graphic.append((
            fk,
            name
                             ))
        self.lst.insert(i, name)
        self.countbutton['state'] = tkinter.ACTIVE
        self.text.set('График {} рассчитан!'.format(name))


    def draw(self):
        for i in self.lst.curselection():
            self.plot.plot(*self.graphic[i][0])
            self.canvas.draw()
            self.toolbar.update()
            self.text.set("График {} нарисован".format(self.graphic[i][1]))
            self.info.update()
    
    def saveFile(self):
        if not self.lst.curselection():
            self.text.set("Выберите график...")
            return
        fname = filedialog.asksaveasfilename()
        fout = open(fname, 'w')
        xrr, yrr = self.graphic[self.lst.curselection()[0]][0]
        for i in self.lines:
            fout.write(i+'\n')
        self.progress['value'] = 0
        self.progress['maximum'] = len(xrr)
        for i in range(len(xrr)):
            temp1 = "{:.15f}".format(xrr[i])
            temp2 = "{:.15f}".format(yrr[i])
            fout.write(temp1+" "*(self.lent-len(temp1)-len(temp2))+temp2+'\n')
            self.text.set("{}%".format((i)*100//len(xrr)))
            self.progress['value'] = i
            self.info.update()
        fout.close()
        self.text.set("Файл  графика {} сохранён!".format(self.graphic[self.lst.curselection()[0]][1]))
    
    def clearPlot(self):
        self.plot.cla()
        self.canvas.draw()
        self.toolbar.update()

def main():
    # Data for plotting
    #pylab.plot(xrr, yrr)
    #pylab.plot(*rolling(0.0058882, 100, f, xrr[0], xrr[-1]))
    #pylab.show()
    root = tkinter.Tk()
    window = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
