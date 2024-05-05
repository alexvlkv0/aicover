import os
import subprocess
from pytube import YouTube

def downloadYT(link="https://www.youtube.com/watch?v=nsfAj5wDBA0"):
    parent_dir = os.path.join(os.getcwd(),'audio')
    yt = YouTube(link).streams.filter(only_audio=True)
    file = yt.first().download(parent_dir)
    print(f'Downloaded {file}')

    default_filename = yt.first().default_filename
    print(f'converting {default_filename}')
    new_filename = default_filename[:default_filename.rfind('.')].replace(" ", "") + '.flac'
    subprocess.run([
        'ffmpeg',
        '-i', os.path.join(parent_dir, default_filename),
        os.path.join(parent_dir+"\\queue", new_filename)
    ])
    print(f'Converted {new_filename}')
    os.remove(file)
    
    return os.path.join(parent_dir+"\\queue", new_filename)

if __name__ == "__main__":
    a = downloadYT('https://www.youtube.com/watch?v=Z-XilpjO5xw')
    print(a)

#subprocess.run(['spleeter', 'separate', '-p', 'spleeter:2stems', '-o', 'output', file], capture_output=True)