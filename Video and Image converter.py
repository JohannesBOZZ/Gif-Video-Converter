import os # just for the file extension in line 24
import customtkinter as ctk
import tkinter
import time
from datetime import datetime
from cofig import *
# Default theme for CustomTKinter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('900x563')
root.title("Converter")
root.resizable(False,False)


def GUI():
    start_time = time.time()

    print(scale_factor_entry.get())
    input_folder = Input_entry.get()
    output_folder = output_entry.get()
    codec_gui = option_menu_codec.get()
    codec = codec_gui_to_normal[codec_gui]
    new_file_format = option_menu_convert.get()
    gif_program = option_menu_gif_program.get()

    if scale_factor_entry.get() == '':
        scale = None
    else:
        scale = float(scale_factor_entry.get())

    if scale_width_entry.get() or scale_hight_entry.get() != '':
        px_scale = (int(scale_width_entry.get()), int(scale_hight_entry.get()))
    else:
        px_scale = None

    new_fps = None
    if fps_entry.get() != '':
        new_fps = int(fps_entry.get())

    if bitrate_entry.get() =='':
        bitrate = None
    else:
        bitrate = f'{bitrate_entry.get()}k'

    if output_folder == '':
        output_folder = input_folder + r'\Converted'
    # creates the ouput folder
    if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    print('-------------------------------------------------------------------')
    print(input_folder, output_folder, scale, px_scale, new_fps, bitrate, codec, new_file_format)
    print('-------------------------------------------------------------------')
    converted_count = 0
    if option_menu_from.get() == 'video' and option_menu_convert.get() not in ['mp3', 'webp', 'gif']:
        count = convert_videos_or_animated_image_to_video(input_folder, output_folder, scale, px_scale, new_fps, bitrate, codec, new_file_format)
        for file_count, end in count:
            print(file_count, '/', end)
            update_bar(file_count, end)
            converted_count = file_count
    elif option_menu_convert.get() == 'gif':
        count = convert_to_gif(input_folder, output_folder, scale, px_scale, new_fps, gif_program)
        for file_count, end in count:
            print(file_count, '/', end)
            update_bar(file_count, end)
            converted_count = file_count
    elif option_menu_convert.get() == 'webp':
        count = convert_video_to_webp(input_folder, output_folder, scale, px_scale, new_fps)
        for file_count, end in count:
            print(file_count, '/', end)
            update_bar(file_count, end)
            converted_count = file_count
    elif option_menu_convert.get() == 'mp3':
        count = convert_to_mp3(input_folder, output_folder, bitrate)
        for file_count, end in count:
            print(file_count, '/', end)
            update_bar(file_count, end)
            converted_count = file_count

    #elif option_menu_convert.get() == 'gif':
    #    count = convert_to_gif
    #print(f'{count} files converted')
    end_time = time.time()
    # calculates the time taken
    execution_time = end_time - start_time
    # converts the time in min and sec or only sec
    if execution_time >= 60:
        execution_time = execution_time /60
        minutes = int(execution_time)
        seconds = float((execution_time - minutes) * 60)
        process_time = f' in {minutes}min {round(seconds, 1)}s'
    elif execution_time >= 3600:
        hours = execution_time // 3600
        minutes = (execution_time % 3600) // 60
        seconds = execution_time % 60
        process_time = f' in {hours}h {minutes}min {round(seconds, 1)}s'
    else:
        process_time = f' in {round(execution_time, 1)}s'
    # real time
    now = datetime.now()
    # message after process is done
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] sucessfully converted {converted_count} files {process_time}\n')
    status_textbox.configure(state="disabled")

def mode(self):
    from_mode = option_menu_from.get()
    to_mode = option_menu_convert.get()
    option_menu_convert.configure(values=what_format[from_mode])
    option_menu_codec.configure(values=what_codec_gui[to_mode])
    if to_mode in ['mp3', 'webp', 'gif']:
        option_menu_codec.place_forget()
        option_menu_gif_program.place(relx=0.63, rely=row2, anchor=tkinter.W)
    elif to_mode not in ['mp3', 'webp', 'gif']:
        option_menu_codec.place(relx=0.63, rely=row2, anchor=tkinter.W)
        option_menu_gif_program.place_forget()
def update_bar(current, end):
    Value = int(current) / int(end)
    progress_bar_text.configure(text=f'{round(Value * 100)}% | {current} of {end}')
    progress_bar_text.update()
    progress_bar.set(Value)
    progress_bar.update()


row1 = 0.2
row2 = 0.3
row3 = 0.4
# GUI Styling
frame = ctk.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)

