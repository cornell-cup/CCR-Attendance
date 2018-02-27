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
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import BorderImage, Color, Rectangle, Line
from CCRAttendanceNode import CCRAttendanceNode
import time
import CCRResources
from CCRResources import res
from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics','show_cusor',0)
Config.write()
CCRResources.populate("res")

class User:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.direction = ""
        self.row = ""
        self.greeting = ""
        self.meeting = ""
        self.team = ""



KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import Clock kivy.clock.Clock
ScreenManagement:
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
    AnchorLayout:
        id: scanning_anchor
        anchor_x:'center'
        anchor_y:'bottom'
        Label: 
            id: scanning_text
            size_hint: None, None
            text: "SCANNING FOR ID"
            color: .61,.61,.61,1
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
            font_sze: 60
        
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
            font_size: 40

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
            font_size: 40

<LoadingWidget>:
    Image:
        source: '../res/logo.png'
        center: self.parent.center
        size: 256, 256
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                origin: self.center
        canvas.after:
            PopMatrix
        
'''

node = CCRAttendanceNode(res("client_secret.json"), "CCR_Attendance_Node", res("db_config.json"))
meetings = node.get_meetings()
projects = node.get_projects()
currentUser = User()

class DoneScreen(Screen):
    done_message = StringProperty()
    def __init__(self, **kwargs):
        super(DoneScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        global currentUser
        self.done_message = currentUser.greeting
        currentUser = User()
        Clock.schedule_once(self.switch, 3)

    def switch(self, dt):
        self.manager.current = "idle"


class GoodbyeScreen(Screen):
    goodbye_message = StringProperty()
    def __init__(self, **kwargs):
        super(GoodbyeScreen, self).__init__(**kwargs)
        
    def on_enter(self):
        global currentUser
        self.goodbye_message = "Goodbye, " + currentUser.name + "!"
        currentUser = User()
        Clock.schedule_once(self.switch, 3)

    def switch(self, dt):
        self.manager.current = "idle"


class MeetingScreen(Screen):
    meeting_message = StringProperty()
    def __init__(self, **kwargs):
        super(MeetingScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
    
    def on_enter(self):
        global currentUser
        self.meeting_message = "Welcome, " + currentUser.name + "!"
        
    def _finish_init(self,dt):
        for meeting in meetings:
            button = Button(text=meeting, font_size = 25)
            button.bind(on_press=lambda x : self.update_meeting(meeting))
            button.bind(on_release=self.move_to_team)
            self.ids.box_layout_top.add_widget(button)

    def update_meeting(self, meeting):
        global currentUser
        currentUser.meeting = meeting

    def move_to_team(self,dt):
        self.manager.current = "teams"


class TeamScreen(Screen):
    team_message = StringProperty()
    def __init__(self, **kwargs):
        super(TeamScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def move_to_done(self, *args):
        node.log_swipe_in(currentUser.id, currentUser.meeting, currentUser.team)
        self.manager.current = "done"

    def _finish_init(self, dt):
        self.team_message = currentUser.greeting
        grid_layout = GridLayout(rows=2)

        for project in projects:
            button = Button(text=project, font_size = 40)
            button.bind(on_press=lambda x : self.update_team(project))
            button.bind(on_release=self.move_to_done)
            grid_layout.add_widget(button)

        self.ids.teams_box.add_widget(grid_layout)

    def update_team(self, team):
        global currentUser
        currentUser.team = team

class LoadingWidget(Widget):
    angle = NumericProperty(0)
    def __init__(self,**kwargs):
        super(LoadingWidget, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2) 
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)        

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

class IdleScreen(Screen):
    def __init__(self, **kwargs):
        super(IdleScreen, self).__init__(**kwargs)
        self.add_widget(LoadingWidget())
        Clock.schedule_once(self.start_fade_in)
        
    def on_enter(self):
        self.start_swipe_job()

    def start_swipe_job(self,*args):
        if node.has_reader():
            node.async_get_user_name_swipe(self.user_swiped)
        elif node.has_swipe_available():
            id,name = node.pop_swipe()
            self.user_swiped(id,name)
    
    def start_fade_in(self,*args):
        anim = Animation(color=[0.61,0.61,0.61,0.0],duration=1.0)
        anim.bind(on_complete=self.start_fade_out)
        anim.start(self.ids.scanning_text)

    def start_fade_out(self,*args):
        anim = Animation(color=[0.61,0.61,0.61,1.0],duration=1.5)
        anim.bind(on_complete=self.start_fade_in)
        anim.start(self.ids.scanning_text)

    def user_swiped(self,id,name):
        global currentUser
        currentUser.name = name
        currentUser.id = id
        if node.is_user_swiped_in(id):
            node.log_swipe_out(id)
            self.manager.current = "goodbye"
        else:
            self.manager.current = "meeting"
        
class ScreenManagement(ScreenManager):
    pass 

presentation = Builder.load_string(KV)

class CCRAttendanceApp(App):
    def build(self):
        return presentation

    def reload_meetings_and_projects(self):
        global projects 
        global meetings 
        projects = node.db.get_projects_list()
        meetings = node.db.get_meetings_list()

CCRAttendanceApp().run()
