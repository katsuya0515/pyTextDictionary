import os
import wx
import re

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,600))
       # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A StatusBar in the bottom of the window

        #Setting up the panel (Left:Text Right:Serach Bar + Dictionary)
        root_panel = wx.Panel(self,wx.ID_ANY)
        right_panel =wx.Panel(self,wx.ID_ANY)


        global TextField
        TextField = wx.TextCtrl(root_panel, style=wx.TE_MULTILINE,size=(500,600))

        global DictionaryField
        style =   wx.TE_NO_VSCROLL | wx.TE_MULTILINE
        DictionaryField = wx.TextCtrl(right_panel, style=style,size=(500,570))
        font = wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        DictionaryField.SetFont(font)
        DictionaryField.Disable()

        global SerchField
        SerchField=wx.TextCtrl(right_panel,wx.ID_ANY,size=(500,30))



        right_layout=wx.BoxSizer(wx.VERTICAL)
        right_layout.Add(SerchField,flag=wx.GROW)
        right_layout.Add(DictionaryField,flag=wx.GROW,proportion=1)
        right_panel.SetSizer(right_layout)
        right_layout.Fit(right_panel)


        root_layout = wx.BoxSizer(wx.HORIZONTAL)
        root_layout.Add(TextField,flag=wx.GROW,proportion=1)
        root_layout.Add(right_panel,flag=wx.GROW,proportion=1)

        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)
    
        
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
        SerchField.Bind(wx.EVT_KEY_UP,self.searchDictionary)
        self.Show(True)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

#入力されているkeyをspaceがうたれる前に配列で補完。spaceがうたれたらその単語をfindDictionaryメッソドに送る
    def changeDictionary(self,evt):
        keycode=evt.GetKeyCode()
        
        if keycode == wx.WXK_SPACE or keycode==46 or keycode==44: #space or 46 "." or 44 ","
            Output=""
            for i in range(len(StringValue)):
                Output=Output+StringValue[i]

            DictionaryField.SetLabel(Output)
            self.findDictionary(Output)
            del StringValue[:]
        else:
           if keycode>64 and keycode<123:
                StringValue.append(chr(keycode).lower())
#Search　barの単語から
    def searchDictionary(self,evt):
        keycode=evt.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.findDictionary(SerchField.GetValue().lower())

#辞書から検索する
    def findDictionary(self,word):
        with open('ejdic-hand-utf8.txt', 'r') as fp:
            for line in fp:
               
                line=line.rstrip()
                if re.match(word,line):

                    DictionaryField.SetValue(line)

                    break
                else:
                    DictionaryField.SetValue('No result')
app = wx.App(False)
frame = MainWindow(None, "pyTextDictionary")
app.MainLoop()