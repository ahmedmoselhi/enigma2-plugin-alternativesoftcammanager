# uncompyle6 version 3.6.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (default, Jul 20 2020, 15:37:01)
# [GCC 7.5.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/Manager.py
# Compiled at: 2020-08-20 14:20:42
from __future__ import print_function
from enigma import eTimer
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.LoadPixmap import LoadPixmap
from enigma import getDesktop
import os
from . import _
from .Softcam import checkconfigdir, getcamcmd, getcamscript, stopcam
VERSION = ''
sz_w = getDesktop(0).size().width()
if sz_w == 1280:
    png_size = '_51x40'
else:
    png_size = '_76x60'


class AltCamManager(Screen):
    if sz_w == 1280:
        skin = '\n        <screen position="center,center" size="630,370" title="Alternative SoftCam Manager">\n        <eLabel position="5,0" size="620,2" backgroundColor="#aaaaaa" />\n        <eLabel position="340,15" size="2,300" backgroundColor="#aaaaaa" />\n        <widget source="list" render="Listbox" position="10,15" size="330,300" scrollbarMode="showOnDemand">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (45, 36), png = 1), \n                MultiContentEntryText(pos = (65, 10), size = (265, 36), font=0,                 flags = RT_HALIGN_LEFT, text = 0), \n                MultiContentEntryText(pos = (5, 25), size = (45, 16), font=1,                 flags = RT_HALIGN_CENTER, text = 2), \n                ],\n        "fonts": [gFont("Regular", 22),gFont("Regular", 10)],\n        "itemHeight": 44\n        }\n        </convert>\n        </widget>\n        <eLabel halign="center" position="375,10" size="210,35" font="Regular;18" text="Ecm info" transparent="1" />\n        <widget name="status" position="360,50" size="320,280" font="Regular;16"  halign="left" noWrap="1" />\n\n        <eLabel position="12,358" size="148,2" backgroundColor="#00ff2525" />\n        <eLabel position="165,358" size="148,2" backgroundColor="#00389416" />\n        <eLabel position="318,358" size="148,2" backgroundColor="#00baa329" />\n        <eLabel position="471,358" size="148,2" backgroundColor="#006565ff" />\n\n        <widget source="key_red" render="Label" position="12,328" zPosition="2" size="148,30"             valign="center" halign="center" font="Regular;22" transparent="1" />\n        <widget source="key_green" render="Label" position="165,328" zPosition="2" size="148,30"             valign="center" halign="center" font="Regular;22" transparent="1" />\n        <widget source="key_yellow" render="Label" position="318,328" zPosition="2" size="148,30"             valign="center" halign="center" font="Regular;22" transparent="1" />\n        <widget source="key_blue" render="Label" position="471,328" zPosition="2" size="148,30"             valign="center" halign="center" font="Regular;22" transparent="1" />\n\n        </screen>'
    else:
        skin = '\n        <screen position="center,center" size="1200,600" title="Alternative SoftCam Manager">\n        <eLabel position="5,0" size="1190,2" backgroundColor="#aaaaaa" />\n        <eLabel position="610,15" size="2,480" backgroundColor="#aaaaaa" />\n        <widget source="list" render="Listbox" position="10,15" size="600,480" scrollbarMode="showOnDemand">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (68, 54), png = 1), \n                MultiContentEntryText(pos = (90, 10), size = (510, 54), font=0,                 flags = RT_HALIGN_LEFT, text = 0), \n                MultiContentEntryText(pos = (5, 38), size = (68, 24), font=1,                 flags = RT_HALIGN_CENTER, text = 2), \n                ],\n        "fonts": [gFont("Regular", 34),gFont("Regular", 16)],\n        "itemHeight": 68\n        }\n        </convert>\n        </widget>\n        <eLabel halign="center" position="650,10" size="530,50" font="Regular;34" text="Ecm info" transparent="0" />\n        <widget name="status" position="650,70" size="530,450" font="Regular;28" halign="left" noWrap="1" />\n\n        <eLabel position="20,570"  size="290,5" backgroundColor="#00ff2525" />\n        <eLabel position="310,570" size="290,5" backgroundColor="#00389416" />\n        <eLabel position="600,570" size="290,5" backgroundColor="#00baa329" />\n        <eLabel position="890,570" size="290,5" backgroundColor="#006565ff" />\n\n        <widget source="key_red" render="Label" position="20,520" zPosition="2" size="290,50"             valign="center" halign="center" font="Regular;34" transparent="1" />\n        <widget source="key_green" render="Label" position="310,520" zPosition="2" size="290,50"             valign="center" halign="center" font="Regular;34" transparent="1" />\n        <widget source="key_yellow" render="Label" position="600,520" zPosition="2" size="290,50"             valign="center" halign="center" font="Regular;34" transparent="1" />\n        <widget source="key_blue" render="Label" position="890,520" zPosition="2" size="290,50"             valign="center" halign="center" font="Regular;34" transparent="1" />\n\n        </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setTitle(_('SoftCam Manager  %s') % VERSION)
        self.Console = Console()
        self['key_red'] = StaticText(_('Stop'))
        self['key_green'] = StaticText(_('Start'))
        self['key_yellow'] = StaticText(_('Restart'))
        self['key_blue'] = StaticText(_('Setup'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.cancel,
                                                                          'ok': self.ok,
                                                                          'green': self.start,
                                                                          'red': self.stop,
                                                                          'yellow': self.restart,
                                                                          'blue': self.setup})
        self['status'] = Label()
        self['list'] = List([])
        checkconfigdir()
        self.actcam = config.plugins.AltSoftcam.actcam.value
        self.camstartcmd = ''
        self.actcampng = LoadPixmap(resolveFilename(
            SCOPE_PLUGINS, 'Extensions/AlternativeSoftCamManager/images/actcam%s.png') % png_size)
        self.defcampng = LoadPixmap(resolveFilename(
            SCOPE_PLUGINS, 'Extensions/AlternativeSoftCamManager/images/defcam%s.png') % png_size)
        self.stoppingTimer = eTimer()
        try:
            self.stoppingTimer_conn = self.stoppingTimer.timeout.connect(
                self.stopping)
        except Exception:
            self.stoppingTimer.timeout.get().append(self.stopping)

        self.closestopTimer = eTimer()
        try:
            self.closestopTimer_conn = self.closestopTimer.timeout.connect(
                self.closestop)
        except Exception:
            self.closestopTimer.timeout.get().append(self.closestop)

        self.createinfo()
        self.Timer = eTimer()
        try:
            self.Timer_conn = self.Timer.timeout.connect(self.listecminfo)
        except Exception:
            self.Timer.callback.append(self.listecminfo)

        self.Timer.start(2000, False)

    def listecminfo(self):
        try:
            self['status'].setText(open('/tmp/ecm.info', 'r').read())
        except Exception:
            self['status'].setText(_('No ecm info'))

    def createinfo(self):
        self.iscam = False
        self.finish = False
        self.camliststart()
        self.listecminfo()

    def camliststart(self):
        if os.path.exists(config.plugins.AltSoftcam.camdir.value):
            self.softcamlist = os.listdir(
                config.plugins.AltSoftcam.camdir.value)
            if self.softcamlist:
                self.softcamlist.sort()
                self.iscam = True
                for x in self.softcamlist:
                    os.chmod(os.path.join(
                        config.plugins.AltSoftcam.camdir.value, x), 493)

                if self.actcam != 'none' and getcamscript(self.actcam):
                    self.createcamlist()
                else:
                    self.Console.ePopen('pidof %s' %
                                        self.actcam, self.camactive)
            else:
                self.finish = True
                self['list'].setList([])
        else:
            checkconfigdir()
            self.camliststart()

    def camactive(self, result, retval, extra_args):
        if result.strip():
            self.createcamlist()
        else:
            self.actcam = 'none'
            self.checkConsole = Console()
            for line in self.softcamlist:
                self.checkConsole.ePopen('pidof %s' %
                                         line, self.camactivefromlist, line)

            self.checkConsole.ePopen('echo 1', self.camactivefromlist, 'none')

    def camactivefromlist(self, result, retval, extra_args):
        if result.strip():
            self.actcam = extra_args
            self.createcamlist()
        else:
            self.finish = True

    def createcamlist(self):
        camlist = []
        if self.actcam != 'none':
            camlist.append((self.actcam, self.actcampng,
                           self.checkcam(self.actcam)))
        for line in self.softcamlist:
            if line != self.actcam:
                camlist.append((line, self.defcampng, self.checkcam(line)))

        self['list'].setList(camlist)
        self.finish = True

    def checkcam(self, cam):
        cam = cam.title()
        if getcamscript(cam):
            return 'Script'
        else:
            if cam[:5] in ('OSCam', 'GCam', 'NCam', 'Camd3', 'Newcs', 'Rucam'):
                return cam[:5]
            if cam[:4] in ('Mcas', 'Gbox', 'Mpcs', 'Mbox'):
                return cam[:4]
            cam = cam[:6]
            if 'Cccam' in cam:
                return 'CCcam'
            return cam

    def start(self):
        if self.iscam and self.finish:
            self.camstart = self['list'].getCurrent()[0]
            if self.camstart != self.actcam:
                print('[Alternative SoftCam Manager] Start SoftCam')
                self.camstartcmd = getcamcmd(self.camstart)
                self.session.open(MessageBox, _('Starting %s') %
                                  self.camstart, type=MessageBox.TYPE_INFO, timeout=3)
                self.stoppingTimer.start(100, False)

    def stop(self):
        if self.iscam and self.actcam != 'none' and self.finish:
            stopcam(self.actcam)
            self.session.open(MessageBox, _('Stopping %s') %
                              self.actcam, type=MessageBox.TYPE_INFO, timeout=3)
            self.actcam = 'none'
            self.closestopTimer.start(1000, False)

    def closestop(self):
        self.closestopTimer.stop()
        self.createinfo()

    def restart(self):
        if self.iscam and self.actcam != 'none' and self.finish:
            print('[Alternative SoftCam Manager] restart SoftCam')
            self.camstart = self.actcam
            if self.camstartcmd == '':
                self.camstartcmd = getcamcmd(self.camstart)
            self.session.open(MessageBox, _('Restarting %s') %
                              self.actcam, type=MessageBox.TYPE_INFO, timeout=3)
            self.stoppingTimer.start(100, False)

    def stopping(self):
        self.stoppingTimer.stop()
        stopcam(self.actcam)
        self.actcam = self.camstart
        service = self.session.nav.getCurrentlyPlayingServiceReference()
        if service:
            self.session.nav.stopService()
        self.Console.ePopen(self.camstartcmd)
        print('[Alternative SoftCam Manager] ', self.camstartcmd)
        if service:
            self.session.nav.playService(service)
        self.createinfo()

    def ok(self):
        if self.iscam and self.finish:
            if self['list'].getCurrent()[0] != self.actcam:
                self.start()
            else:
                self.restart()

    def cancel(self):
        if self.finish:
            if config.plugins.AltSoftcam.actcam.value != self.actcam:
                config.plugins.AltSoftcam.actcam.value = self.actcam
            config.plugins.AltSoftcam.save()
            self.close()
        else:
            self.cancelTimer = eTimer()
            try:
                self.cancelTimer_conn = self.cancelTimer.timeout.get().connect(self.listecminfo)
            except Exception:
                self.cancelTimer.timeout.get().append(self.setfinish)

            self.cancelTimer.start(4000, False)

    def setfinish(self):
        self.cancelTimer.stop()
        self.finish = True
        self.cancel()

    def setup(self):
        if self.finish:
            self.session.openWithCallback(self.createinfo, ConfigEdit)


