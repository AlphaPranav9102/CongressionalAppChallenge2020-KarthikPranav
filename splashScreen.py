from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


class splashScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(splashScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        Window.clearcolor = self.greyColorTuple

        self.mainScreenSpeechPromptAssistantPic = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.7, 0.35),
            pos_hint={"top": 58/68, "x":0.15},
        )

        self.add_widget(self.mainScreenSpeechPromptAssistantPic)

        self.mainScreenTopLabel = Label(
            text='Vocate',
            size=(Window.size[0], Window.size[1]*0.16),
            pos=(0, 0),
            size_hint=(1, 0.175), 
            pos_hint={"x":0, "top": 0.5},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=38,
        )
        self.add_widget(self.mainScreenTopLabel)
        Clock.schedule_once(self.screenTransition, 4)

    def screenTransition(self, dt):
        Vocate().sm.current = "mainScreen"

    

        