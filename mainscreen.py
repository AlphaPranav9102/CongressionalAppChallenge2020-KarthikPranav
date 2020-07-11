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

        #Set the iamge path for the display

        self.imagePath = "assets/TestImages/portraitTest.jpg"

        #Make an image widget and then use the ratio for further use - Not displayed

        self.mainScreenImageRatioGet = Image(
            source=self.imagePath,
            pos_hint={"top": 56/68, "x":0.1}
        )

        #Setting up image ratios and which side will be maximized

        if (Window.size[0]*0.8)/self.mainScreenImageRatioGet.texture_size[0] < (Window.size[1]*0.36)/self.mainScreenImageRatioGet.texture_size[1]:
            self.imageRatio = [Window.size[0]*0.8, (Window.size[0]*0.8)/self.mainScreenImageRatioGet.texture_size[0]*self.mainScreenImageRatioGet.texture_size[1]]
        else:
            self.imageRatio = [(Window.size[1]*0.36)/self.mainScreenImageRatioGet.texture_size[1]*self.mainScreenImageRatioGet.texture_size[0], (Window.size[1]*0.36)]

        #Drawing the image
        
        with self.canvasHolderLabel.canvas:
            #Drawing the border under the image iin relation to the ratio

            Color(*self.greyColorTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5-Window.size[0]*0.025, Window.size[1]*(169/272)-self.imageRatio[1]/2 - Window.size[1]*0.0125),
                size=(Window.size[0]*0.05 + self.imageRatio[0], Window.size[1]*0.025 + self.imageRatio[1])
                
            )

            #Drawing the image in relation to the ratio

            Color(*self.greyColorTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5, Window.size[1]*(169/272)-self.imageRatio[1]/2),
                size=self.imageRatio,
                source=self.imagePath
                
            )

        #Creating the dynamic speech prompter button for the user.

        self.promptStr = "Who are in the photo? What is the special moment in the photo?"

        self.mainScreenSpeechPromptButtonMiddle = Button(
            text=self.promptStr,
            size_hint=(0.9, 0.175),
            pos_hint={"top": 26/68, "x":0.05},
            color=self.darkBlueList,
            font_name="latoBold",
            halign="left",
            text_size=(self.size[0]*1.5, self.size[1]*1.25),
            valign="middle",
            background_normal="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicNormal.png",
            background_down="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicDown.png",
            border = [30, 30, 30, 30]
        )

        #Mkaing sure the text fits prefectly
        self.mainScreenSpeechPromptButtonMiddle.texture_update()

        self.mainScreenLayout.add_widget(self.mainScreenSpeechPromptButtonMiddle)

        #Adding the Assistant Icon to the Speech Prompt button above

        self.mainScreenSpeechPromptAssistantPic = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.14, 0.14),
            pos_hint={"top": 25/68, "x":0.08},
        )

        self.mainScreenLayout.add_widget(self.mainScreenSpeechPromptAssistantPic)

        #Creating the Lower Button that given the option to record text

        self.mainScreenEnterTextButtonLower = Button(
            text="Enter\nText",
            size_hint=(0.333, 0.156),
            pos_hint={"top": 6/34, "x":(1/2) - (1/6)},
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