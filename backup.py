import telebot
from telebot import types
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

bot = telebot.TeleBot('6376347293:AAHKkjC5kaMJmuQpjrPhjDxUdF7Cb0rRO9I')

user_states = {}

@bot.message_handler(commands=['start', 'help'])
def start(message):
        
        keyboard = types.InlineKeyboardMarkup(); 
       
        key_download_video = types.InlineKeyboardButton(text='Download Video', callback_data='Download_Video')
        key_video_to_audio = types.InlineKeyboardButton(text='Convert Video to Audio', callback_data='Convert_Video_to_Audio')
        
        keyboard.add(key_video_to_audio, key_download_video)

        bot.send_message(message.chat.id, "Hello! I'm a bot that can manage your youtube account. Pick an option.", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def handle_options_button(call):
        user_id = call.from_user.id
        if call.data == 'Download_Video':
               user_states[user_id] = 'download_video'
               bot.send_message(call.message.chat.id, "Send a link")        
        elif call.data == 'Convert_Video_to_Audio':
                user_states[user_id] = 'convert_video_to_audio'
                bot.send_message(call.message.chat.id, "Send a youtube video link and how you'd like to name audio file: 'link, file name'")
        elif call.data == "360p":
              quality = "360p"

@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_user_response(message):
    user_id = message.from_user.id
    state = user_states.pop(user_id)  
    if state == 'download_video':
        get_video(message)
    elif state == 'convert_video_to_audio':
        get_vid_toAud(message)


def get_video(message):
        try:
            
            url = message.text
        #     format = "mp4"
            yt = YouTube(url)
            
            keyboard = types.InlineKeyboardMarkup(); 
            key_720p = types.InlineKeyboardButton(text='720p', callback_data='720p')
            key_360p = types.InlineKeyboardButton(text='360p', callback_data='360p')
            keyboard.add(key_720p, key_360p)
           
            bot.send_message(message.from_user.id, "pick the video quality", reply_markup=keyboard)
           
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