class ConfigEdit(Screen, ConfigListScreen):
    if sz_w == 1280:
        skin = '\n        <screen name="ConfigEdit" position="center,center" size="620,200">\n            <eLabel position="5,0" size="610,2" backgroundColor="#aaaaaa" />\n            <widget name="config" position="20,20" size="580,100" zPosition="1"                 scrollbarMode="showOnDemand" />\n\n            <eLabel position="20,180"  size="140,5" backgroundColor="#00ff2525" />\n            <eLabel position="460,180" size="140,5" backgroundColor="#00389416" />\n\n            <widget source="key_red" render="Label" position="20,140" zPosition="2" size="140,40"                 valign="center" halign="center" font="Regular;22" transparent="1" />\n            <widget source="key_green" render="Label" position="460,140" zPosition="2" size="140,40"                 valign="center" halign="center" font="Regular;22" transparent="1" />\n\n            <widget source="about" render="Label" position="170,160" size="280,30" valign="center" halign="center" zPosition="2" foregroundColor="blue" font="Regular;14"/>\n\n            <widget name="HelpWindow" position="340,470" size="1,1" zPosition="5"                 pixmap="skin_default/vkey_icon.png" transparent="1" alphatest="on" />\n        </screen>'
    else:
        skin = '\n        <screen name="ConfigEdit" position="center,center" size="860,250">\n            <eLabel position="5,0" size="850,2" backgroundColor="#aaaaaa" />\n            <widget name="config" position="20,20" size="820,150" zPosition="1"                 scrollbarMode="showOnDemand" />\n\n            <eLabel position="20,240"  size="200,5" backgroundColor="#00ff2525" />\n            <eLabel position="640,240" size="200,5" backgroundColor="#00389416" />\n\n            <widget source="key_red" render="Label" position="20,200" zPosition="2" size="200,40"                 valign="center" halign="center" font="Regular;32" transparent="1" />\n            <widget source="key_green" render="Label" position="640,200" zPosition="2" size="200,40"                 valign="center" halign="center" font="Regular;32" transparent="1" />\n\n            <widget source="about" render="Label" position="230,200" size="400,40" valign="center" halign="center" zPosition="2" foregroundColor="blue" font="Regular;18"/>\n\n            <widget name="HelpWindow" position="520,680" size="1,1" zPosition="5"                 pixmap="skin_default/vkey_icon.png" transparent="1" alphatest="on" />\n        </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setTitle(_('SoftCam path configuration'))
        self['key_red'] = StaticText(_('Exit'))
        self['key_green'] = StaticText(_('Ok'))
        self['HelpWindow'] = Pixmap()
        self['about'] = StaticText('modified << python 3.10.2 >> 2022\n')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'cancel': self.cancel,
                                                                       'red': self.cancel,
                                                                       'ok': self.ok,
                                                                       'green': self.ok}, -2)
        configlist = []
        ConfigListScreen.__init__(self, configlist, session=session)
        configlist.append(getConfigListEntry(
            _('SoftCam config directory'), config.plugins.AltSoftcam.camconfig))
        configlist.append(getConfigListEntry(
            _('SoftCam directory'), config.plugins.AltSoftcam.camdir))
        configlist.append(getConfigListEntry(
            _("Show 'Restart softcam' in extensions menu"), config.plugins.AltSoftcam.restartext))
        self['config'].setList(configlist)

    def ok(self):
        msg = []
        if not os.path.exists(config.plugins.AltSoftcam.camconfig.value):
            msg.append('%s ' % config.plugins.AltSoftcam.camconfig.value)
        if not os.path.exists(config.plugins.AltSoftcam.camdir.value):
            msg.append('%s ' % config.plugins.AltSoftcam.camdir.value)
        if not msg:
            if config.plugins.AltSoftcam.camconfig.value[(-1)] == '/':
                config.plugins.AltSoftcam.camconfig.value = config.plugins.AltSoftcam.camconfig.value[
                    :-1]
            if config.plugins.AltSoftcam.camdir.value[(-1)] == '/':
                config.plugins.AltSoftcam.camdir.value = config.plugins.AltSoftcam.camdir.value[
                    :-1]
            config.plugins.AltSoftcam.save()
            self.close()
        else:
            self.session.open(MessageBox, _(
                'Directory %s does not exist!\nPlease set the correct directory path!') % msg, type=MessageBox.TYPE_INFO, timeout=5)

    def cancel(self, answer=None):
        if answer is None:
            if self['config'].isChanged():
                self.session.openWithCallback(self.cancel, MessageBox, _(
                    'Really close without saving settings?'))
            else:
                self.close()
        else:
            if answer:
                config.plugins.AltSoftcam.camconfig.cancel()
                config.plugins.AltSoftcam.camdir.cancel()
                self.close()
        return
