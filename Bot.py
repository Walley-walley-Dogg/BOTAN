import telebot
from telebot import types
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

bot = telebot.TeleBot('6376347293:AAHKkjC5kaMJmuQpjrPhjDxUdF7Cb0rRO9I')


@bot.message_handler(commands=['start', 'help'])
def start(message):
        bot.send_message(message.from_user.id, "Hello! I'm a bot that can manage your youtube account. Pick an option below.")
        keyboard = types.InlineKeyboardMarkup(); 
        key_download_video = types.InlineKeyboardButton(text='Download Video', callback_data='Download_Video')

        key_video_to_audio = types.InlineKeyboardButton(text='Convert Video to Audio', callback_data='Convert_Video_to_Audio')
        keyboard.add(key_video_to_audio, key_download_video)

        bot.send_message(message.chat.id, "Pick option:", reply_markup=keyboard)





          

@bot.message_handler(commands=['download'])
def download_video(message):
        bot.send_message(message.from_user.id, "Send a link and format like in example: 'link format' ")
        bot.register_next_step_handler(message, get_video)     

@bot.message_handler(commands=['VideoToAudio'])
def Video_to_Audio(message):
        bot.send_message(message.from_user.id, "Send a youtube video link and how you'd like to name audio file: 'link, file name'")
        bot.register_next_step_handler(message, get_vid_toAud)     

def get_video(message):
        try:
            url, format = message.text.split()[0], message.text.split()[1]
            yt = YouTube(url)
            bot.send_message(message.from_user.id, "Getting the video...")
            yt.streams.first()
            video = yt.streams.filter(file_extension=format).first()
            video_path = '\\videos'
        
            video.download(video_path)

            video_file = open(f'{video_path}\\{video.default_filename}', 'rb')
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, video_file)
        except Exception as e:
            bot.reply_to(message, f'Oops! An error occured! {e}')

def get_vid_toAud(message):
        try:
            url = message.text.split(", ")[0]
            yt = YouTube(url)
            bot.send_message(message.from_user.id, "Getting the video...")
            stream = yt.streams.filter(file_extension='mp4').first()
            video_path = stream.download("\\videos")
            
            
            output_dir = 'audios'
            os.makedirs(output_dir, exist_ok=True)

            video = VideoFileClip(video_path)

            
            audio_path = os.path.join(output_dir, message.text.split(", ")[1])

            video.audio.write_audiofile(f'{audio_path}.mp3', codec='libmp3lame')

            bot.send_chat_action(message.chat.id, 'upload_audio')

            audio_file = open(f'{audio_path}.mp3', 'rb')
            bot.send_audio(message.chat.id, audio_file)

            video.close()

        except Exception as e:
            bot.reply_to(message, f'Oops! An error occured! {e}')




bot.polling(non_stop=True)