#This project is by Pranav and Karthik for the Congression App Challenge (CAC2020).

#Imported Kivy

import kivy

kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import RoundedRectangle, Line
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen


Window.size = (350, 700)
Window.clearcolor = (250/255, 250/255, 250/255, 255/255)

#Imported Lato Fonts

LabelBase.register(
    name="latoBold",
    fn_regular="Fonts/Lato-Bold.ttf"
)

LabelBase.register(
    name="latoBlack",
    fn_regular="Fonts/Lato-Black.ttf"
)


class TestApp(App, Widget):
    def mainScreen(self):

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        # Creating float layout for main screen
        self.mainScreenLayout = FloatLayout()

        self.canvasHolderLabel = Label(size=(Window.size[0], Window.size[1]*0.175))
        self.mainScreenLayout.add_widget(self.canvasHolderLabel)

        #Drawing the rounded rectangle under the main header -- Not Scalable

        with self.canvasHolderLabel.canvas:
            Color(*self.greyColorTuple)
            RoundedRectangle(
                segments=100,
                radius=[(0, 0), (0, 0), (35.0, 35.0), (0, 0)],
                pos=(0, Window.size[1]-Window.size[1]*0.175),
                size=(Window.size[0], Window.size[1]*0.175)
                
            )

        #Creating the main header at the top - Semi Scalable

        self.mainScreenTopLabel = Label(
            text='Welcome Back!',
            size=(Window.size[0], Window.size[1]*0.16),
            pos=(0, 0),
            size_hint=(1, 0.175), 
            pos_hint={"x":0, "top": 1},
            color=self.darkBlueList,
            font_name="latoBlack",
            font_size=32,
        )
        self.mainScreenLayout.add_widget(self.mainScreenTopLabel)

        #Drawing the rounded rectangle under the image

        with self.canvasHolderLabel.canvas:
            Color(*self.greyColorTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.05, Window.size[1]*(66/136)),
                size=(Window.size[0]*0.9, Window.size[1]*0.275)
                
            )

        #Creating the iamge prompt slot for the user

        self.mainScreenImagePlacementTop = Image(
            source="assets/TestImages/BeachImageTest.jpg",
            size_hint=(0.8, 0.4),
            pos_hint={"top": 56/68, "x":0.1},
            allow_stretch=True
        )

        self.mainScreenLayout.add_widget(self.mainScreenImagePlacementTop)

        #Create Rounded corners for image

        with self.mainScreenImagePlacementTop.canvas:
            Color(*self.greyColorList)
            Line(
                rounded_rectangle = (
                    Window.size[0]*0.1, #x
                    Window.size[1]*(68/136), #y
                    Window.size[0]*0.8, #width
                    Window.size[1]*0.25, #height
                    25, #c1
                    25, #c2
                    25, #c3
                    25 #c4
                ),
                width=5.2
            )

        #Creating the dynamic speech prompter button for the user.

        self.mainScreenSpeechPromptButtonMiddle = Button(
            text="Who all are in this photo?",
            size_hint=(0.9, 0.175),
            pos_hint={"top": 15/34, "x":0.05},
            color=self.darkBlueList,
            font_name="latoBold",
            font_size=int(Window.size[0]/13.6),
            halign="left",
            text_size=(self.size[0]*1.75, self.size[1]),
            valign="middle",
            background_normal="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicNormal.png",
            background_down="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicDown.png",
            border = [30, 30, 30, 30]
        )

        self.mainScreenLayout.add_widget(self.mainScreenSpeechPromptButtonMiddle)

        #Adding the Assistant Icon to the Speech Prompt button above

        self.mainScreenSpeechPromptAssistantPic = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.14, 0.14),
            pos_hint={"top": 29/68, "x":0.08},
        )

        self.mainScreenLayout.add_widget(self.mainScreenSpeechPromptAssistantPic)

        #Creating the Lower Button that given the option to record text

        self.mainScreenEnterTextButtonLower = Button(
            text="Enter\nText",
            size_hint=(0.333, 0.156),
            pos_hint={"top": 7/34, "x":(1/2) - (1/6)},
            color=self.whiteList,
            font_name="latoBold",
            font_size=22,
            halign="left",
            background_normal="assets/mainScreenEnterTextButtonLower/DarkBlueRoundedButtonPicNormal.png",
            background_down="assets/mainScreenEnterTextButtonLower/DarkBlueRoundedButtonPicDown.png",
            border = [-0, -0, -0, -0]
        )
        

        self.mainScreenLayout.add_widget(self.mainScreenEnterTextButtonLower)
        

        return(self.mainScreenLayout)
    
    def build(self):
        return(TestApp.mainScreen(self))

TestApp().run()
