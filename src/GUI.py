from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.image import Image, AsyncImage
from kivy.core.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import BorderImage, Color, Rectangle, Line
from CCRAttendanceNode import CCRAttendanceNode
import time
import CCRResources
from CCRResources import res
from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')

CCRResources.populate("res")

class User:
    def __init__(self):
        self.name = ""
        self.id = ""
        self.direction = ""
        self.row = ""
        self.greeting = ""
        self.meeting = ""
        self.team = ""



KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import Clock kivy.clock.Clock
ScreenManagement:
    transition: FadeTransition()
    IdleScreen:
        id: idle
    MeetingScreen:
        id: meeting
    TeamScreen:
        id: teams
    DoneScreen:
        id: done
    GoodbyeScreen:
        id: goodbye
    
<IdleScreen>:
    name: "idle"
    canvas.before:
        Rectangle:
            pos : self.pos
            size : self.size
            Color:
                rgba: 1, 1, 1, 1
    Label: 
        text: "CORNELL CUP ATTENDANCE"
        color: 0,0,0,1
        font_size: 50
    
<GoodbyeScreen>:
    name: "goodbye"
    canvas.before:
        Rectangle:
            pos : self.pos
            size : self.size
            Color:
                rgba: 1, 1, 1, 1
    Label: 
        text: root.goodbye_message
        color: 0,0,0,1
        font_size: 60
    
<DoneScreen>:
    name: "done"
    canvas.before:
        Rectangle:
            pos : self.pos
            size : self.size
            Color:
                rgba: 1, 1, 1, 1
    BoxLayout:
        orientation: "vertical"
        Label:
            text: root.done_message
            color: 0,0,0,1
            font_size: 60
        Image:
            source: '../res/checkmark.png'
            size_hint: 0.3, 0.4
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        Label:
            text: "Thanks! You've been signed in."
            color: 0,0,0,1
            font_sze: 30
        
<MeetingScreen>:
    name: "meeting"
    canvas.before:
        Rectangle:
            pos : self.pos
            size : self.size
            Color:
                rgba: 1, 1, 1, 1
    BoxLayout:
        id: box_layout_top
        orientation: "vertical"
        Label:
            text: root.meeting_message
            color: 0,0,0,1
            font_size: 60
            
        Label:
            text: "What type of meeting are you signing in to?"
            color: 0,0,0,1
            font_size: 30

<TeamScreen>:
    name: "teams"
    canvas.before:
        Rectangle:
            pos : self.pos
            size : self.size
            Color:
                rgba: 1, 1, 1, 1
    BoxLayout:
        id: teams_box
        orientation : "vertical"
        Label:
            text: root.team_message
            color: 0,0,0,1
            font_size: 60
        Label:
            text: "Which subteam are you on?"
            color: 0,0,0,1
            font_size: 30
'''

currentUser = User()
node = CCRAttendanceNode(res("client_secret.json"), "CCR_Attendance_Node", res("db_config.json"))
#node.start_swipe_logging_job()
projects = node.db.get_projects_list()
meetings = node.db.get_meetings_list()


class DoneScreen(Screen):
    def __init__(self, **kwargs):
        super(DoneScreen, self).__init__(**kwargs)
        global currentUser
        self.done_message = currentUser.greeting
        currentUser = User()

    def on_enter(self):
        Clock.schedule_once(self.switch, 3)

    def switch(self, dt):
        self.manager.current = "idle"


class GoodbyeScreen(Screen):
    def __init__(self, **kwargs):
        super(GoodbyeScreen, self).__init__(**kwargs)
        global currentUser
        self.goodbye_message = "Goodbye, " + currentUser.name + "!"
        currentUser = User()

    def on_enter(self):
        Clock.schedule_once(self.switch, 3)

    def switch(self, dt):
        self.manager.current = "idle"


class MeetingScreen(Screen):
    meeting_message = StringProperty()
    def __init__(self, **kwargs):
        super(MeetingScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self,dt):
        for meeting in meetings:
            button = Button(text=meeting, font_size = 25)
            button.bind(on_press=lambda x : self.update_meeting(meeting))
            button.bind(on_release=self.move_to_team)
            self.ids.box_layout_top.add_widget(button)
        

        self.meeting_message = "Welcome, " + currentUser.name + "!"

    def update_meeting(self, meeting):
        currentUser.meeting = meeting

    def move_to_team(self,dt):
        self.manager.current = "teams"


class TeamScreen(Screen):
    def __init__(self, **kwargs):
        super(TeamScreen, self).__init__(**kwargs)
        self.team_message = currentUser.greeting
        Clock.schedule_once(self._finish_init)

    def move_to_done(self, *args):
        self.manager.current = "done"
        node.log_swipe_in(currentUser.id, currentUser.meeting,
                          currentUser.team)

    def _finish_init(self, dt):
        grid_layout = GridLayout(cols=2)
        for project in projects:
            button = Button(text=project, font_size = 25)
            button.bind(on_press=lambda x : self.update_team(project))
            button.bind(on_release=self.move_to_done)
            grid_layout.add_widget(button)

        self.ids.teams_box.add_widget(grid_layout)

    def update_team(self, team):
        currentUser.team = team

class IdleScreen(Screen):
    def __init__(self, **kwargs):
        super(IdleScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.user_swiped)
        #Clock.schedule_once(node.async_get_user_swipe(self.user_swiped))

    def user_swiped(self,dt):
        currentUser.id = id
        self.manager.current = "meeting"

class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_string(KV)


class MainApp(App):
    def build(self):
        return presentation


MainApp().run()