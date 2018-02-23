from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

KV = '''

<Greeting>:
    title: "Greeting"
    message: message
    id: label
    content: b1
    BoxLayout:
        id: b1
        Label: 
            id: message
            text: ""
            font_size: 40

'''

class Greeting(Label):
    
    def set_label(self, name):
        

class GUIApp(App):
    def build(self):
        return Label(text='Hello World')

GUIApp().run()