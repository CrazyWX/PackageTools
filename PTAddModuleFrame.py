#!/usr/bin/env python
import wx
import os
from PTDBManager import PTDBManager
from PTModule import  PTModule

class PTAddModuleFrame (wx.Frame):
    localPathTip = None
    localPathText = None
    localPathBtn = None

    remotePathTextTip = None
    remotePathText = None
    remotePathUserTip = None
    remotePathUser = None
    remotePathPwdTip = None
    remotePathPwd = None

    specRepoTip = None
    specRepoChoice = None

    addBtn = None

    callback = None

    specRepoList = None
    selectedSpecRepo = None

    def __init__(self, parent, callback, specRepoList):
        windowSize = wx.DisplaySize()

        size = (600,290)
        pos = ((windowSize[0] - size[0])/2,(windowSize[1] - size[1])/2)
        wx.Frame.__init__(self, parent, wx.ID_ANY, u"Add module", pos=pos, size=size)
        self.SetMinSize(size)

        self.specRepoList = specRepoList
        self.callback = callback

        gridSizer = wx.FlexGridSizer(5, 2, 10, 10)

        # Local path
        self.localPathTip = wx.StaticText(self)
        self.localPathTip.SetLabelText(u"Local path :")
        gridSizer.Add(self.localPathTip, 0)

        self.localPathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_READONLY,size=(400, 22))
        self.localPathBtn = wx.Button(self, wx.ID_ANY, u"Choose")
        self.localPathBtn.Bind(wx.EVT_BUTTON, self.OnChooseDirectory)

        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.localPathText, 1, wx.EXPAND|wx.RIGHT, 10)
        hBox.Add(self.localPathBtn, 0)
        gridSizer.Add(hBox, 1, wx.EXPAND)

        self.remotePathTextTip = wx.StaticText(self)
        self.remotePathTextTip.SetLabelText(u"SVN URL :")
        gridSizer.Add(self.remotePathTextTip, 0)

        self.remotePathText = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(400, 22))
        gridSizer.Add(self.remotePathText, 1, wx.EXPAND)

        self.remotePathUserTip = wx.StaticText(self)
        self.remotePathUserTip.SetLabelText(u"Account :")
        gridSizer.Add(self.remotePathUserTip, 0)

        self.remotePathUser = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT, size=(200, 22))
        gridSizer.Add(self.remotePathUser, 1, wx.EXPAND)

        self.remotePathPwdTip = wx.StaticText(self)
        self.remotePathPwdTip.SetLabelText(u"Password :")
        gridSizer.Add(self.remotePathPwdTip, 0)

        self.remotePathPwd = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_LEFT | wx.TE_PASSWORD,size=(200, 22))
        gridSizer.Add(self.remotePathPwd, 1, wx.EXPAND)

        # Spec repo
        self.specRepoTip = wx.StaticText(self)
        self.specRepoTip.SetLabelText(u"Spec repo :")
        gridSizer.Add(self.specRepoTip, 0)

        specRepoChoiceList = ['None']
        for specRepo in specRepoList:
            specRepoChoiceList.append(specRepo.name)
        self.specRepoChoice = wx.Choice(self, wx.ID_ANY, choices=specRepoChoiceList, name=u"Spec repo list")
        self.specRepoChoice.Bind(wx.EVT_CHOICE, self.OnChoiceSpecRepo)
        gridSizer.Add(self.specRepoChoice, 1, wx.EXPAND)

        gridSizer.AddGrowableCol(1)

        # Add btn
        self.addBtn = wx.Button(self, wx.ID_ANY, u"Add")
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddModule)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 1, wx.EXPAND|wx.ALL, 30)
        sizer.Add(self.addBtn, 0, wx.CENTER|wx.BOTTOM, 30)

        self.SetSizer(sizer)
        self.Show(True)

    def OnChoiceSpecRepo(self, event):
        findSpecRepo = None
        for specRepo in self.specRepoList:
            if specRepo.name == event.String:
                findSpecRepo = specRepo
                break
        self.selectedSpecRepo = findSpecRepo

    def OnChooseDirectory(self, event):
        dirDlg = wx.DirDialog(self, u"Choose directory", os.path.expanduser('~'), wx.DD_DEFAULT_STYLE)
        if dirDlg.ShowModal() == wx.ID_OK:
            self.localPathText.SetValue(dirDlg.GetPath())

    def OnAddModule(self, event):
        module = PTModule()
        module.localPath = self.localPathText.GetValue()
        module.remotePath = self.remotePathText.GetValue()
        module.username = self.remotePathUser.GetValue()
        module.password = self.remotePathPwd.GetValue()
        module.name = os.path.basename(module.localPath)
        if self.selectedSpecRepo != None:
            module.specRepoId = self.selectedSpecRepo.id
        else:
            module.specRepoId = 0

        if len(module.localPath) > 0 and len(module.remotePath) > 0 and len(module.username) > 0 and len(module.password) > 0 and module.specRepoId > 0:
            PTDBManager().addNewModule([module], self.AddModuleCallback)
        else:
            wx.MessageBox(u"Should fill all inputs.", u"Error", wx.OK | wx.ICON_INFORMATION)

    def AddModuleCallback(self, moduleList):
        if self.callback != None:
            self.callback(moduleList)