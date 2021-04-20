import wave
import pyaudio
from gtts import gTTS
import os


def playmyaudio():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = 3
    filename = "output.wav"
    p = pyaudio.PyAudio()
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Finished recording')
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


import speech_recognition as sr
from playsound import playsound
import winsound

MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            cipher += ' '
    return cipher


def decrypt(message):
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
    return decipher


def main():
    print("ENTER E FOR ENCRYPTION OR D FOR DECRYPTION")
    c = input()
    c = c.upper()
    if c == 'E':
        print("ENTER T TO WRITE TEXT OR ENTER A TO SPEAK")
        d = input()
        if d == 'A':
            playmyaudio()
            filename = "output.wav"
            r = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
                print(text)
            message = text
            result = encrypt(message.upper())
            print(result)
            for i in result:
                if i == '.':
                    winsound.Beep(1000, 100)
                if i == '-':
                    winsound.Beep(1000, 500)
        else:
            print("ENTER THE TEXT :")
            message = input()
            result = encrypt(message.upper())
            print(result)
            for i in result:
                if i == '.':
                    winsound.Beep(1000, 100)
                if i == '-':
                    winsound.Beep(1000, 500)
    else:
        print("ENTER THE MORSE CODE :")
        message = input()
        result = decrypt(message)
        language = 'en'
        speech = gTTS(text=result, lang=language, slow=False)
        speech.save("text.wav")
        os.system("text.wav")
        print(result)


# Executes the main function
if __name__ == '__main__':
    main()
