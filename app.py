from flask import Flask, render_template, jsonify
import speech_recognition as sr
import threading

app = Flask(__name__)

recognizer = sr.Recognizer()
current_text = ""
listening = False

def listen_and_recognize():
    global current_text
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while listening:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                current_text += text + " "  # Append the new text
                print(f"Recognized: {text}")
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")

@app.route('/start-listening', methods=['POST'])
def start_listening():
    global listening, current_text
    listening = True
    threading.Thread(target=listen_and_recognize).start()
    return jsonify({"status": "Listening started"})

@app.route('/stop-listening', methods=['POST'])
def stop_listening():
    global listening
    listening = False
    return jsonify({"status": "Listening stopped"})

@app.route('/reset', methods=['POST'])
def reset_text():
    global current_text
    current_text = ""
    return jsonify({"status": "Text reset"})

@app.route('/get-text', methods=['GET'])
def get_text():
    return jsonify({"text": current_text})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
