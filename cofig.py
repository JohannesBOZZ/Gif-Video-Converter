import os
from skimage.transform import resize
from moviepy.editor import *
from pathlib import Path
from PIL import Image
# not used
what_codec = {
        '.mp4': ['libx264', 'libx265'],# bitrate ja
        '.avi': ['libx264', 'libvpx', 'libvpx-vp9'],# bitrate ja
        '.mov':['libx264', 'libx265'],# bitrate ja
        '.mkv': ['libx264', 'libx265', 'libvpx'],# bitrate ja
        '.webm': ['libvpx', 'libvpx-vp9'],# bitrate ja
        }
# converts the what_codec_gui names to a name that ffmpeg can use
codec_gui_to_normal = {
    'H.264': 'libx264',
    'H.265': 'libx265',
    'VP8': 'libvpx',
    'VP9': 'libvpx-vp9',
}

what_codec_gui = {
        'mp4': ['H.264', 'H.265'],# bitrate ja
        'avi': ['H.264', 'VP8', 'VP9'],# bitrate ja
        'mov':['H.264', 'H.265'],# bitrate ja
        'mkv': ['H.264', 'H.265', 'VP8'],# bitrate ja
        'webm': ['VP8', 'VP9'],# bitrate ja
        'gif': [''],
        'webp': [''],
        'mp3': [''],
        }

what_format ={
    'video': ["mp4", "avi", "mov", "mkv", "gif", "webm", "webp", "mp3" ],
    'gif': ["mp4", "avi", "mov", "mkv", "gif", "webm", "webp" ],
    'webp': [".mp4" ],
}

file_format = (".mp4", ".avi", ".mov", ".mkv", ".gif", ".webm")

def convert_videos_or_animated_image_to_video(input_path, output_path, scale_factor=None, scale=None, fps=None, bitrate='8000k', codec=None, new_file_format=None):
    # Liste aller Dateien im angegebenen Ordner abrufen
    file_list = os.listdir(input_path)
    file_count = 0
    end=0
    for file_name in file_list: 
        if file_name.endswith(file_format): end+=1
    for file_name in file_list:
        # Überprüfen, ob es sich um eine Videodatei handelt
        if file_name.endswith(file_format):
            video_path = os.path.join(input_path, file_name)

            # Video mit MoviePy laden
            video = VideoFileClip(video_path)

            # Skalierung des Videos anwenden, falls angegeben
            if scale is not None:
                video = video.resize(scale)
            elif scale_factor is not None and scale is None:
                width, height = video.size
                scale = (width*scale_factor, height*scale_factor)
                video = video.resize(scale)
            # FPS des Videos abrufen
            clip_fps = video.fps
            if fps:
                clip_fps = fps
            # Ausgabe-Dateipfad für die MP4-Datei erstellen
            mp4_file_name = os.path.splitext(file_name)[0] + f".{new_file_format}"
            mp4_file_path = os.path.join(output_path, mp4_file_name)

            # MP4-Datei erstellen und speichern
            video.write_videofile(mp4_file_path, fps=clip_fps, bitrate=bitrate, codec=codec)

            # Video-Clip freigeben
            video.close()
            file_count += 1
            yield file_count, end
    return 
            
#convert_videos_or_animated_image_to_video(r"E:\temp\mp4", r"E:\temp\mp4\new", codec = 'libx264', scale=(1920, 1080))


def convert_to_gif(input_path, output_path, scale_factor=None, scale=None, fps=None, program='imageio'):
    # Liste aller Dateien im angegebenen Ordner abrufen
    file_list = os.listdir(input_path)
    file_count = 0
    end=0
    for file_name in file_list: 
        if file_name.endswith(file_format): end+=1
    for file_name in file_list:
        # Überprüfen, ob es sich um eine Videodatei handelt
        if file_name.endswith(file_format):
            file_path = os.path.join(input_path, file_name)

            # Video mit MoviePy laden
            video = VideoFileClip(file_path)

            # Skalierung des Videos anwenden, falls angegeben
            if scale is not None:
                video = video.resize(scale)
            elif scale_factor is not None and scale is None:
                width, height = video.size
                scale = (width*scale_factor, height*scale_factor)
                video = video.resize(scale)
            clip_fps = video.fps
            if fps:
                clip_fps = fps
            # GIF erstellen und speichern
            gif_file_name = os.path.splitext(file_name)[0] + ".gif"
            gif_file_path = os.path.join(output_path, gif_file_name)
            video.write_gif(gif_file_path, fps=clip_fps, program=program)

            video.close()
            file_count += 1
            yield file_count, end
    return 

