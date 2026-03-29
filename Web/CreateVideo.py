import cv2
import os




def merge_files_to_video(file_list, output_path="final.mp4", fps=25):

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