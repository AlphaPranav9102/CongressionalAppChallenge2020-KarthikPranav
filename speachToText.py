from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)

in_text = input('Enter what you want me to say: ')
speak(in_text)