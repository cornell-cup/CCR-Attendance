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
import signal

Config.set('graphics','show_cusor',0)
Config.write()
CCRResources.populate("res")
node = None
meetings = []
projects = []

def do_connect():
    try:
        global node
        global meetings
        global projects
        node = CCRAttendanceNode(res("client_secret.json"), "CCR_Attendance_Node", res("db_config.json"))
        meetings = node.get_meetings()
        projects = node.get_projects()
    except Exception:
            time.sleep(10)
            print "Failed to connect. Trying again in 10 seconds."
            do_connect()

def end_read(signal,frame):
    print "Ctrl+C captured, ending....."
    node.stop_swipe_logging_job()
    App.get_running_app().stop()
    exit(0)

signal.signal(signal.SIGINT,end_read)

class User:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.direction = ""
        self.row = ""
        self.greeting = ""
        self.meeting = ""
        self.team = ""
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
        self.goodbye_message = "Goodbye, " + currentUser.name[:currentUser.name.find(" ")] + "!"
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
        self.meeting_message = "Welcome, " + currentUser.name[:currentUser.name.find(" ")] + "!"
        
    def _finish_init(self,dt):
        for meeting in meetings:
            button = Button(text=meeting, font_size = 25)
            button.bind(on_press=lambda x, m=meeting:self.update_meeting(m))
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
        node.log_swipe_in(currentUser.id, currentUser.name, currentUser.meeting, currentUser.team)
        self.manager.current = "done"

    def _finish_init(self, dt):
        self.team_message = currentUser.greeting
        grid_layout = GridLayout(rows=2)

        for project in projects:
            button = Button(text=project, font_size = 40)
            button.bind(on_press=lambda x, p=project:self.update_team(p))
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

do_connect()

presentation = Builder.load_file(res("gui.kv"))

class CCRAttendanceApp(App):
    def build(self):
        return presentation

    def reload_meetings_and_projects(self):
        global projects 
        global meetings 
        projects = node.db.get_projects_list()
        meetings = node.db.get_meetings_list()

CCRAttendanceApp().run()
