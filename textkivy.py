import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock


class MyApp(App):

    def build(self):
        self.input = None

        self.inputButton = Button(text='Hello world')

        self.inputButton.bind(on_release=self.makeInput)

        self.goWhile = Clock.schedule_interval(self.fakeWhile, 0)
        self.goInput = None

        return(self.inputButton)

    def fakeWhile(self, dt, **kwargs):
        #The point of the fake while is to simulate getting input from the user
        #The input will be a butten being pressed

        if self.checkInput("ok") != "Not there yet":
            print(self.checkInput("ok"))
            Clock.unschedule(self.goWhile)


    def checkInput(self, dt, **kwargs):
        if self.input != None and dt == "ok":
            return(self.input)
        elif self.input != None and dt != "ok":
            Clock.unschedule(self.goInput)
            self.goWhile = Clock.schedule_interval(self.fakeWhile, 0)
        elif self.input == None and dt == "ok":
            Clock.unschedule(self.goWhile)
            self.goInput = Clock.schedule_interval(self.checkInput, 0)
            return("Not there yet")
        else:
            pass

    def makeInput(self, dt, **kwargs):
        self.input = "Pranav"


if __name__ == '__main__':
    MyApp().run()