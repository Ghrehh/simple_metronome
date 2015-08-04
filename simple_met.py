import random
import wx

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(350,220), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetTitle('Simple Metronome')
        panel = wx.Panel(self)
        style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE

        self.can_call = True

        self.speed = 500
        self.go = False

        self.text = wx.StaticText(panel, style=style, label="1")
        self.text.SetForegroundColour((178, 0, 0))
        font = wx.Font(50, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)
        self.counter = 1

        self.sound1 = wx.Sound('met1.wav')
        self.sound2 = wx.Sound('met2.wav')

        self.cbtn = wx.Button(panel, label="Go", pos=(0, 166))
        self.cbtn.Bind(wx.EVT_BUTTON, self.gogo)

        self.sld = wx.Slider(panel, value=120, minValue=30, maxValue=300, pos=(90, 166),
            size=(200, -1), style=wx.SL_HORIZONTAL)
        self.sld.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
        self.txt = wx.StaticText(panel, label='120 BPM', pos=(292, 168))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.text, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)


    def on_timer(self):
        if not self.go:
            return
        if self.counter == 5:
            self.counter = 1
        self.text.SetLabel(str(self.counter))
        self.change_color()
        self.play_sound()
        self.counter +=1
        wx.CallLater(self.speed, self.on_timer)


    def play_sound(self):
        if self.counter == 1:
            self.sound1.Play(wx.SOUND_ASYNC)
        else:
            self.sound2.Play(wx.SOUND_ASYNC)


    def change_color(self):
            if self.counter == 4:
                self.text.SetForegroundColour((178, 0, 0))
            else:
                self.text.SetForegroundColour((0, 102, 255))


    def gogo(self, e):
        if self.go == False:
            self.go = True
            self.on_timer()
            self.cbtn.Label = "Stop"
        else:
            self.go = False
            self.cbtn.Label = "Go"


    def OnSliderScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()

        self.txt.SetLabel(str(val) + " BPM")
        self.speed = 60000 / val



app = wx.App()
frame = Frame(None)
frame.Show()
app.MainLoop()
