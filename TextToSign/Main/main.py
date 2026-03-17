from NLPText import nlptext
from TextToSign.Database.ConnectDB import connect_mysql
from mysql.connector import Error
import cv2
import os

def play_media(media_list):

    for media_type, word, path in media_list:

        if media_type == "video":
            play_videos([(word, path)])

        elif media_type == "image":
            play_images(word, path)

def play_videos(video_list):

    for word, path in video_list:

        if not os.path.exists(path):
            print("❌ File not found:", path)
            continue

        cap = cv2.VideoCapture(path)

        if not cap.isOpened():
            print("❌ Cannot open:", path)
            continue

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.2
            thickness = 3

            # lấy kích thước frame
            frame_height, frame_width, _ = frame.shape

            # lấy kích thước text
            (text_width, text_height), _ = cv2.getTextSize(
                word, font, font_scale, thickness
            )

            # tính vị trí center-top
            x = int((frame_width - text_width) / 2)
            y = 50

            cv2.putText(
                frame,
                word,
                (x, y),
                font,
                font_scale,
                (0, 0, 255),
                thickness,
                cv2.LINE_AA
            )

            cv2.imshow("Sign Language Player", frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()

    cv2.destroyAllWindows()


def play_images(word, path):

    if not os.path.exists(path):
        print("❌ Image not found:", path)
        return

    img = cv2.imread(path)

    if img is None:
        print("❌ Cannot open image:", path)
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    thickness = 3

    h, w, _ = img.shape

    (text_w, text_h), _ = cv2.getTextSize(
        word, font, font_scale, thickness
    )

    x = int((w - text_w) / 2)
    y = 50

    cv2.putText(
        img,
        word,
        (x, y),
        font,
        font_scale,
        (0,0,255),
        thickness,
        cv2.LINE_AA
    )

    cv2.imshow("Sign Language Player", img)

    cv2.waitKey(1500)  # hiển thị 1.5s
    cv2.destroyAllWindows()


def get_video_by_word(conn, word):
    try:
        cursor = conn.cursor()

        sql = "SELECT video FROM text2sign WHERE word = %s"
        cursor.execute(sql, (word,))

        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    except Error as e:
        print("❌ Database error:", e)
        return None


def convert_words_to_media(conn, word_list):

    cursor = conn.cursor()

    media = []

    for word in word_list:

        sql = "SELECT word, video, image FROM text2sign WHERE word = %s"
        cursor.execute(sql, (word,))

        result = cursor.fetchone()

        if result:

            w, video, image = result

            if video:
                media.append(("video", w, video))

            elif image:
                media.append(("image", w, image))

            else:
                print("⚠️ No media for:", word)

        else:
            print("⚠️ No sign for:", word)

    return media


if __name__ == "__main__":

    # output từ NLP
    nlp_output = nlptext.convert_to_sign_structure(nlptext.text)

    conn = connect_mysql(
        host="localhost",
        user="root",
        password="123456@aB",
        database="text2sign"
    )

    if conn:

        print("🔎 NLP output:", nlp_output)

        media_list = convert_words_to_media(conn, nlp_output)

        print("\n🎥 Media list:")
        for m in media_list:
            print(m)

        play_media(media_list)

        conn.close()
        print("\n🔒 Closed connection to MySQL.")