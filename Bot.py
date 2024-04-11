import telebot
from telebot import types
from pytube import YouTube



bot = telebot.TeleBot('6376347293:AAHKkjC5kaMJmuQpjrPhjDxUdF7Cb0rRO9I')


user_states = {}
links=[]
selected_audio_formats = []


@bot.message_handler(commands=['start', 'help'])
def start(message):
        

        bot.send_message(message.chat.id, "Hello! I'm a bot that can manage your youtube account.")
        initialize_main_buttons(message.chat.id)

def initialize_main_buttons(chat_id):
        keyboard = types.InlineKeyboardMarkup(); 
       
        key_download_video = types.InlineKeyboardButton(text='Download Video', callback_data='Download_Video')
        key_video_to_audio = types.InlineKeyboardButton(text='Convert Video to Audio', callback_data='Convert_Video_to_Audio')
        
        keyboard.add(key_video_to_audio, key_download_video)
        bot.send_message(chat_id,"Pick option",reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_options_button(call):
        user_id = call.from_user.id
        if call.data == 'Download_Video':
               user_states[user_id] = 'download_video'
               bot.delete_message(call.message.chat.id,call.message.id )
               bot.send_message(call.message.chat.id, "Send a link")        
        elif call.data == 'Convert_Video_to_Audio':
                user_states[user_id] = 'convert_video_to_audio'
                bot.delete_message(call.message.chat.id,call.message.id )
                bot.send_message(call.message.chat.id, "Send a youtube video link")
        elif call.data == '360p':
              bot.delete_message(call.message.chat.id, call.message.id)
              get_video(links.pop(),call.message.chat.id, '360p')
        elif call.data == '720p':
              bot.delete_message(call.message.chat.id, call.message.id)
              
              get_video(links.pop(),call.message.chat.id, '720p')
        elif call.data == '1080p':
              bot.delete_message(call.message.chat.id, call.message.id)
              
              get_video(links.pop(),call.message.chat.id, '1080p')
        elif call.data == '480p':
              bot.delete_message(call.message.chat.id, call.message.id)
              
              get_video(links.pop(),call.message.chat.id, '480p')
        elif call.data == '240p':
              bot.delete_message(call.message.chat.id, call.message.id)
              
              get_video(links.pop(),call.message.chat.id, '240p')    
        elif call.data == '1440p':
              bot.delete_message(call.message.chat.id, call.message.id)
              
              get_video(links.pop(),call.message.chat.id, '1440p') 
        elif call.data == '2160p':
              bot.delete_message(call.message.chat.id, call.message.id)
              get_video(links.pop(),call.message.chat.id, '2160p') 
        elif int(call.data) in selected_audio_formats:
              bot.delete_message(call.message.chat.id, call.message.id)
              get_vid_toAud(links.pop(), call.message.chat.id, call.data)
               

@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_user_response(message):
    user_id = message.from_user.id
    state = user_states.pop(user_id)  
    if state == 'download_video':
        links.append(message.text)
        get_quality(message)
    elif state == 'convert_video_to_audio':
        links.append(message.text)
        get_format(message)


def get_video(Url,chat_id, desired_quality):
        try:  
            yt = YouTube(Url)

            video_streams = yt.streams.all()
            
            selected_stream = None
            for stream in video_streams:
                  if stream.resolution == desired_quality and stream.includes_audio_track:
                        selected_stream = stream
                        break

            if selected_stream:
                video_path = '\\videos'
                bot.send_message(chat_id, "downloading the video...")
                selected_stream.download(video_path)

                video_file = open(f'{video_path}\\{selected_stream.default_filename}', 'rb')
                bot.send_chat_action(chat_id, 'upload_video')
                bot.send_video(chat_id, video_file)
                

                initialize_main_buttons(chat_id)
            else:
                  bot.send_message(chat_id, "Desired quality not found:(")
                  initialize_main_buttons(chat_id)
        except Exception as e:
            bot.send_message(chat_id, f'Oops! An error occured! {e}')
            initialize_main_buttons(chat_id)


def get_quality(message):
        keyboard = types.InlineKeyboardMarkup(); 

        key_720 = types.InlineKeyboardButton(text='720p', callback_data='720p')
        key_360 = types.InlineKeyboardButton(text='360p', callback_data='360p')
        key_1080 = types.InlineKeyboardButton(text='1080p', callback_data='1080p')
        key_480 = types.InlineKeyboardButton(text='480p', callback_data='480p')
        key_240 = types.InlineKeyboardButton(text='240p', callback_data='240p')
        key_1440 = types.InlineKeyboardButton(text='1440p', callback_data='1440p')
        key_2160 = types.InlineKeyboardButton(text='2160p', callback_data='2160p')

        keyboard.add(key_720, key_360, key_240, key_480, key_1080, key_1440, key_2160)
        bot.send_message(message.chat.id, "Pick quality", reply_markup=keyboard)
        

def get_vid_toAud(Url, chat_id, desired_format):
        try:
            yt = YouTube(Url)
            selected_audio_stream = yt.streams.get_by_itag(desired_format)
            audio_file_path = '\\audios'
            bot.send_message(chat_id, "downloading the audio...")

            selected_audio_stream.download(audio_file_path)
            
            with open(f'{audio_file_path}\\{selected_audio_stream.default_filename}', 'rb') as audio_file:
                  bot.send_audio(chat_id, audio_file)
            initialize_main_buttons(chat_id)

        except Exception as e:
            bot.send_message(chat_id, f'Oops! An error occured! {e}')
            initialize_main_buttons(chat_id)


def get_format(message):
    video_url = message.text

    # Create a YouTube object
    yt = YouTube(video_url)

    # Get available audio streams
    audio_streams = yt.streams.filter(only_audio=True)

    # Create inline keyboard with audio format buttons
    keyboard = types.InlineKeyboardMarkup()
    for stream in audio_streams:
        format_button = types.InlineKeyboardButton(text=stream.mime_type, callback_data=stream.itag)
        selected_audio_formats.append(stream.itag)
        keyboard.add(format_button)

    # Send message with keyboard
    bot.send_message(message.chat.id, "Pick audio format:", reply_markup=keyboard)
      

bot.polling(non_stop=True)