import os
import subprocess

ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"

input_folder = r"C:\Users\trungnh\PycharmProjects\Speech2ASL\text2sign\video"
output_folder = r"C:\Users\trungnh\PycharmProjects\Speech2ASL\uploads"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):

    if file.endswith(".mp4"):

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        cmd = [
            ffmpeg,
            "-i", input_path,
            "-vcodec", "libx264",
            "-acodec", "aac",
            "-movflags", "+faststart",
            output_path
        ]

        print("Converting:", file)

        subprocess.run(cmd)

print("Done convert all videos")