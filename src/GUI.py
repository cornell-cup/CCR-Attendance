from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import time


KV = '''

#:import Clock kivy.clock.Clock
<Greeting>:
    title: "Greeting"
    message: message
    id: popup
    content: b1
    BoxLayout:
        id: b1
        Label: 
            id: message
            text: ""
            font_size: 40
        Button:
            text: "Confirmed!"
            on_release: popup.dismiss()
    
PILayout:
    orientation: "vertical"
    Label:
        text: "Cornell Cup"
    Button: 
        text: "Sign In/Out"
        on_release:
            root.greetingLabel.open()
            root.greetingLabel.set_welcome("Conan")
            Clock.schedule_once(root.greetingLabel.clear_label, 5)


'''

class Greeting(Popup):
    
    def set_welcome(self, name):
        self.message.text = "Welcome " + name

    def set_goodbye(self, name):
        self.message.text = "Goodbye " + name
    
    def clear_label(self, dt):
        self.message.text = ""

class PILayout(BoxLayout):

    def __init__(self, **kwargs):
        super(PILayout, self).__init__(**kwargs)
        self.greetingLabel = Greeting()

class GUIApp(App):
    def build(self):
        return Builder.load_string(KV)

GUIApp().run()