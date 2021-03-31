#-*- coding: utf-8 -*-

import wx
from wx.lib.wordwrap import wordwrap
from wx import adv

__author__ = 'WellenWoo'

class layout_template():
    def About_info(self,name,version,cr,des,website,developers,client):
#        info = wx.AboutDialogInfo() #wx2.8
        info = adv.AboutDialogInfo() #wx4.0
        info.Name = name
        info.Version = version
        info.Copyright = cr
        info.Description = wordwrap(des,350,client)
        info.WebSite = (website, "feedback")
        info.Developers = [developers]
        return info
