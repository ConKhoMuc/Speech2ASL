import subprocess
import uuid
import os

def convert_video_to_browser_format(input_path, output_dir="uploads"):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(
        output_dir,
        f"final.mp4"
    )

    command = [
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx264",   # video chuẩn browser
        "-acodec", "aac",       # audio chuẩn browser
        "-strict", "experimental",
        "-y",
        output_path
    ]

    try:
        subprocess.run(command, check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        print("✅ Converted:", output_path)
        return output_path

    except subprocess.CalledProcessError:
        print("❌ Convert failed:", input_path)
        return None