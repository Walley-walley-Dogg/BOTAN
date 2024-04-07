import telebot
from pytube import YouTube

bot = telebot.TeleBot('6376347293:AAHKkjC5kaMJmuQpjrPhjDxUdF7Cb0rRO9I')


@bot.message_handler(commands=['start', 'help'])
def start(message):
        bot.send_message(message.from_user.id, 'Привет, я бот, который конвертирует отправленные видео в MP4 файлы')


@bot.message_handler(commands=['download'])
def download_video(message):
        bot.send_message(message.from_user.id, 'Скинь ссылку и формат через пробел')
        bot.register_next_step_handler(message, get_video)     

def get_video(message):
        try:
            url, format = message.text.split()[0], message.text.split()[1]
            yt = YouTube(url)
            video = yt.streams.filter(file_extension=format).first()
            video_path = 'D:\\BOTAN\\videos'
            video.download(video_path)
            video_file = open(f'{video_path}\\{yt.title}.mp4', 'rb')
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, video_file)
        except Exception as e:
            bot.reply_to(message, f'Произошла ошибка: {e}')



bot.polling(non_stop=True)