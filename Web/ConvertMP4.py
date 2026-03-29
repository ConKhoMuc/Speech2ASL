import subprocess
import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
def convert_video_to_browser_format(input_path, result, output_dir="uploads"):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # sanitize filename
    filename = result.replace(" ", "_").lower()

    output_path = os.path.join(
        output_dir,
        f"{filename}.mp4"
    )

    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-y",
        output_path
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print("✅ Converted:", output_path)

        # return url path
        return output_path.replace("\\", "/")

    except subprocess.CalledProcessError:
        print("❌ Convert failed:", input_path)
        return None
#convert_video_to_browser_format(
  #  r"C:\Users\trungnh\PycharmProjects\Speech2ASL\text2sign\video/happy.mp4",
  #  "happy"
#)
#C:\ffmpeg\bin\ffmpeg.exe -i C:\Users\trungnh\PycharmProjects\Speech2ASL\uploads\happy.mp4 C:\Users\trungnh\PycharmProjects\Speech2ASL\uploads\happy1.mp4