import tkinter
import customtkinter
from tkinter import ttk, filedialog
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import AudioFileClip
import os
import datetime

download_format = None

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)

        selected_format = download_format.get()

        if selected_format == 0:  # MP4 format
            # Get available video streams
            video_streams = ytObject.streams.filter(file_extension="mp4")

            # Extract the resolutions from the video streams
            resolutions = [stream.resolution for stream in video_streams]

            # Create a dropdown menu for resolution selection
            resolution_variable = tkinter.StringVar(app)
            resolution_variable.set(resolutions[0])  # Set the default resolution

            resolution_label = customtkinter.CTkLabel(app, text="Select resolution:")
            resolution_label.pack()

            style = ttk.Style(app)
            style.configure('Custom.TMenubutton', background='white', relief='solid', borderwidth=1, padding=6)
            resolution_menu = ttk.OptionMenu(app, resolution_variable, *resolutions, style='Custom.TMenubutton')
            resolution_menu.pack()

            # Wait for the user to select a resolution
            app.wait_variable(resolution_variable)

            selected_resolution = resolution_variable.get()

            # Find the selected resolution stream
            video = video_streams.get_by_resolution(selected_resolution)

            title.configure(text=ytObject.title, text_color="white")
            finishLabel.configure(text="")
            
            # Prompt the user for the save location for the video
            save_path_video = filedialog.askdirectory()
            
            # Set the save path for the video
            video.download(output_path=save_path_video)
            
            # Reset progress bar and hide resolution selector
            progressBar.set(0)
            progress.configure(text="0%")
            resolution_label.pack_forget()
            resolution_menu.pack_forget()
            
        elif selected_format == 1:  # MP3 format
            audio_stream = ytObject.streams.get_audio_only()
            audio_file_name = f"audio_{ytObject.video_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            
            # Prompt the user for the save location for the MP3 file
            save_path_mp3 = filedialog.askdirectory()
            
            audio_stream.download(output_path=save_path_mp3, filename=audio_file_name)
            
            # Convert the downloaded audio file to MP3 format
            mp4_path = os.path.join(save_path_mp3, audio_file_name)
            mp3_file_name = f"audio_{ytObject.video_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            mp3_path = os.path.join(save_path_mp3, mp3_file_name)
            
            audio = AudioFileClip(mp4_path)
            audio.write_audiofile(mp3_path)
            
            # Close the audio file
            audio.close()

            # Delete the original MP4 audio file
            os.remove(mp4_path)
            
            # Reset progress bar
            progressBar.set(0)
            progress.configure(text="0%")

        finishLabel.configure(text="Video Downloaded!")
    except RegexMatchError:
        finishLabel.configure(text="Invalid YouTube link", text_color="red")
    except Exception as e:
        print("Error downloading video:", str(e))
        finishLabel.configure(text="Error downloading video", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    progress.configure(text=per + '%')
    progress.update()

    # Update progress bar
    progressBar.set(float(percentage_of_completion) / 100)

#system Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Christian YouTube Downloader")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube link.")
title.pack(padx=10, pady=10)

# Link input
url_variable = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_variable)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress bar
progress = customtkinter.CTkLabel(app, text="0%")
progress.pack()

progressBar= customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Download format selection
download_format = tkinter.IntVar()
radio_mp4 = customtkinter.CTkRadioButton(app, text="MP4", variable=download_format, value=0)
radio_mp4.pack()
radio_mp3 = customtkinter.CTkRadioButton(app, text="MP3", variable=download_format, value=1)
radio_mp3.pack()

# Run app
app.mainloop()