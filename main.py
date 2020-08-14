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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.graphics import Ellipse
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics.vertex_instructions import RoundedRectangle, Line
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView

import pyaudio

import wave

import speech_recognition as sr

import shutil
import csv

widthInput = 350

Window.size = (widthInput, widthInput*2)
Window.clearcolor = (250/255, 250/255, 250/255, 255/255)

#Imported Lato and Montserrat Fonts

LabelBase.register(
    fn_regular="Fonts/Lato-Regular.ttf",
    name="latoRegular"
)

LabelBase.register(
    fn_regular="Fonts/Lato-Bold.ttf",
    name="latoBold"
)

LabelBase.register(
    name="latoBlack",
    fn_regular="Fonts/Lato-Black.ttf"
)

LabelBase.register(
    name="montserratExtraBold",
    fn_regular="Fonts/Montserrat-ExtraBold.ttf"
)

LabelBase.register(
    name="montserratRegular",
    fn_regular="Fonts/Montserrat-Regular.ttf"
)


class recordingScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(recordingScreen, self).__init__(**kwargs)

        #Initializing all of the needed main theme colors

        self.lightGreyColorTuple = (243/255, 243/255, 243/255, 243/255)
        self.lightGreyColorList = [243/255, 243/255, 243/255, 243/255]

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.appBackgroundTuple = (250/255, 250/255, 250/255, 255/255)
        self.appBackgroundList = [250/255, 250/255, 250/255, 255/255]

        #Add background

        Window.clearcolor = self.appBackgroundTuple

        #Add variables for screen

        self.firstRecord = False

        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44032
        self.RECORD_SECONDS = 7
        self.WAVE_OUTPUT_FILENAME = "output.wav"

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        self.startRecord = False

        self.frames = []

        #Make a testing canvasHolder

        self.canvasHolderLabel = Label(size=(Window.size[0], Window.size[1]*0.175))
        

        #Drawing the rounded rectangle under the main header -- Not Scalable

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.labelRect = RoundedRectangle(
                segments=100,
                radius=[(0, 0), (0, 0), (35.0, 35.0), (0, 0)],
                pos=(0, Window.size[1]-Window.size[1]*0.175),
                size=(Window.size[0], Window.size[1]*0.175),
                source="assets/general/GreyBackground.png"
                
            )

        self.add_widget(self.canvasHolderLabel)

        #Add button which goes back to previous screen.

        self.backButton = Button(
            size_hint=(0.13, 0.05),
            pos_hint={"top": 127/136, "x": 0.06},
            background_normal="assets/backButton/backButtonNormal.png",
            background_down="assets/backButton/backButtonNormal.png",
            border=[0, 0, 0, 0]
        )

        self.backButton.bind(on_release=self.goBack)

        self.add_widget(self.backButton)

        #Add the logo at the top next to question

        self.recordingScreenTopLogoCard = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.175, 0.175),
            pos_hint={"top": 67.5/68, "x":0.22}
        )

        self.add_widget(self.recordingScreenTopLogoCard)

        #Add the label for the question at the top 

        self.recordingScreenTopQuestionLabel = Label(
            text='Who is in the photo?',
            size_hint=(0.7, 0.175), 
            pos_hint={"x":0.3, "top": 1},
            color=self.darkBlueList,
            font_name="latoBold",
            halign="left",
            valign="middle",
            text_size=(self.size[0]*1.33, self.size[1]),
            font_size=self.height * 0.2
        )

        #Change text to fit

        self.recordingScreenTopQuestionLabel.texture_update()

        self.recordingScreenTopQuestionLabel.font_size = self.recordingScreenTopQuestionLabel.font_size * 1.25
        
        self.add_widget(self.recordingScreenTopQuestionLabel)

        #Add the label but without text so it is blank at the start

        self.recordingScreenAnswerCardLabel = Label(
            size_hint=(0.8, 0.175), 
            pos_hint={"x":0.1, "top": 220/272},
            color=self.darkBlueList,
            font_name="latoBold",
            halign="center",
            valign="middle",
            font_size=self.height * 0.2,
            text_size=(Window.size[0]*0.8, Window.size[1]*0.175),
        )

        #Change text to fit

        self.recordingScreenAnswerCardLabel.texture_update()
        
        self.add_widget(self.recordingScreenAnswerCardLabel)

        #Make an image widget and then use the ratio for further use - Not displayed

        self.recordingScreenImageRatioGet = Image(
            source="assets/TestImages/squareTest.jpg",
            pos_hint={"top": 56/68, "x":0.1}
        )

        #Setting up image ratios and which side will be maximized

        if (Window.size[0]*0.8)/self.recordingScreenImageRatioGet.texture_size[0] < (Window.size[1]*0.36)/self.recordingScreenImageRatioGet.texture_size[1]:
            self.imageRatio = [Window.size[0]*0.8, (Window.size[0]*0.8)/self.recordingScreenImageRatioGet.texture_size[0]*self.recordingScreenImageRatioGet.texture_size[1]]
        else:
            self.imageRatio = [(Window.size[1]*0.36)/self.recordingScreenImageRatioGet.texture_size[1]*self.recordingScreenImageRatioGet.texture_size[0], (Window.size[1]*0.36)]

        #Drawing the image
        
        with self.canvasHolderLabel.canvas:
            #Drawing the border under the image in relation to the ratio

            Color(*self.whiteTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5-Window.size[0]*0.025, Window.size[1]*(105/272)-self.imageRatio[1]/2 - Window.size[1]*0.0125),
                size=(Window.size[0]*0.05 + self.imageRatio[0], Window.size[1]*0.025 + self.imageRatio[1]),
                source="assets/general/GreyBackground.png"
                
            )

            #Drawing the image in relation to the ratio

            Color(*self.greyColorTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5, Window.size[1]*(105/272)-self.imageRatio[1]/2),
                size=self.imageRatio,
                source="assets/TestImages/squareTest.jpg"
                
            )
        
        #Add the recorder button so that user can record


        self.recordingScreenRecorderButtonBottom = Button(
            size_hint=(0.25, 0.12),
            pos_hint={"top": 9/68, "x":(1/2) - (1/8)},
            color=self.lightGreyColorTuple,
            font_name="latoBold",
            font_size=22,
            halign="left",
            background_normal="assets/mainScreenSpeechRecorderButtonBottom/RedColorCirclularButtomPicNormal.png",
            background_down="assets/mainScreenSpeechRecorderButtonBottom/RedColorCirclularButtomPicNormal.png",
            border = [-0, -0, -0, -0]
        )
        
        self.recordingScreenRecorderButtonBottom.bind(on_press=self.popupInitRecorderStart)
        self.add_widget(self.recordingScreenRecorderButtonBottom)

        #Creating the layout for the popup

        self.recordingPopupContent = FloatLayout()

        #Adding label saying they are being recorded

        self.recordingScreenRecordingLabelMiddlePopup = Label(
            text="Recording ...",
            font_size="30",
            font_name="latoBold",
            halign="center",
            valign="middle",
            size_hint=(0.8, 0.175),
            pos_hint={"x":0.1, "top": 220/272},
            color=self.darkBlueList
        )
        self.recordingPopupContent.add_widget(self.recordingScreenRecordingLabelMiddlePopup)

        #Adding the button to stop the recording

        self.recordingScreenRecordingStopBottomPopup = Button(
            size_hint=(0.30, 0.26),
            pos_hint={"top": 17/68, "x":(1/2) - (3/20)},
            background_normal="assets/recordingScreenRecordingStopBottomPopup/recordingScreenRecordingStopBottomPopupNormal.png",
            border=(0, 0, 0, 0)
        )
        self.recordingPopupContent.add_widget(self.recordingScreenRecordingStopBottomPopup)

        self.recordingScreenRecordingStopBottomPopup.bind(on_press=self.stopRecordAddText)

        #Creating the popup which starts after recording    

        self.recordingPopup = Popup(
            content=self.recordingPopupContent,
            auto_dismiss=False,
            size_hint=(0.9, 0.5),
            background="assets/recordingScreenRecordingPopup/recordingScreenRecordingPopupBackground.png",
            pos_hint={"top": 35/68, "x":(1/2) - (9/20)},
            separator_color=[0, 0, 0, 0],
            title="",
            border=(0, 0, 0, 0)
        )

        self.checkRecordEvent = Clock.schedule_interval(self.recordStart, 1 / 43)

    #recordStart() starts getting frames from the microphone

    def recordStart(self, dt, *kwargs):
        if self.startRecord == True:
            self.data = self.stream.read(self.CHUNK)
            self.frames.append(self.data)

    #popupInitRecorderStart() opens the recording popup and sets the start recording variable as true

    def popupInitRecorderStart(self, dt, *kwargs):
        self.recordingPopup.open()
        self.startRecord = True

    #stopRecordAddText() stops recording, closes popup, and gets the text from the recording

    def stopRecordAddText(self, dt, *kwargs):
        self.recordingPopup.dismiss()

        self.wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        self.wf.setnchannels(self.CHANNELS)
        self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        self.wf.setframerate(self.RATE)
        self.wf.writeframes(b''.join(self.frames))
        self.wf.close()

        if self.firstRecord == False:
            with self.canvasHolderLabel.canvas:
                Color(*self.whiteTuple)
                RoundedRectangle(
                    segments=100,
                    radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                    pos=(Window.size[0]*0.05, Window.size[1]*(169/272)),
                    size=(Window.size[0]*0.9, Window.size[1]*0.175),
                    source="assets/general/GreyBackground.png"
                    
                )

        self.filename = self.WAVE_OUTPUT_FILENAME
        self.r = sr.Recognizer()

        try:
            with sr.AudioFile(self.filename) as self.source:
                self.audio_data = self.r.record(self.source)
                self.recordingScreenAnswerCardLabel.text = str(self.r.recognize_google(self.audio_data))
                self.recordingScreenAnswerCardLabel.text = self.recordingScreenAnswerCardLabel.text[0].upper() + self.recordingScreenAnswerCardLabel.text[1:] + "."
                self.recordingScreenAnswerCardLabel.texture_update()
        except:
            self.recordingScreenAnswerCardLabel.text = "Try recording again."

        self.frames = []

        self.firstRecord = True

        self.startRecord = False

    #goBack() sets the screen at mainScreen

    def goBack(self, dt):
        Vocate.sm.transition.direction = "right"
        Vocate.sm.current = "mainScreen"

class mainScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(mainScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.lightGreyColorTuple = (243/255, 243/255, 243/255, 243/255)
        self.lightGreyColorList = [243/255, 243/255, 243/255, 243/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.darkestBlueTuple = (4/255, 61/255, 66/255, 255/255)
        self.darkestBlueList = [5/255, 61/255, 66/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.appBackgroundTuple = (250/255, 250/255, 250/255, 255/255)
        self.appBackgroundList = [250/255, 250/255, 250/255, 255/255]

        #Add background

        Window.clearcolor = self.appBackgroundTuple

        #Make a testing canvasHolder

        self.canvasHolderLabel = Label(size=(Window.size[0], Window.size[1]*0.175))
        

        #Drawing the rounded rectangle under the main header -- Not Scalable

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.labelRect = RoundedRectangle(
                segments=100,
                radius=[(0, 0), (0, 0), (45.0, 45.0), (0, 0)],
                pos=(0, Window.size[1]-Window.size[1]*0.175),
                size=(Window.size[0], Window.size[1]*0.175),
                source="assets/general/GreyBackground.png"
                
            )

        self.add_widget(self.canvasHolderLabel)

        #Creating the main header at the top - Semi Scalable

        self.mainScreenTopLabel = Label(
            text='Welcome Back!',
            size=(Window.size[0], Window.size[1]*0.16),
            pos=(0, 0),
            size_hint=(1, 0.175), 
            pos_hint={"x":0, "top": 1},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/9.7),
        )

        self.add_widget(self.mainScreenTopLabel)

        #Make an image widget and then use the ratio for further use - Not displayed

        self.mainScreenImageRatioGet = Image(
            source="C:/Users/Penguinkid/Downloads/8481.jpg",
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

            Color(*self.whiteTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5-Window.size[0]*0.025, Window.size[1]*(169/272)-self.imageRatio[1]/2 - Window.size[1]*0.0125),
                size=(Window.size[0]*0.05 + self.imageRatio[0], Window.size[1]*0.025 + self.imageRatio[1]),
                source="assets/general/GreyBackground.png"
                
            )

            #Drawing the image in relation to the ratio

            Color(*self.whiteTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5, Window.size[1]*(169/272)-self.imageRatio[1]/2),
                size=self.imageRatio,
                source="C:/Users/Penguinkid/Downloads/8481.jpg"
                
            )

        #Creating the dynamic speech prompter button for the user.

        self.mainScreenSpeechPromptButtonMiddle = Button(
            text="Where were you? What were he/she doing?",
            size_hint=(0.9, 0.175),
            pos_hint={"top": 26/68, "x":0.05},
            color=self.darkestBlueList,
            font_name="latoBold",
            halign="left",
            text_size=(self.size[0]*1.5, self.size[1]*1.25),
            valign="middle",
            background_normal="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicNormal.png",
            background_down="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicNormal.png",
            border = [30, 30, 30, 30]
        )

        #Making sure the text fits prefectly

        self.mainScreenSpeechPromptButtonMiddle.texture_update()
        self.mainScreenSpeechPromptButtonMiddle.font_size = self.mainScreenSpeechPromptButtonMiddle.font_size*1.25

        self.add_widget(self.mainScreenSpeechPromptButtonMiddle)

        #Adding the Assistant Icon to the Speech Prompt button above

        self.mainScreenSpeechPromptAssistantPic = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.14, 0.14),
            pos_hint={"top": 25/68, "x":0.1}
        )

        self.add_widget(self.mainScreenSpeechPromptAssistantPic)

        #Creating the Lower Button that given the option to record text

        self.mainScreenEnterTextButtonLower = Button(
            text="Start\nRecording",
            size_hint=(0.333, 0.156),
            pos_hint={"top": 6/34, "x":(1/2) - (1/6)},
            color=self.whiteList,
            font_name="latoBold",
            font_size=20,
            halign="center",
            background_normal="assets/mainScreenEnterTextButtonLower/DarkBlueRoundedButtonPicNormal.png",
            background_down="assets/mainScreenEnterTextButtonLower/DarkBlueRoundedButtonPicDown.png",
            border = [-0, -0, -0, -0]
        )
        
        #Add function to when button is pressed

        self.mainScreenEnterTextButtonLower.bind(on_press=self.toRecording)

        self.add_widget(self.mainScreenEnterTextButtonLower)

    #Changes position and size when screen changes

    def update_rect(self, *args):
        self.labelRect.pos = (0, Window.size[1]-Window.size[1]*0.175)
        self.labelRect.size = (Window.size[0], Window.size[1]*0.175)

    #Function to change screens when button is pressed

    def toRecording(self, dt):
        Vocate.sm.transition.direction = "left"
        Vocate.sm.current = "recordingScreen"


class addImageScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(addImageScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.lightGreyColorTuple = (243/255, 243/255, 243/255, 243/255)
        self.lightGreyColorList = [243/255, 243/255, 243/255, 243/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.darkestBlueTuple = (4/255, 61/255, 66/255, 255/255)
        self.darkestBlueList = [5/255, 61/255, 66/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.appBackgroundTuple = (250/255, 250/255, 250/255, 255/255)
        self.appBackgroundList = [250/255, 250/255, 250/255, 255/255]

        self.blackTuple = (0, 0, 0, 1)
        self.blackList = [0, 0, 0, 1]

        #Add background

        Window.clearcolor = self.appBackgroundTuple

        #Make a testing canvasHolder

        self.canvasHolderLabel = Label(
            size=(Window.size[0], Window.size[1]*0.025),
        )
        
        #Drawing the rounded rectangle under the main header -- Not Scalable

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.labelRect = RoundedRectangle(
                segments=100,
                radius=[(0, 0), (0, 0), (45.0, 45.0), (0, 0)],
                pos=(0, Window.size[1]-Window.size[1]*0.11),
                size=(Window.size[0], Window.size[1]*0.11),
                source="assets/general/GreyBackground.png"
                
            )

        self.add_widget(self.canvasHolderLabel)

        #Creating the main header at the top - Semi Scalable

        self.addImageScreenTopLabel = Label(
            text='Vocate',
            size=(Window.size[0], Window.size[1]*0.125),
            pos=(0, 0),
            size_hint=(1, 0.125), 
            pos_hint={"x":0, "top": 1},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/9.7)
        )

        self.add_widget(self.addImageScreenTopLabel)



        #Add label which shows what the page is doing

        self.addImageScreenMainLabel = Label(
            text='Add Memories',
            text_size=(Window.size[0]*0.8, Window.size[1]*0.05),
            size_hint=(0.8, 0.05),
            pos_hint={"x":0.1, "top": 28/32},
            halign="left",
            color=self.blackList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/13)
        )

        self.add_widget(self.addImageScreenMainLabel)

        #Add button which sends user back to caretaker screen

        self.backButton = Button(
            size_hint=(0.13, 0.05),
            pos_hint={"top": 131/136, "x": 0.06},
            background_normal="assets/backButton/backButtonNormal.png",
            background_down="assets/backButton/backButtonNormal.png",
            border=[0, 0, 0, 0]
        )

        self.backButton.bind(on_release=self.goBack)

        self.add_widget(self.backButton)

        #Make a drawing that will hold the upload image button

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.uploadImageRect = RoundedRectangle(
                segments=100,
                radius=[(40.0, 40.0), (40.0, 40.0), (40.0, 40.0), (40.0, 40.0)],
                pos=(Window.size[0]*0.1, Window.size[1]-Window.size[1]*0.575),
                size=(Window.size[0]*0.8, Window.size[1]*0.375),
                source="assets/general/GreyBackground.png"
                
            )

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.uploadImageRect = RoundedRectangle(
                segments=100,
                radius=[(40.0, 40.0), (40.0, 40.0), (40.0, 40.0), (40.0, 40.0)],
                pos=(Window.size[0]*0.125, Window.size[1]-Window.size[1]*0.56),
                size=(Window.size[0]*0.75, Window.size[1]*0.35),
                source="assets/general/addImageScreenImageUploadDottedLine.png"
                
            )

        #Added text to box to say to upload photo

        self.addImageScreenUploadImageText = Label(
            text="Upload Image",
            size_hint=(0.4, 0.1),
            pos_hint={"x":0.3, "top": 24/32},
            halign="center",
            color=self.fullOrangeList,
            font_name="montserratExtraBold",
            font_size=20
        )

        self.add_widget(self.addImageScreenUploadImageText)

        #Added button to upload photo

        self.addImageScreenUploadImageButton = Button(
            size_hint=(0.2, 0.10),
            pos_hint={"top": 42/68, "x":0.4},
            background_normal="assets/addImageScreenImageUploadButton/addImageScreenImageUploadButtonNormal.png",
            background_down="assets/addImageScreenImageUploadButton/addImageScreenImageUploadButtonDown.png",
            border = [0, 0, 0, 0]
        )

        self.addImageScreenUploadImageButton.bind(on_release=self.browseFiles)

        self.add_widget(self.addImageScreenUploadImageButton)

        #Add floatlayout for the filepopup

        self.filePopupContent = FloatLayout()

        #Created fileUpload popup

        self.filePopup = Popup(
            content=self.filePopupContent,
        )

        # first, create the scrollView
        self.scrollView = scrollView = ScrollView()

        # then, create the fileChooser and integrate it in thescrollView
        self.fileChooser = fileChooser = FileChooserListView(size_hint_y=None)
        fileChooser.height = Window.size[1] # this is a bit ugly...
        scrollView.add_widget(fileChooser)

        # construct the content, widget are used as a spacer
        self.filePopupContent.add_widget(Widget(size_hint_y=None, height=5))
        self.filePopupContent.add_widget(scrollView)
        self.filePopupContent.add_widget(Widget(size_hint_y=None, height=5))

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        btn = Button(text='Ok')
        btn.bind(on_release=self.validate)
        btnlayout.add_widget(btn)

        btn = Button(text='Cancel')
        btn.bind(on_release=self.filePopup.dismiss)
        btnlayout.add_widget(btn)
        self.filePopupContent.add_widget(btnlayout)

        #Creating the floatlayout() for the popup

        self.metadataPopupContent = FloatLayout()

        #Creating the metadataPopup

        self.metadataPopup = Popup(
            content=self.metadataPopupContent,
            auto_dismiss=False,
            size_hint=(0.9, 0.5),
            background="assets/recordingScreenRecordingPopup/recordingScreenRecordingPopupBackground.png",
            pos_hint={"top": 35/68, "x":(1/2) - (9/20)},
            separator_color=[0, 0, 0, 0],
            title="",
            border=(0, 0, 0, 0)
        )

        #Creating the list with all of the metadata

        self.metadataQuestions = [
            "1. Give the image a title",
            "2. What was the location",
            "3. List the people in the\nimage",
            "4. Type in a special\nquestion",
            "5. What's the answer"
        ]

        #Creating the list which all metadata gets saved to

        self.metadataAnswers=[]

        #Creating variable to change questions

        self.metadataQuestionIndexes = 0

        #Adding the Label which has question

        self.metadataPopupQuestionLabel = Label(
            text=self.metadataQuestions[self.metadataQuestionIndexes],
            size_hint=(1, 0.2),
            pos_hint={"x": 0, "top": 33/36},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/17),
            halign="center"
        )

        self.metadataPopupContent.add_widget(self.metadataPopupQuestionLabel)

        #Adding the textinput which takes the answers

        self.metadataPopupQuestionAnswerInput = TextInput(
            text='',
            multiline=False,
            border=[30, 30, 30, 30],
            background_color=self.lightGreyColorTuple,
            background_normal="assets/general/greyBackground.png",
            background_active="assets/general/greyBackground.png",
            font_name="latoBold",
            font_size=25,
            size_hint=(0.7, 0.15),
            pos_hint={"x": 0.15, "top": 0.6},
            cursor_color=self.blackList
        )

        self.metadataPopupContent.add_widget(self.metadataPopupQuestionAnswerInput)

        #Adding the canvas which gives the rounding corners to the text input

        with self.metadataPopupQuestionLabel.canvas:
            Color(*self.lightGreyColorList)
            self.leftSemi = Ellipse(
                segments=100,
                pos=(self.metadataPopup.size[0]*0.505, self.metadataPopup.size[1]*1.6), 
                size=(self.metadataPopup.size[1]*0.5, self.metadataPopup.size[1]*0.45),
                angle_start=180,
                angle_end=360,
                source="assets/general/greyBackground.png"
                
            )

            self.rightSemi = Ellipse(
                segments=100,
                pos=(self.metadataPopup.size[0]*2.505, self.metadataPopup.size[1]*1.6), 
                size=(self.metadataPopup.size[1]*0.5, self.metadataPopup.size[1]*0.45),
                angle_start=0,
                angle_end=180,
                source="assets/general/greyBackground.png"
                
            )

        #Adding the button to change to the next question

        self.metadataPopupNextQuestionButton = Button(
            text='Next    ',
            border=[30, 30, 30, 30],
            background_normal="assets/general/addImageScreenNextQuestionButton.png",
            background_down="assets/general/addImageScreenNextQuestionButton.png",
            font_name="montserratExtraBold",
            font_size=25,
            size_hint=(0.5, 0.1675),
            pos_hint={"x": 0.25, "top": 0.3},
            color=self.fullOrangeList,
            halign="left"
        )

        self.metadataPopupNextQuestionButton.bind(on_release=self.saveMeta)

        self.metadataPopupContent.add_widget(self.metadataPopupNextQuestionButton)

    #Creating function to save the file path of the selected file

    def validate(self, instance):
        print(self.fileChooser.selection)
        self.filePopup.dismiss()
        self.value = self.fileChooser.selection
        print('choosen file: %s' % self.value)

        if str(self.value) != "[]":
            self.metadataPopup.open()

    #Creating function to open the filePopup

    def browseFiles(self, dt):
        self.filePopup.open()

    #Making function to save all of the Metadata answers and changing the question

    def saveMeta(self, dt):
        if self.metadataQuestionIndexes == 4:
            self.metadataAnswers.append(self.metadataPopupQuestionAnswerInput.text)
            print(["imageDatabase/" + self.value[0].split("\\")[-1]] + self.metadataAnswers)
            self.metadataPopup.dismiss()

            shutil.copyfile(self.value[0], "imageDatabase/" + self.value[0].split("\\")[-1])

        else:
            self.metadataAnswers.append(self.metadataPopupQuestionAnswerInput.text)
            self.metadataQuestionIndexes += 1
            self.metadataPopupQuestionLabel.text = self.metadataQuestions[self.metadataQuestionIndexes]
            self.metadataPopupQuestionAnswerInput.text = ""

    def goBack(self, dt):
        Vocate.sm.transition.direction = "right"
        Vocate.sm.current = "caretakerScreen"


class statsScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(statsScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.lightGreyColorTuple = (243/255, 243/255, 243/255, 243/255)
        self.lightGreyColorList = [243/255, 243/255, 243/255, 243/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.darkestBlueTuple = (4/255, 61/255, 66/255, 255/255)
        self.darkestBlueList = [5/255, 61/255, 66/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.appBackgroundTuple = (250/255, 250/255, 250/255, 255/255)
        self.appBackgroundList = [250/255, 250/255, 250/255, 255/255]

        self.blackTuple = (0, 0, 0, 1)
        self.blackList = [0, 0, 0, 1]

        #Add background

        Window.clearcolor = self.appBackgroundTuple

        #Make a testing canvasHolder

        self.canvasHolderLabel = Label(size=(Window.size[0], Window.size[1]*0.175))
        

        #Drawing the rounded rectangle under the main header -- Not Scalable

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.labelRect = RoundedRectangle(
                segments=100,
                radius=[(0, 0), (0, 0), (45.0, 45.0), (0, 0)],
                pos=(0, Window.size[1]-Window.size[1]*0.11),
                size=(Window.size[0], Window.size[1]*0.11),
                source="assets/general/GreyBackground.png"
                
            )

        self.add_widget(self.canvasHolderLabel)

        #Creating the main header at the top - Semi Scalable

        self.statsScreenTopLabel = Label(
            text='Vocate',
            size=(Window.size[0], Window.size[1]*0.125),
            pos=(0, 0),
            size_hint=(1, 0.125), 
            pos_hint={"x":0, "top": 1},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/9.7)
        )

        self.add_widget(self.statsScreenTopLabel)

        #Adding button to go pack to previous screen

        self.backButton = Button(
            size_hint=(0.13, 0.05),
            pos_hint={"top": 131/136, "x": 0.06},
            background_normal="assets/backButton/backButtonNormal.png",
            background_down="assets/backButton/backButtonNormal.png",
            border=[0, 0, 0, 0]
        )

        self.backButton.bind(on_release=self.goBack)

        self.add_widget(self.backButton)

        #Adding label with screen intention

        self.statsScreenMainLabel = Label(
            text='Stats',
            text_size=(Window.size[0]*0.8, Window.size[1]*0.05),
            size_hint=(0.8, 0.05),
            pos_hint={"x":0.1, "top": 28/32},
            halign="left",
            color=self.blackList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/13)
        )

        self.add_widget(self.statsScreenMainLabel)

        #Adding a button which has the stats of the viewed memories

        self.statsScreenStatTopLeft = Button(
            markup=True,
            text='Memories Viewed\n[size=14][/size]\n[size=30][color=f78f1eff]{}[/color][/size]'.format(8),
            text_size=(Window.size[0]*0.4, Window.size[1]*0.2),
            size_hint=(0.4, 0.2),
            pos_hint={"x":0.08, "top": 26/32},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            halign="center",
            valign="middle",
            font_size=20,
            background_normal="assets/statsScreenStatTopLeft/statsScreenStatTopLeftNormal.png",
            background_down="assets/statsScreenStatTopLeft/statsScreenStatTopLeftNormal.png",
            border=[0, 0, 0, 0]
        )

        self.add_widget(self.statsScreenStatTopLeft)

        #Adding a button which has the stats of the incorrect answers

        self.statsScreenStatTopRight = Button(
            markup=True,
            text="Incorrect Answers\n[size=14][/size]\n[size=30][color=f78f1eff]{}[/color][/size]".format(4),
            text_size=(Window.size[0]*0.4, Window.size[1]*0.2),
            size_hint=(0.4, 0.2),
            pos_hint={"x":0.54, "top": 26/32},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            halign="center",
            valign="middle",
            font_size=20,
            background_normal="assets/statsScreenStatTopLeft/statsScreenStatTopLeftNormal.png",
            background_down="assets/statsScreenStatTopLeft/statsScreenStatTopLeftNormal.png",
            border=[0, 0, 0, 0]
        )

        self.add_widget(self.statsScreenStatTopRight)

        #Adding a button which has the stats of the interaction time

        self.statsScreenStatMiddle = Button(
            markup=True,
            text="[size=30][color=f78f1eff]{}[/color][/size]\nmin of interaction".format(16),
            line_height=1.2,
            size_hint=(0.87, 0.17),
            pos_hint={"top": 40/68, "x":0.075},
            text_size=(Window.size[0]*0.75, Window.size[1]*0.17),
            color=[1, 1, 1, 1],
            font_name="montserratExtraBold",
            font_size=22,
            halign="center",
            valign="middle",
            background_normal="assets/statsScreenStatMiddle/statsScreenStatMiddleNormal.png",
            background_down="assets/statsScreenStatMiddle/statsScreenStatMiddleNormal.png",
            border = [0, 0, 0, 0]
        )

        self.add_widget(self.statsScreenStatMiddle)

        #Adding a button which has the stats of the longest day streak

        self.statsScreenStatBottomLeft = Button(
            markup=True,
            text="[size=36][color=f78f1eff]{}[/color][/size]\nLongest\nDay\nStreak".format(5),
            line_height=1.2,
            size_hint=(0.4, 0.35),
            pos_hint={"top": 27/68, "x":0.08},
            text_size=(Window.size[0]*0.4, Window.size[1]*0.35),
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=20,
            halign="center",
            valign="middle",
            background_normal="assets/statsScreenStatBottomLeft/statsScreenStatBottomLeftNormal.png",
            background_down="assets/statsScreenStatBottomLeft/statsScreenStatBottomLeftNormal.png",
            border = [0, 0, 0, 0]
        )

        self.add_widget(self.statsScreenStatBottomLeft)

        #Adding a button which has the stats of the total correct answers

        self.statsScreenStatBottomRight = Button(
            markup=True,
            text="Total\nCorrect\nAnswers\n[size=36][color=f78f1eff]{}[/color][/size]".format(26),
            line_height=1.2,
            size_hint=(0.4, 0.35),
            pos_hint={"top": 27/68, "x":0.54},
            text_size=(Window.size[0]*0.4, Window.size[1]*0.35),
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=20,
            halign="center",
            valign="middle",
            background_normal="assets/statsScreenStatBottomLeft/statsScreenStatBottomLeftNormal.png",
            background_down="assets/statsScreenStatBottomLeft/statsScreenStatBottomLeftNormal.png",
            border = [0, 0, 0, 0]
        )

        self.add_widget(self.statsScreenStatBottomRight)

    def goBack(self, dt):
        Vocate.sm.transition.direction = "right"
        Vocate.sm.current = "caretakerScreen"

class caretakerScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(caretakerScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.lightGreyColorTuple = (243/255, 243/255, 243/255, 243/255)
        self.lightGreyColorList = [243/255, 243/255, 243/255, 243/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.darkestBlueTuple = (4/255, 61/255, 66/255, 255/255)
        self.darkestBlueList = [5/255, 61/255, 66/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.appBackgroundTuple = (250/255, 250/255, 250/255, 255/255)
        self.appBackgroundList = [250/255, 250/255, 250/255, 255/255]

        self.blackTuple = (0, 0, 0, 1)
        self.blackList = [0, 0, 0, 1]

        #Add background

        Window.clearcolor = self.appBackgroundTuple

        #Make a testing canvasHolder

        self.canvasHolderLabel = Label(size=(Window.size[0], Window.size[1]*0.175))
        

        #Drawing the rounded rectangle under the main header -- Not Scalable

        with self.canvasHolderLabel.canvas:
            Color(*self.whiteTuple)
            self.labelRect = RoundedRectangle(
                segments=100,
                radius=[(0, 0), (0, 0), (45.0, 45.0), (0, 0)],
                pos=(0, Window.size[1]-Window.size[1]*0.11),
                size=(Window.size[0], Window.size[1]*0.11),
                source="assets/general/GreyBackground.png"
                
            )

        self.add_widget(self.canvasHolderLabel)

        #Creating the main header at the top - Semi Scalable

        self.caretakerScreenTopLabel = Label(
            text='Vocate',
            size=(Window.size[0], Window.size[1]*0.125),
            pos=(0, 0),
            size_hint=(1, 0.125), 
            pos_hint={"x":0, "top": 1},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/9.7),
        )

        self.add_widget(self.caretakerScreenTopLabel)

        #Adding button to send user back to previous screen

        self.backButton = Button(
            size_hint=(0.13, 0.05),
            pos_hint={"top": 131/136, "x": 0.06},
            background_normal="assets/backButton/backButtonNormal.png",
            background_down="assets/backButton/backButtonNormal.png",
            border=[0, 0, 0, 0]
        )

        self.backButton.bind(on_release=self.goBack)
        
        self.add_widget(self.backButton)

        #Added preview of stats for the user for the stats screen

        self.caretakerScreenStatsButton = Button(
            markup=True,
            text="[size=22][color=000000]Stats[/color][/size]\nMemories Viewed - [color=f78f1eff]{}[/color]\nCorrect Answers - [color=f78f1eff]{}[/color]".format("8", "4"),
            line_height=1.2,
            size_hint=(0.9, 0.17),
            pos_hint={"top": 60/68, "x":0.05},
            text_size=(Window.size[0]*0.75, Window.size[1]*0.17),
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=18,
            halign="left",
            valign="center",
            background_normal="assets/caretakerScreenStatsButton/caretakerScreenStatsButtonNormal.png",
            background_down="assets/caretakerScreenStatsButton/caretakerScreenStatsButtonDown.png",
            border = [0, 0, 0, 0]
        )

        self.caretakerScreenStatsButton.bind(on_release=self.toStats)

        self.add_widget(self.caretakerScreenStatsButton)

        #Creating a system to see the ratio of image

        self.caretakerScreenImageRatioGet = Image(
            source="assets/TestImages/squareTest.jpg",
            pos_hint={"top": 56/68, "x":0.1}
        )

        #Setting up image ratios and which side will be maximized

        if (Window.size[0]*0.8)/self.caretakerScreenImageRatioGet.texture_size[0] < (Window.size[1]*0.3)/self.caretakerScreenImageRatioGet.texture_size[1]:
            self.imageRatio = [Window.size[0]*0.8, (Window.size[0]*0.8)/self.caretakerScreenImageRatioGet.texture_size[0]*self.caretakerScreenImageRatioGet.texture_size[1]]
        else:
            self.imageRatio = [(Window.size[1]*0.3)/self.caretakerScreenImageRatioGet.texture_size[1]*self.caretakerScreenImageRatioGet.texture_size[0], (Window.size[1]*0.3)]

        #Drawing the image
        
        with self.canvasHolderLabel.canvas:
            #Drawing the border under the image iin relation to the ratio

            Color(*self.whiteTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5-Window.size[0]*0.025, Window.size[1]*(148/272)-self.imageRatio[1]/2 - Window.size[1]*0.0125),
                size=(Window.size[0]*0.05 + self.imageRatio[0], Window.size[1]*0.025 + self.imageRatio[1]),
                source="assets/general/GreyBackground.png"
                
            )

            #Drawing the image in relation to the ratio

            Color(*self.whiteTuple)
            RoundedRectangle(
                segments=100,
                radius=[(25.0, 25.0), (25.0, 25.0), (25.0, 25.0), (25.0, 25.0)],
                pos=(Window.size[0]*0.5-self.imageRatio[0]*0.5, Window.size[1]*(148/272)-self.imageRatio[1]/2),
                size=self.imageRatio,
                source="assets/TestImages/squareTest.jpg"
                
            )

        #Adding Button to add new memories

        self.caretakerScreenAddMemoriesButton = Button(
            text="Add\nMemories",
            size_hint=(0.9, 0.17),
            pos_hint={"top": 51/136, "x":0.05},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=30,
            halign="center",
            valign="middle",
            background_normal="assets/caretakerScreenStatsButton/caretakerScreenStatsButtonNormal.png",
            background_down="assets/caretakerScreenStatsButton/caretakerScreenStatsButtonDown.png",
            border = [5, 5, 5, 5]
        )

        self.caretakerScreenAddMemoriesButton.bind(on_release=self.toAddImage)

        self.add_widget(self.caretakerScreenAddMemoriesButton)

        #Adding button to see all of the memories

        self.caretakerScreenAllMemoriesButton = Button(
            text="All Memories",
            size_hint=(0.9, 0.17),
            pos_hint={"top": 28/136, "x":0.05},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=30,
            halign="center",
            valign="middle",
            background_normal="assets/caretakerScreenStatsButton/caretakerScreenStatsButtonNormal.png",
            background_down="assets/caretakerScreenStatsButton/caretakerScreenStatsButtonDown.png",
            border = [5, 5, 5, 5]
        )

        self.add_widget(self.caretakerScreenAllMemoriesButton)

    #Adding function to go to stats screen

    def toStats(self, dt):
        Vocate.sm.transition.direction = "left"
        Vocate.sm.current = "statsScreen"

    #Adding function to go back to login screen

    def goBack(self, dt):
        Vocate.sm.transition.direction = "right"
        Vocate.sm.current = "loginScreen"

    #Adding function to go to the adding image screen

    def toAddImage(self, dt):
        Vocate.sm.transition.direction = "left"
        Vocate.sm.current = "addImageScreen"


class loginScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(loginScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.darkestBlueTuple = (4/255, 61/255, 66/255, 255/255)
        self.darkestBlueList = [5/255, 61/255, 66/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.blackTuple = (0, 0, 0, 1)
        self.blackList = [0, 0, 0, 1]

        #Setting background color to greyColorTuple

        Window.clearcolor = self.greyColorTuple

        #Setting the name of the app

        self.loginScreenTopLabel = Label(
            text='Vocate',
            size=(Window.size[0], Window.size[1]*0.16),
            size_hint=(1, 0.175), 
            pos_hint={"x":0, "top": 1},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=40
        )
        self.add_widget(self.loginScreenTopLabel)

        #Adding label to see who they are

        self.loginScreenPromptLabel = Label(
            text='Who are you?',
            size=(Window.size[0], Window.size[1]*0.16),
            size_hint=(1, 0.175), 
            pos_hint={"x":0, "top": 0.93},
            color=self.blackList,
            font_name="montserratExtraBold",
            font_size=25
        )

        self.add_widget(self.loginScreenPromptLabel)

        #Adding assistant logo

        self.loginScreenSpeechPromptAssistantPic = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.65, 0.3),
            pos_hint={"top": 54/68, "x":0.175},
        )

        self.add_widget(self.loginScreenSpeechPromptAssistantPic)

        #Adding a user button to go to user main screen

        self.loginScreenUserButton = Button(
            text="User",
            size_hint=(0.9, 0.19),
            pos_hint={"top": 32/68, "x":0.05},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=40,
            halign="center",
            valign="middle",
            background_normal="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicNormal.png",
            background_down="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicDown.png",
            border = [30, 30, 30, 30]
        )

        self.loginScreenUserButton.bind(on_release=self.toUser)

        self.add_widget(self.loginScreenUserButton)

        #Adding button to go to caretaker main screen

        self.loginScreenCaretakerButton = Button(
            text="Caretaker",
            size_hint=(0.9, 0.19),
            pos_hint={"top": 18/68, "x":0.05},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=40,
            halign="center",
            valign="middle",
            background_normal="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicNormal.png",
            background_down="assets/mainScreenSpeechPromptButtonMiddle/GreyColorRoundedButtonPicDown.png",
            border = [30, 30, 30, 30]
        )

        self.loginScreenCaretakerButton.bind(on_release=self.toCaretaker)

        self.add_widget(self.loginScreenCaretakerButton)

    #Adding function to go to user screen

    def toUser(self, dt):
        Vocate.sm.transition.direction = "left"
        Vocate.sm.current = "mainScreen"

    #Adding function to go to the caretaker screen

    def toCaretaker(self, dt):
        Vocate.sm.transition.direction = "left"
        Vocate.sm.current = "caretakerScreen"


class splashScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(splashScreen, self).__init__(**kwargs)

        #Initializing all of the main theme colors

        self.greyColorTuple = (239/255, 239/255, 239/255, 239/255)
        self.greyColorList = [239/255, 239/255, 239/255, 239/255]

        self.lightGreyColorTuple = (243/255, 243/255, 243/255, 243/255)
        self.lightGreyColorList = [243/255, 243/255, 243/255, 243/255]

        self.darkBlueTuple = (5/255, 79/255, 80/255, 255/255)
        self.darkBlueList = [5/255, 79/255, 80/255, 255/255]

        self.darkestBlueTuple = (4/255, 61/255, 66/255, 255/255)
        self.darkestBlueList = [5/255, 61/255, 66/255, 255/255]

        self.whiteTuple = (1, 1, 1, 1)
        self.whiteList = [1, 1, 1, 1]

        self.fullOrangeTuple = (247/255, 143/255, 30/255, 255/255)
        self.fullOrangeList = [247/255, 143/255, 30/255, 255/255]

        self.appBackgroundTuple = (250/255, 250/255, 250/255, 255/255)
        self.appBackgroundList = [250/255, 250/255, 250/255, 255/255]

        #Add background

        Window.clearcolor = self.darkestBlueTuple

        #Add main logo to the front page

        self.splashScreenLogoPic = Image(
            source="assets/assistantLogo/AssistantLogoPic.png",
            size_hint=(0.7, 0.35),
            pos_hint={"top": 58/68, "x":0.15},
        )

        self.add_widget(self.splashScreenLogoPic)

        #Add the name fo the app on the splash screen

        self.splashScreenNameMiddle = Label(
            text='Vocate',
            size=(Window.size[0], Window.size[1]*0.16),
            pos=(0, 0),
            size_hint=(1, 0.175), 
            pos_hint={"x":0, "top": 0.5},
            color=self.darkBlueList,
            font_name="montserratExtraBold",
            font_size=int(Window.size[0]/6)
        )
        self.add_widget(self.splashScreenNameMiddle)

        #Add a clock that fires when the timer goes up to the function which changes screens

        Clock.schedule_once(self.screenTransition, 6)

    #Function that changes screens to mainScreen

    def screenTransition(self, dt):
        Vocate.sm.current = "loginScreen"

class Vocate(App):

    def build(self):
        self.sm = ScreenManager()

        #Adding splash screen to screenManager

        self.splashPage = splashScreen()
        screen = Screen(name='splashScreen')
        screen.add_widget(self.splashPage)
        self.sm.add_widget(screen)

        #Adding login screen to screenManager

        self.loginPage = loginScreen()
        screen = Screen(name='loginScreen')
        screen.add_widget(self.loginPage)
        self.sm.add_widget(screen)

        #Adding caretaker screen to screenManager

        self.caretakerPage = caretakerScreen()
        screen = Screen(name='caretakerScreen')
        screen.add_widget(self.caretakerPage)
        self.sm.add_widget(screen)

        #Adding stats screen to screenManager

        self.statsScreen = statsScreen()
        screen = Screen(name="statsScreen")
        screen.add_widget(self.statsScreen)
        self.sm.add_widget(screen)

        #Adding addImage screen to screenManager

        self.addImageScreen = addImageScreen()
        screen = Screen(name="addImageScreen")
        screen.add_widget(self.addImageScreen)
        self.sm.add_widget(screen)

        #Adding main screen to screenManager

        self.mainPage = mainScreen()
        screen = Screen(name='mainScreen')
        screen.add_widget(self.mainPage)
        self.sm.add_widget(screen)

        #Adding recording screen to screenManager

        self.recordingPage = recordingScreen()
        screen = Screen(name='recordingScreen')
        screen.add_widget(self.recordingPage)
        self.sm.add_widget(screen)
        
        return(self.sm)

if __name__ == "__main__":
    Vocate = Vocate()
    Vocate.run()