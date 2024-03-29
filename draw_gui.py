# -*- coding: utf-8 -*-

import wx
import os
from os import path
from collections import namedtuple
import  wx.lib.rcsizer  as rcs
from wordcloud import STOPWORDS
from wx import adv

from utility_template import layout_template
import wordcloud_gen as wcg
import wx.lib.agw.gradientbutton as gbtn

__author__ = 'WellenWoo'
__mail__ = 'wellenwoo@163.com'

imgformat = "jpg (*.jpg)|*.jpg|"     \
           "jpeg(*.jpeg) |*.jpeg|"\
           "png(*.png) |*.png|"\
           "tiff(*.tif) |*.tiff|"\
           "All files (*.*)|*.*"

txtformat = "txt (*.txt)|*.txt|"\
            "All files (*.*)|*.*"

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(600,-1))
        Size = namedtuple("Size",['x','y'])
        s = Size(100,50)

        self.cn_text = None
        self.en_text = None
        cwd = os.getcwd()
        self.mask_path = path.join(path.abspath(cwd),'alice_mask.png')
        self.user_sw = STOPWORDS

        self.lt = layout_template()
        self.name = 'WordCloud draw'
        self.version = '0.2'
        self.des = '''Draw the word cloud.\n'''
        self.git_website = "https://github.com/WellenWoo/WordCloud_draw"
        self.copyright = "(C) 2018 All Right Reserved"
        
        """创建菜单栏"""
        filemenu = wx.Menu()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit\tCtrl+Q","Tenminate the program")

        confmenu = wx.Menu()
        menuSw = confmenu.Append(wx.ID_ANY,"StopWords","Add user StopWrods dict")
        menuMask = confmenu.Append(wx.ID_ANY,"Mask","Set mask")
        
        helpmenu = wx.Menu ()
        menuAbout = helpmenu.Append(wx.ID_ABOUT ,"&About","Information about this program")

        menuBar = wx.MenuBar ()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(confmenu,"&Configure")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar)
        
        """创建输入框"""
        self.in1 = wx.TextCtrl(self,-1,size = (2*s.x,s.y))

        """创建按钮"""
        b1 = gbtn.GradientButton(self, -1, label = "text")
        b2 = gbtn.GradientButton(self, -1, label = "run")

        """设置输入框的提示信息"""
        self.in1.SetToolTipString('choose a text file')

        """界面布局"""
        self.sizer0 = rcs.RowColSizer()
        self.sizer0.Add(b1,row = 1,col = 1)
        self.sizer0.Add(self.in1,row = 1,col = 2)
        self.sizer0.Add(b2,row = 1,col = 3)

        """绑定回调函数"""
        self.Bind(wx.EVT_BUTTON, self.choose_cn, b1)
        self.Bind(wx.EVT_BUTTON, self.draw_cn, b2)

        '''菜单绑定函数'''
        self.Bind(wx.EVT_MENU,self.OnExit,menuExit)
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)
        
        self.Bind(wx.EVT_MENU,self.get_stopwords,menuSw)
        self.Bind(wx.EVT_MENU,self.get_mask,menuMask)
        
        self.SetSizer(self.sizer0)
        self.SetAutoLayout(1)
        self.sizer0.Fit(self)
        self.CreateStatusBar()
        self.Show(True)

    def get_stopwords(self,evt):
        fn = self.choose_file(txtformat)
        if fn is None:
            return None
        else:
            self.user_sw = wcg.user_stopwords(fn)

    def get_mask(self,evt):
        temp = self.choose_file(imgformat)
        if temp is not None:
            self.mask_path = temp

    def choose_cn(self,evt):
        """Choose a Chinses text file"""
        self.cn_text = None
        self.cn_text = self.choose_file(txtformat)
        if self.cn_text is None:
            pass
        else:
            self.in1.Clear()
            self.in1.write(self.cn_text)
            
    def choose_file(self,wildcard):
        '''choose img'''
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
#            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR #wx2.8
            style = wx.FD_OPEN | wx.FD_MULTIPLE |     #wx4.0
                    wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                    wx.FD_PREVIEW
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            dlg.Destroy()
            return paths[0]
        else:
            return None

    def draw_cn(self,evt):
        if self.cn_text is None:
            self.raise_msg(u'plaese Choose a Chinses text file first.')
            return None
        else:
            text = wcg.get_text_cn(self.cn_text)
            wcg.draw_wc(text,self.mask_path,self.user_sw)

    def raise_msg(self,msg):
        '''add the warning message'''
#        info = wx.AboutDialogInfo() #wx2.8
        info = adv.AboutDialogInfo() #wx4.0
        info.Name = "Warning Message"
        info.Copyright = msg
#        wx.AboutBox(info) wx2.8
        adv.AboutBox(info) #wx4.0

    def OnAbout(self, evt):
        info = self.lt.About_info(self.name,self.version,self.copyright,
                                  self.des,self.git_website,
                                  __author__+'\n'+__mail__,wx.ClientDC(self))    
#        wx.AboutBox(info) wx2.8
        adv.AboutBox(info) #wx4.0
        
    def OnExit(self,event):
        """退出函数"""
        self.Close()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None,'WordCloud_draw')
    app.MainLoop()
    