def convert_video_to_webp(input_path, output_path, scale_factor=None, scale=None, fps=None):
    # Erstelle den Zielordner, wenn er nicht existiert
    file_list = os.listdir(input_path)
    file_count = 0
    end=0
    for file_name in file_list: 
        if file_name.endswith(file_format): end+=1
    # Durchsuche den Eingabeordner nach Dateien mit den unterstützten Formaten
    supported_formats = (".mp4", ".avi", ".mov", ".mkv", ".gif", ".webm")
    for filename in file_list:
        if filename.endswith(supported_formats):
            input_file = os.path.join(input_path, filename)
            output_file = os.path.join(output_path, os.path.splitext(filename)[0] + ".webp")
            video = VideoFileClip(input_file)
            
            if scale is not None:
                video = video.resize(scale)
            elif scale_factor is not None and scale is None:
                width, height = video.size
                scale = (width*scale_factor, height*scale_factor)
                video = video.resize(scale)

            # Prüfe den Dateityp und konvertiere entsprechend
            if filename.endswith((".mp4", ".avi", ".mov", ".mkv", ".webm")):
                # Konvertiere MP4 zu WebP
                target_fps = video.fps
                if fps:
                    target_fps = fps
                frame_duration = int((1.0 / target_fps) * 1000)
                frames = [frame for frame in video.iter_frames()]
                imageio.mimsave(output_file, frames, format="webp", duration=frame_duration)
            elif filename.endswith(".gif"):
                # Konvertiere GIF zu WebP
                gif_reader = imageio.get_reader(input_file)
                gif_meta = gif_reader.get_meta_data()
                frame_duration = gif_meta['duration']
                if fps:
                    target_fps = fps
                    frame_duration = int((1.0 / target_fps) * 1000)
                frames = [frame for frame in gif_reader]
                if scale is not None or scale_factor is not None:
                    target_resolution = (scale[1], scale[0])
                    frames = [resize(frame, target_resolution, preserve_range=True).astype(frame.dtype) for frame in frames]
                imageio.mimsave(output_file, frames, format="webp", duration=frame_duration)

            file_count += 1
            video.close()
            yield file_count, end
    return 


def convert_image_to_webp(input_path, output_path, scale_factor=None, scale=None, quality=90):
    # Erstelle den Zielordner, wenn er nicht existiert
    file_list = os.listdir(input_path)
    file_count = 0
    end=0
    for file_name in file_list: 
        if file_name.endswith(file_format): end+=1
    # Durchsuche den Eingabeordner nach Dateien mit den unterstützten Formaten
    supported_formats = (".jpg", ".jepg", ".png", ".webp")
    for filename in file_list:
        if filename.endswith(supported_formats):
            input_file = os.path.join(input_path, filename)
            output_file = os.path.join(output_path, os.path.splitext(filename)[0] + ".webp")
            image = Image.open(input_file)
            
            if scale is not None:
                image = image.resize(scale)
            elif scale_factor is not None and scale is None:
                width, height = image.size
                scale = (int(width*scale_factor), int(height*scale_factor))
                image = image.resize(scale)

            # Prüfe den Dateityp und konvertiere entsprechend

            image.save(output_file, format="webp", optimize = True, quality = quality)
            file_count += 1
            image.close()
            yield file_count, end
    return 


def convert_to_mp3(input_path, output_path, bitrate=None):
    # Überprüfe, ob der Ausgabeordner existiert, wenn nicht, erstelle ihn
    file_list = os.listdir(input_path)
    file_count = 0
    end=0
    for file_name in file_list: 
        if file_name.endswith(file_format): end+=1
    # Durchlaufe alle Dateien im Eingabeordner
    for file_name in file_list:
        if file_name.endswith(".mp4"):
            try:
                # Konstruiere die vollständigen Pfadangaben für Eingabe- und Ausgabedateien
                input_file = os.path.join(input_path, file_name)
                output_file = os.path.join(output_path, os.path.splitext(file_name)[0] + ".mp3")

                # Konvertiere MP4 zu MP3
                video = VideoFileClip(input_file)
                audio = video.audio
                audio.write_audiofile(output_file, bitrate=bitrate)
                audio.close()
                file_count += 1

            except Exception as e:
                print(e)
            yield file_count, end
    return 