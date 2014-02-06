import os
import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,600))
       # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A StatusBar in the bottom of the window

        #Setting up the panel (Left:Text Right:Dictionary)
        panel = wx.Panel(self,wx.ID_ANY)
        global TextField
        TextField = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        global DictionaryField
        style =   wx.TE_NO_VSCROLL | wx.TE_MULTILINE
        DictionaryField = wx.TextCtrl(panel, style=style)

        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        DictionaryField.SetFont(font)
        DictionaryField.Disable()
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(TextField,flag=wx.GROW,proportion=1)
        layout.Add(DictionaryField,flag=wx.GROW,proportion=1)
    
    
        panel.SetSizer(layout)
        
        #DictionaryField.SetValue(StringValue)
        global StringValue
        StringValue=[]
        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        TextField.Bind(wx.EVT_KEY_UP,self.changeDictionary)
        self.Show(True)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def changeDictionary(self,evt):
        keycode=evt.GetKeyCode()
        
        if keycode == wx.WXK_SPACE or keycode==46 or keycode==44: #46 "."  44 ","
            #DictionaryField.SetLabel(StringValue)
            Output=""
            for i in range(len(StringValue)):
                Output=Output+StringValue[i]

            DictionaryField.SetLabel(Output)
            self.findDictionary(Output)
            del StringValue[:]
        else:
           if keycode>64 and keycode<123:
                StringValue.append(chr(keycode).lower())

    def findDictionary(self,word):
        with open('ejdic-hand-utf8.txt', 'r') as fp:
            for line in fp:
                line = line.rstrip()
                if line.find(word) != -1:

                    DictionaryField.SetValue(line)

                    break

app = wx.App(False)
frame = MainWindow(None, "pyTextDictionary")
app.MainLoop()