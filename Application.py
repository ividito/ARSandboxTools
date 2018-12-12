from Tkinter import *
import tkFileDialog
import platform
import DEMConverter as dem

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.fileType = 'none'
        self.outputFile = 'output.grid'  # TODO add selection

    def filetypesel(self):
        if self.filetypevar.get()==1:
            return 'xyz'
        elif self.filetypevar.get()==2:
            return 'USGS'
        else:
            return 'none'

    def inputfilesel(self):  # TODO implement appropriate filetypes based on selection
        self.inputselection = tkFileDialog.askopenfilename(initialdir = "/" if platform.system()=='Linux' else "C:/",title = "Select file",filetypes = (("xyz files","*.xyz"),("all files","*.*")))
        print self.inputselection
        self.inputSelectionLabel.config(text="Input DEM file = "+self.inputselection)
        self.inputSelectionLabel.grid(column=1, row=4)
        return

    def inputGraphFileSel(self):
        self.inputgraph = tkFileDialog.askopenfilename(initialdir = "/" if platform.system()=='Linux' else "C:/",title = "Select file",filetypes = (("inputgraph files","*.inputgraph"),("all files","*.*")))
        print self.inputgraph
        self.inputgraphSelectionLabel.config(text="Inputgraph file = " + self.inputgraph)
        self.inputgraphSelectionLabel.grid(column=1, row=5)
        return

    def attributecheck(self):
        text=''
        try:
            self.fileType
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
                text = text+"Please select a input graph.\n"
        return text

    def convertLoadFile(self):
        error = self.attributecheck()
        self.errorLabel.config(text=error)
        if error:
            return

        if self.fileType == 'xyz':
            dem.ConvertXYZToGrid(self.inputselection, self.outputFile)
            #  load inputgraph with outputfile
        elif self.fileType == 'USGS':
            print "USGS files not implemented"
        self.quit()

    def createWidgets(self):
        self.filetypevar = IntVar()

        self.filetypeLabel = Label(self)
        self.filetypeLabel.config(text="Select DEM file type")
        self.filetypeLabel.grid()

        self.xyzSelect = Radiobutton(self, text='xyz', variable=self.filetypevar, value=1, command=self.filetypesel)
        self.xyzSelect.grid(column=0)
        self.usgsSelect = Radiobutton(self, text='USGS', variable=self.filetypevar, value=2, command=self.filetypesel)
        self.usgsSelect.grid(column=0)
        self.noneSelect = Radiobutton(self, text='None (start sandbox normally)', variable=self.filetypevar, value=3, command=self.filetypesel)
        self.noneSelect.select()
        self.noneSelect.grid(column=0)

        self.inputSelectionLabel = Label(self)
        self.inputSelectionLabel.grid(column=1, row=4, ipadx=10)
        self.inputgraphSelectionLabel = Label(self)
        self.inputgraphSelectionLabel.grid(column=1, row=5, ipadx=10)

        self.inputSelectBtn = Button(self, text='Choose Input DEM', command=self.inputfilesel)
        self.inputSelectBtn.grid(column=0, row=4)
        self.inputGraphBtn = Button(self, text='Choose inputgraph', command=self.inputGraphFileSel)
        self.inputGraphBtn.grid(column=0, row=5)

        self.startButton = Button(self, text='Start ARSandbox', command=self.convertLoadFile)
        self.startButton.grid()
        self.errorLabel = Label(self)
        self.errorLabel.grid(column=1, row=6)
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()


if __name__ == '__main__':
    app = Application()
    app.master.title('ARSandbox File Loader')
    app.mainloop()