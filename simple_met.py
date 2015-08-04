import wx

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(350,220), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetTitle('Simple Metronome')
        panel = wx.Panel(self)
        style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE

        self.current_bpm = 120

        self.speed = 500
        self.go = False

        self.top = 4
        self.bottom = 4

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

        self.comboTop = wx.ComboBox(panel, pos=(0, 0), value="4", style=wx.CB_READONLY, choices=['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'])
        self.comboTop.Bind(wx.EVT_COMBOBOX, self.OnWidgetEnterTop)

        self.comboBottom = wx.ComboBox(panel, pos=(0, 25), value="4", style=wx.CB_READONLY, choices=['4', '8', '16'])
        self.comboBottom.Bind(wx.EVT_COMBOBOX, self.OnWidgetEnterBottom)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.text, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)


    def on_timer(self):
        if not self.go:
            return
        if self.counter == self.top + 1:
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
            if self.counter == self.top:
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

        self.current_bpm = val
        self.txt.SetLabel(str(val) + " BPM")
        self.speed = (240000 / val) / self.bottom

    def OnWidgetEnterTop(self, e):

        obj = e.GetEventObject()
        val = obj.GetValue()

        self.comboTop.SetLabel(val)
        self.top = int(val)

    def OnWidgetEnterBottom(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()

        self.comboBottom.SetLabel(val)
        self.bottom = int(val)

        self.speed = (240000 / self.current_bpm ) / self.bottom



app = wx.App()
frame = Frame(None)
frame.Show()
app.MainLoop()
