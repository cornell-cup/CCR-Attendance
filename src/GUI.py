from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
#from CCRAttendance import CCRAttendance 
import time

class User:
    def __init__(self):
        self.name = ""
        self.direction = ""
        self.row = ""
        self.greeting = ""
        self.meeting = ""
        self.team = ""

#node = CCRAttendanceNode("a","b","c")
#node.start_swipe_logging_job()
currentUser = User()

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
ScreenManagement:
    transition: FadeTransition()
    IdleScreen:
        id: idle
    MainScreen:
        id: main
    AnotherScreen:
        id: other
    MeetingScreen:
        id: meeting
    TeamScreen:
        id: teams

<IdleScreen>:
    name: "idle"
    Label: 
        text: "CORNELL CUP ATTENDANCE"
        font_size: 50

<MainScreen>:
    name: "main"
    Button:
        on_release: app.root.current = "other"
        text: 'Another Screen'
        font_size: 50
            
<AnotherScreen>:
    name: "other"
    Button:
        on_release: app.root.current = "main"
        text: 'back to the home screen'
        font_size: 50

<MeetingScreen>:
    name: "meeting"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: root.meeting_message
            font_size: 30
        Label:
            text: "What type of meeting are you signing in to?"
            font_size: 30
        BoxLayout:
            id: b1
            orientation: "horizontal"
            Button: 
                text: "Work Meeting"
                on_press: root.update_meeting("Work")
                on_release: app.root.current = "teams"
            Button: 
                text: "Dave Meeting"
                on_press: root.update_meeting("Dave")
                on_release: app.root.current = "teams"
            Button: 
                text: "Make-Up Meeting"
                on_press: root.update_meeting("Make-up")
                on_release: app.root.current = "teams"


<TeamScreen>:
    name: "teams"
    BoxLayout:
        orientation : "vertical"
        Label:
            text: root.team_messsage
            font_size: 30
        Label:
            text: "Which subteam are you on?"
            font_size: 30
        GridLayout:
            id: g1
            cols: 2
            Button: 
                text: "Wall"
                on_press: root.update_team("Wall")
                on_release: app.root.current = "idle"
            Button: 
                text: "Pogo"
                on_press: root.update_team("Pogo")
                on_release: app.root.current = "idle"
            Button: 
                text: "Minibot"
                on_press: root.update_team("Minibot")
                on_release: app.root.current = "idle"
            Button: 
                text: "Experimental"
                on_press: root.update_team("Experimental")
                on_release: app.root.current = "idle"

'''

class MeetingScreen(Screen):
    def __init__(self, **kwargs):
        super(MeetingScreen, self).__init__(**kwargs)
        if currentUser.direction == "IN":
            self.update_in()

    def update_in(self):
        print(currentUser.name)
        self.meeting_message = "Welcome, " + currentUser.name + "!"
        currentUser.greeting =  "Welcome, " + currentUser.name + "!"

    def update_meeting(self, meeting):
        currentUser.meeting = meeting

class TeamScreen(Screen):
    def __init__(self, **kwargs):
        super(TeamScreen, self).__init__(**kwargs)
        self.team_messsage = currentUser.greeting

    def update_team(self, team):
        currentUser.team = team


class MainScreen(Screen):
    pass

class AnotherScreen(Screen):
    pass

#CHECK IF PERSON IS SWIPED IN OR NOT 
#SIGN THEM OUT OR ASK THEM QUESTIONS

class IdleScreen(Screen):

    def __init__(self, **kwargs):
        super(IdleScreen, self).__init__(**kwargs)
        counter = 0
        while currentUser.name == "":
            # node.has_swipe_available():
            swipe = {"user": "Laura", "direction": "IN", "row": 1}  # node.pop_swipe()
            currentUser.name = swipe["user"]
            currentUser.direction = swipe["direction"]
            currentUser.row = swipe["row"]
            counter += 1
        Clock.schedule_once(self.switch, 1 / 60)
    def switch(self, dt):
        print(self)
        self.parent.current = "meeting"



class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_string(KV)


class MainApp(App):
    def build(self):
        return presentation

MainApp().run()