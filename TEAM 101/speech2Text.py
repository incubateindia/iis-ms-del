import speech_recognition as sr

r = sr.Recognizer()

# with sr.Microphone() as source:
#     print('Speak')
#     audio = r.listen(source)

#     try:
#         text = r.recognize_google(audio)
#         print(" You said :")
#     except:
#         print("Sorry")
audio_name = "1"
with sr.AudioFile('./audio_uploads/'+audio_name+'.wav') as source:
    audio = r.record(source)
    try:
            text = r.recognize_google(audio)
            print(" You said :"+text)
    except:
            print("Sorry")