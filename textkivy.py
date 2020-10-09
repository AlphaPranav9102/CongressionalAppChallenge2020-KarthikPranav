import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
class music(App):
    
    def build(self):

        self.testButton = Button(
            text="Press Button to Play"
        )

        self.testButton.bind(on_release=self.on_press)

        return self.testButton

    def on_press(self, dt):
        self.sound = SoundLoader.load("playSound.mp3")

        print(self.sound, "hello")
        
        if self.sound:
            print(self.sound.length, self.sound.volume)

        self.sound.play()


music().run()