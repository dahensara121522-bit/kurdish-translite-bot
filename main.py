import os
import telebot
from PIL import Image
import pytesseract
from googletrans import Translator

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8788687057:AAEqNyzHx_RccccxNT6Lqu--Q_IgOVF8Npl')

bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "بەخێربێیت! وێنەیەک بنێرە تا دەقەکەی بەشێوەی ڕاستەوخۆ بۆ بپشکنم و وەریبگێڕم بۆ کوردی.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "کەمێک چاوەڕێ بکە، وێنەکە دەخوێندرێتەوە...")
        
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_path = "photo.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)
        
        if not extracted_text.strip():
            bot.reply_to(message, "هیچ دەقێک لەم وێنەیەدا نەدۆزرایەوە!")
            return

        translated = translator.translate(extracted_text, dest='ckb')
        
        response = f"📝 **دەقی دەرهێنراو:**\n{extracted_text}\n\n☀️ **وەرگێڕانی کوردی:**\n{translated.text}"
        bot.reply_to(message, response, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"کێشەیەک ڕوویدا: {str(e)}")

bot.infinity_polling()
