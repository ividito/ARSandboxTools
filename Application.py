from Tkinter import *
import tkFileDialog
import platform
import DEMConverter as dem
import InputGraphManager as ig
import os
import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.master.resizable(False, False)
        self.fileType = 'none'
        self.outputFile = 'output.grid'  # TODO add selection

    def filetypesel(self):
        if self.filetypevar.get()==1:
            self.fileType= 'xyz'
        elif self.filetypevar.get()==2:
            self.fileType = 'USGS'
        else:
            self.fileType = 'none'

    def inputfilesel(self):  # TODO implement appropriate filetypes based on selection
        self.inputselection = tkFileDialog.askopenfilename(initialdir = "/" if platform.system()=='Linux' else "C:/",title = "Select file",filetypes = (("xyz files","*.xyz"),("all files","*.*")))
        print self.inputselection
        self.inputSelectionLabel.config(text=self.inputselection, wraplength=150)
        self.inputSelectionLabel.grid(column=5, row=0)

        xi, yi, Z = dem.ExtractGridFromXYZ(self.inputselection)
        self.f = Figure(figsize=(3, 3), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.pcolormesh(xi, yi, Z)
        self.a.set_axis_off()
        self.f.subplots_adjust(top=1, bottom=-0.1, left=-0.1, right=1.1)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas._tkcanvas.grid(column=4, row=1, rowspan=6, columnspan=2, padx=10)
        return

    def inputGraphFileSel(self):
        self.inputgraph = tkFileDialog.askopenfilename(initialdir = "/" if platform.system()=='Linux' else "C:/",title = "Select file",filetypes = (("inputgraph files","*.inputgraph"),("all files","*.*")))
        print self.inputgraph
        self.inputgraphSelectionLabel.config(text="Inputgraph file = " + self.inputgraph)
        self.inputgraphSelectionLabel.grid(column=3, row=5)
        return

    def attributecheck(self):
        text=''
        try:
            self.fileType
            if self.fileType =='none': raise AttributeError
        except AttributeError:
            text = text+"Please select a filetype.\n"
        if self.fileType!='none':
            try:
                self.inputselection
            except AttributeError:
                text = text+"Please select a input DEM.\n"
            try:
                self.inputgraph
            except AttributeError:
                text = text+"Please select a input graph."
        return text

    def convertLoadFile(self):
        error = self.attributecheck()
        self.errorLabel.config(text=error)
        if error:
            return

        if self.fileType == 'xyz':
            dem.ConvertXYZToGrid(self.inputselection, self.outputFile)
            cwd = os.getcwd()
            ig.setDemFileName(self.inputgraph, cwd+'\\'+self.outputFile)
        elif self.fileType == 'USGS':
            print "USGS files not implemented"
        else:
            print self.fileType
        self.quit()


    def createWidgets(self):
        self.filetypevar = IntVar()

        self.filetypeLabel = Label(self)
        self.filetypeLabel.config(text="Select DEM file type:")
        self.filetypeLabel.grid(column=2)

        self.xyzSelect = Radiobutton(self, text='xyz', variable=self.filetypevar, value=1, command=self.filetypesel)
        self.xyzSelect.grid(column=2, sticky=S)
        self.usgsSelect = Radiobutton(self, text='USGS', variable=self.filetypevar, value=2, command=self.filetypesel)
        self.usgsSelect.grid(column=2, sticky=N)
        self.noneSelect = Radiobutton(self, text='None (start sandbox normally)', variable=self.filetypevar, value=3, command=self.filetypesel)
        #self.noneSelect.grid(column=0)

        self.seperator = ttk.Separator(self, orient=VERTICAL)
        self.seperator.grid(column=1, row=0, rowspan=8, sticky='ns', padx=10)

        self.inputSelectionLabel = Label(self)
        self.inputSelectionLabel.grid(column=5, row=0, ipadx=10)
        self.inputgraphSelectionLabel = Label(self)
        self.inputgraphSelectionLabel.grid(column=3, row=5, ipadx=10)

        self.inputSelectBtn = Button(self, text='Choose Input DEM', command=self.inputfilesel)
        self.inputSelectBtn.grid(column=2, row=4, sticky=S)
        self.inputGraphBtn = Button(self, text='Choose inputgraph', command=self.inputGraphFileSel)
        self.inputGraphBtn.grid(column=2, row=5, sticky=N)

        self.startButton = Button(self, text='Start ARSandbox (Advanced)', command=self.convertLoadFile)
        self.startButton.grid(column=2, row=7, pady=10)
        self.errorLabel = Label(self)
        self.errorLabel.grid(column=4, row=7)
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=0, row=5)
        self.normalStartButton = Button(self, text='Start ARSandbox', command=self.quit)
        self.normalStartButton.grid(column=0, row=3, padx=10)

        # placeholder preview panel, this gets replaced by the real preview
        self.f = Figure(figsize=(3, 3), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.set_axis_off()
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas._tkcanvas.grid(column=4, row=1, rowspan=6, columnspan=2, padx=10)
        self.previewLabel = Label(self, text='Preview loaded DEM:')
        self.previewLabel.grid(column=4, columnspan=1, row=0, sticky=W, pady=12)



if __name__ == '__main__':
    app = Application()
    app.master.title('ARSandbox File Loader')
    app.mainloop()
