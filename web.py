import subprocess
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import speech_recognition as sr
import spacy
from mysql.connector import Error
from Web.ConvertMP4 import convert_video_to_browser_format
from Web.CreateVideo import merge_files_to_video
from Web.DBConnect import get_connection

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

app = Flask(__name__)
CORS(app)  # 🔥 thêm dòng này
#CORS(app, resources={r"/*": {"origins": "http://localhost:63342"}})
# Load model AI
#model = whisper.load_model("base")



def speech_to_text_from_file(audio_path):

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        # dùng Google Speech Recognition
        text = recognizer.recognize_google(audio, language="en-US")

        print("🗣 Recognized text:", text)

        return text

    except sr.UnknownValueError:
        print("❌ Cannot understand audio")
        return ""

    except sr.RequestError as e:
        print("❌ API error:", e)
        return ""

#nlptext



nlp = spacy.load("en_core_web_sm")

#text_temp = speech_to_text_from_file("temp.wav")

TIME_WORDS = {
    "yesterday","today","tomorrow","tonight","now",
    "later","soon","morning","evening","afternoon"
}

def convert_to_sign_structure(sentence):

    doc = nlp(sentence)

    subject = None
    verb = None
    obj = None

    time = []
    location = []
    adjectives = []
    negation = None
    persons = []

    for token in doc:

        # phát hiện tên người
        if token.ent_type_ == "PERSON":
            persons.append(token.text)

        # VERB chính
        if token.dep_ == "ROOT":
            verb = token.lemma_

        # SUBJECT
        if token.dep_ in ["nsubj","csubj"]:
            subject = token.text

        # PASSIVE SUBJECT
        if token.dep_ in ["nsubjpass","csubjpass"]:
            obj = token.text

        # OBJECT
        if token.dep_ in ["dobj","iobj","attr","oprd"]:
            obj = token.text

        # ADJECTIVE COMPLEMENT
        if token.dep_ == "acomp":
            adjectives.append(token.text)

        # PREPOSITIONAL OBJECT
        if token.dep_ == "prep":
            for child in token.children:
                if child.dep_ == "pobj":
                    location.append(child.text)

        # PASSIVE AGENT
        if token.dep_ == "agent":
            for child in token.children:
                if child.dep_ == "pobj":
                    subject = child.text

        # TIME
        if token.text.lower() in TIME_WORDS:
            time.append(token.text)

        # NEGATION
        if token.dep_ == "neg":
            negation = token.text

        # NOUN MODIFIER
        if token.dep_ in ["compound","amod"]:
            adjectives.append(token.text)

    def split_name(name):
        return list(name.upper())

    output = []

    output.extend(time)
    output.extend(location)

    if subject:
        if subject in persons:
            output.extend(split_name(subject))
        else:
            output.append(subject)

    if negation:
        output.append(negation)

    if verb and verb != "be":
        output.append(verb)

    if obj:
        if obj in persons:
            output.extend(split_name(obj))
        else:
            output.append(obj)

    output.extend(adjectives)

    print("SIGN STRUCTURE:", " ".join(output))
    return output


#print(convert_to_sign_structure(text_temp))



UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def convert_to_wav(input_path):

    output_path = "temp.wav"

    command = [
        "ffmpeg",
        "-i", input_path,
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_path,
        "-y"
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return output_path


# Mapping text → video
"""VIDEO_MAP = {
    "he": "text2sign/video/output.mp4",
    "tạm biệt": "bye.mp4",
    "cảm ơn": "thanks.mp4"
}
"""


def get_video_by_word(word):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT source FROM text2sign WHERE word = %s"
        cursor.execute(sql, (word,))

        result = cursor.fetchone()

        if result:
            print(result[0])
            return result[0]

        else:
            return None

    except Error as e:
        print("❌ Database error:", e)
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    file = request.files["audio"]

    # tạo tên file random
    #filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    # lưu file
    file.save(filepath)

    # giờ mới convert
    wav_path = convert_to_wav(filepath)

    # Speech → Text
    result = convert_to_sign_structure(speech_to_text_from_file(wav_path))
    #text = result["text"].lower()
    print("Text:", result)

    # Map → video
    video_files = [get_video_by_word(w) for w in result]
    print("VIDEO_FILES:", video_files)

    video = convert_video_to_browser_format(merge_files_to_video(video_files))


    if video_files:
        return jsonify({
            "text": speech_to_text_from_file(wav_path),
            "nlptext": result,
            "video": f"{video}"
        })

    return jsonify({
        "text": speech_to_text_from_file(wav_path),
        "nlptext": result,
        "video": None
    })


@app.route("/uploads/<filename>")
def get_video(filename):
    video_dir = os.path.join(os.getcwd(), "uploads")

    return send_from_directory(
        video_dir,
        filename,
        mimetype="video/mp4"
    )

if __name__ == "__main__":
    app.run(debug=True)