import time

import cv2
from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles
from Web.DBConnect import get_connection
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
import os
import speech_recognition as sr
import spacy
from mysql.connector import Error
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
fast_app = FastAPI()

origins = ["*"]

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@fast_app.middleware("http")
async def no_cache(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

fast_app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

@fast_app.get("/")
def home():
    return FileResponse("Templates/index.html")

# fast_app.mount(
#     "/uploads",
#     StaticFiles(directory="uploads"),
#     name="uploads"
# )
@fast_app.get("/api/video/{word}")
def get_video(word: str):

    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM text2sign WHERE word=%s"
    cursor.execute(sql, (word,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            "word": result[1],
            "source": result[4]
        }

    return {
        "word": word,
        "source": "upload/audio.mp4"
    }


#upload video

@fast_app.post("/upload_audio")
async def upload_audio(audio: UploadFile = File(...)):

    try:
        os.makedirs("uploads", exist_ok=True)
        file_location = f"uploads/{audio.filename}"
        # save file
        with open(file_location, "wb") as buffer:
            buffer.write(await audio.read())
        # convert wav
        wav_path = convert_to_wav(file_location)
        # speech to text
        result = speech_to_text_from_file(wav_path)
        if not result:
            return JSONResponse(
                content={"error": "Speech recognition failed"},
                status_code=400
            )
        print("Text:", result)
        # NLP (cache từ mysql)
        result_nlp = get_nlp_by_word(result)
        if not result_nlp:
            result_nlp = convert_to_sign_structure(result)
        words = result_nlp if result_nlp else result.split()
        if isinstance(words, str):
            words = words.split()
        # 🔥 CHECK FULL SENTENCE VIDEO
        existing_video = get_video_from_db(result)
        if existing_video:
            if os.path.exists(existing_video):
                print("✅ Using cached full sentence")
                return {
                    "text": result,
                    "video": existing_video,
                    "nlptext": list(words),
                    "cached": True
                }
            else:
                print("⚠️ Cache invalid, regenerate...")
        # 🔥 CHECK TEXT EXIST IN MYSQL
        video_files = []
        for w in words:
            v = get_video_by_word(w)
            if v:
                video_files.append(v)
            else:
                for c in w:
                    letter_video = get_video_by_word(c)
                    if letter_video:
                        video_files.append(letter_video)
        if len(video_files) == 0:
            default = "uploads/default.mp4"
            if os.path.exists(default):
                video_files.append(default)
            else:
                return JSONResponse(
                    content={"error": "No video found"},
                    status_code=400
                )
        # merge video
        merged_video = merge_files_to_video(
            video_files,
            "uploads/final.mp4"
        )
        print("Merged:", merged_video)
        if not merged_video:
            return JSONResponse(
                content={"error": "Merge failed"},
                status_code=500
            )
        # convert browser
        video = convert_video_to_browser_format(
            merged_video,
            result
        )
        print("Final video:", video)
        if not video:
            return JSONResponse(
                content={"error": "Convert failed"},
                status_code=500
            )
        # save mysql
        create_word(
            result,
            "",
            "",
            video,
            result_nlp
        )
        print("Saved to MySQL")
        return {
            "text": result,
            "nlptext": list(words),
            "video": f"{video}?t={int(time.time())}",
            "cached": False
        }
    except Exception as e:
        print("ERROR:", str(e))
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
#convert_video_to_browser_format
def convert_video_to_browser_format(input_path, result, output_dir="uploads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = result.replace(" ", "_").lower()
    output_path = os.path.join(
        output_dir,
        f"{filename}.mp4"
    )
    command = ["ffmpeg", "-i", input_path, "-vcodec",
               "libx264",  # video chuẩn browser
               "-acodec", "aac",  # audio chuẩn browser
               "-strict", "experimental",
               "-y", output_path]
    try:
        subprocess.run(command, check=True)
        print("✅ Converted:", output_path)
        return f"uploads/{filename}.mp4"
    except Exception as e:
        print("Convert error:", e)
        return None
#speech to text
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
TIME_WORDS = {
    "yesterday", "today", "tomorrow", "tonight", "now",
    "later", "soon", "morning", "evening", "afternoon"
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
        if token.dep_ in ["nsubj", "csubj"]:
            subject = token.text
        # PASSIVE SUBJECT
        if token.dep_ in ["nsubjpass", "csubjpass"]:
            obj = token.text
        # OBJECT
        if token.dep_ in ["dobj", "iobj", "attr", "oprd"]:
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
        if token.dep_ in ["compound", "amod"]:
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
#Convert to file wav
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
    result = subprocess.run(command, capture_output=True)
    print("FFMPEG:", result.stderr)
    return output_path
def get_video_from_db(word):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT source FROM text2sign WHERE word=%s"
        cursor.execute(sql, (word,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            print("✅ Video from DB:", result[0])
            return result[0]
    except Exception as e:
        print("DB video error:", e)
    return None
# Mapping text → video
def get_video_by_word(word):
    word = word.lower().strip()
    # local file
    path = os.path.join("uploads", f"{word}.mp4")
    if os.path.exists(path):
        return path
    # DB
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT source FROM text2sign WHERE word=%s"
        cursor.execute(sql, (word,))
        result = cursor.fetchone()
        conn.close()
        if result:
            # convert URL → local path
            source = result[0]
            local = source.replace(
                "",
                ""
            )
            if os.path.exists(local):
                return local
    except Exception as e:
        print("DB error:", e)
    return None
#mapping text -> nlpword
def get_nlp_by_word(word):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT nlpword FROM text2sign WHERE word=%s"
        cursor.execute(sql, (word,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            print("✅ NLP from DB:", result[0])
            return result[0]
    except Exception as e:
        print("DB NLP error:", e)
    return None
#merge_files_to_video
def merge_files_to_video(file_list, output_path="uploads/final.mp4", fps=25):
    width = None
    height = None
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = None
    for path in file_list:
        if not os.path.exists(path):
            print("❌ Not found:", path)
            continue
        ext = os.path.splitext(path)[1].lower()
        # ===== IMAGE =====
        if ext in [".jpg", ".png", ".jpeg"]:
            img = cv2.imread(path)
            if img is None:
                print("❌ Cannot read image:", path)
                continue
            if width is None:
                height, width = img.shape[:2]
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            else:
                img = cv2.resize(img, (width, height))
            # lấy tên file làm text
            word = os.path.splitext(os.path.basename(path))[0]
            cv2.putText(img, word, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,0,255), 2)
            # hiển thị ảnh 1.5s
            for _ in range(int(fps * 1.5)):
                out.write(img)
        # ===== VIDEO =====
        elif ext in [".mp4", ".avi", ".mov"]:
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                print("❌ Cannot open video:", path)
                continue
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if width is None:
                    height, width = frame.shape[:2]
                    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                else:
                    frame = cv2.resize(frame, (width, height))
                word = os.path.splitext(os.path.basename(path))[0]
                cv2.putText(frame, word, (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0,0,255), 2)
                out.write(frame)
            cap.release()
        else:
            print("⚠️ Unsupported format:", path)
    if out:
        out.release()
        print("✅ Final video:", output_path)
        return output_path
    else:
        print("❌ No output created")
        return None
# Save database
def create_word(word, video, images, source, nlpword):
    try:
        conn1 = get_connection()
        cursor = conn1.cursor()
        sql = "INSERT INTO text2sign (word, video, images, source, nlpword) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(
            sql,
            (word, video, images, source, str(nlpword))
        )
        conn1.commit()
        conn1.close()
        print("✅ Saved:", word)
    except Error as e:
        print("❌ DB error:", e)
#hàm main
if __name__ == "__main__":
    uvicorn.run(
        fast_app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        log_config=None
    )