label = ctk.CTkLabel(master=frame,
                               text='Converter',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.06, anchor=tkinter.CENTER)

Input_entry = ctk.CTkEntry(master=frame, 
                                    placeholder_text='Input folder',
                                    font=('sora', 16),
                                    width=490,
                                    height=24,
                                    corner_radius=5)
Input_entry.place(relx=0.02, rely=row1, anchor=tkinter.W)
# button to start download process
output_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='Output folder (default is `Input folder`)',
                            font=("sora", 16),
                            width=490,height=24,
                            corner_radius=5)
output_entry.place(relx=0.02, rely=row2, anchor=tkinter.W)


# entry for quality by jpg
jpg_quality = ctk.CTkEntry(master=frame,
                            placeholder_text='Bitrate',
                            font=("sora", 16),
                            width=150,
                            height=24,
                            corner_radius=5)

convert_only_from_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='from',
                                bg_color='transparent')
convert_only_from_lable.place(relx=0.63, rely=row1, anchor=tkinter.W)
# menu for changing the sort mode
option_menu_from = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 16),
                                width=100,
                                height=24,
                                corner_radius=5,
                                values=["video", "gif"],
                                command=mode,)
option_menu_from.place(relx=0.7, rely=row1, anchor=tkinter.W)

to_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='to',
                                bg_color='transparent')
to_lable.place(relx=0.83, rely=row1, anchor=tkinter.W)
# menu for changing the convert mode
option_menu_convert = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 16),
                                width=100,
                                height=24,
                                corner_radius=5,
                                values=what_format['video'],
                                command=mode,)
option_menu_convert.place(relx=0.98, rely=row1, anchor=tkinter.E)
# if you wont AI generated images

option_menu_codec = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 16),
                                width=140,
                                height=24,
                                corner_radius=5,
                                values=what_codec_gui['mp4'],
                                command=mode,)
option_menu_codec.place(relx=0.63, rely=row2, anchor=tkinter.W)

option_menu_gif_program = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 16),
                                width=140,
                                height=24,
                                corner_radius=5,
                                values=['imageio', 'ffmpeg'],
                                command=mode,)

button = ctk.CTkButton(master=frame,
                                    font=('sora', 16),
                                    height=32,
                                    corner_radius=5,
                                    text='Convert',
                                    command=GUI)
button.place(relx=0.98, rely=row2, anchor=tkinter.E)
# textbox whith exit message

rezise_with_faktor_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='Rezise with factor',
                                bg_color='transparent')
rezise_with_faktor_lable.place(relx=0.02, rely=row3, anchor=tkinter.W)

scale_factor_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='factor',
                            font=("sora", 16),
                            width=70,
                            height=24,
                            corner_radius=5)
scale_factor_entry.place(relx=0.212, rely=row3, anchor=tkinter.W)

or_with_pixle_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='or with pixle',
                                bg_color='transparent')
or_with_pixle_lable.place(relx=0.315, rely=row3, anchor=tkinter.W)

scale_width_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='width',
                            font=("sora", 16),
                            width=80,
                            height=24,
                            corner_radius=5)
scale_width_entry.place(relx=0.455, rely=row3, anchor=tkinter.W)

x_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='X',
                                bg_color='transparent')
x_lable.place(relx=0.56, rely=row3, anchor=tkinter.W)

scale_hight_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='hight',
                            font=("sora", 16),
                            width=80,
                            height=24,
                            corner_radius=5)
scale_hight_entry.place(relx=0.582, rely=row3, anchor=tkinter.W)

fps_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='new fps',
                            font=("sora", 16),
                            width=100,
                            height=24,
                            corner_radius=5)
fps_entry.place(relx=0.71, rely=row3, anchor=tkinter.W)

bitrate_entry = ctk.CTkEntry(master=frame,
                            placeholder_text='bitrate',
                            font=("sora", 16),
                            width=100,
                            height=24,
                            corner_radius=5)
bitrate_entry.place(relx=0.98, rely=row3, anchor=tkinter.E)

status_textbox = ctk.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=824,
                                        height=230,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.692, anchor=tkinter.CENTER)
status_textbox.configure(state="disabled")

progress_bar = ctk.CTkProgressBar(master=frame,
                                width=700,
                                mode='determinate',)
progress_bar.place(relx=0.02, rely=0.97, anchor=tkinter.W)
progress_bar.set(0)

progress_bar_text = ctk.CTkLabel(master=frame,
                                text='0% | 0 of 0',
                                bg_color='transparent')
progress_bar_text.place(relx=0.86, rely=0.97, anchor=tkinter.W)

root.mainloop()
