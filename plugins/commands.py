#MIT License

#Copyright (c) 2021 SUBIN

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from utils import USERNAME, mp
from config import Config
U=USERNAME
CHAT=Config.CHAT
msg=Config.msg
HOME_TEXT = "<b>Merhaba, [{}](tg://user?id={})\n\nBen NetdVoiceBot Kanallarınızın Ve Gruplarınızın Sesli Sohbetinde Müzik Çalabilirim\n\nHatta Sesli Sohbetinizde Youtube Canlı Akışı yapabilirim.\n\nYardım Almak İçin /help Komutunu Yazın.</b>"
HELP = """

<b>
Bir ses dosyasına veya youtube bağlantısına yanıt olarak /play <şarkı adı> kullanın veya /play'i kullanın.
Bir youtube çalma listesindeki tüm şarkıları çalmak için /yplay'i kullanın.
Jio Saavn'dan bir şarkı çalmak için <code>/splay şarkı adı</code>'nı veya bir jiosaavn albümündeki veya /cplay <kanalındaki tüm şarkıları çalmak için <code>/splay -a albüm adı</code>'nı da kullanabilirsiniz. kullanıcı adı veya kanal kimliği> bir telgraf kanalından müzik çalmak için.</b>

**Ortak Komutlar**:

**/play**  Oynatmak için bir ses dosyasına veya YouTube bağlantısına yanıt verin veya /play <şarkı adı> öğesini kullanın.
**/splay** Jio Saavn'dan müzik çalın, o albümdeki tüm şarkıları çalmak için /splay <şarkı adı> veya <code>/splay -a albüm adı</code> kullanın.
**/player**  Çalmakta olan şarkıyı göster.
**/upload** Çalmakta olan şarkıyı ses dosyası olarak yükler.
**/help** Komutlar için yardımı göster
**/playlist** Shows the playlist.

**Admin Komutlar**:
**/skip** [n] ... Sonraki Şarkıya Atlar
**/cplay** Bir kanalın müzik dosyalarından müzik çalın.
**/yplay** Bir youtube çalma listesinden müzik çalın.
**/join**  Sesli sohbete katılır.
**/leave**  Mevcut sesli sohbetten ayrılır.
**/shuffle** Çalma Listesini Karıştırır.
**/vc**  Hangi VC'nin birleştirildiğini kontrol edin.
**/stop**  Oynatmayı durdur.
**/radio** Radyoyu Başlatın.
**/stopradio** Radyo Akışını durdurur.
**/clearplaylist** Oynatma listesini temizle
**/export** Mevcut çalma listesini ileride kullanmak üzere dışa aktarın.
**/import** Önceden dışa aktarılan bir oynatma listesini içe aktarın.
**/replay**  Baştan oynatın.
**/clean** Kullanılmayan RAW PCM dosyalarını kaldırın.
**/pause** Oynatmayı duraklat.
**/resume** Oynatmaya devam et.
**/volume** Sesi değiştir (0-200).
**/mutevc**   VC'de sessize alın.
**/unmutevc**  VC'de sesi açın.
**/restart**  Bot'u günceller ve yeniden başlatır.
"""




@Client.on_message(filters.command(['start', f'start@{U}']))
async def start(client, message):
    buttons = [
        [
                InlineKeyboardButton('⚙️ Kanalımız', url='https://t.me/NetdBots'),
                InlineKeyboardButton('🧩 Sahip', url='https://t.me/Azerbesk'),
    ],
    [
        InlineKeyboardButton('👨🏼‍🦯 Yardım', callback_data='help'),
        
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)



@Client.on_message(filters.command(["help", f"help@{U}"]))
async def show_help(client, message):
    buttons = [
        [
                InlineKeyboardButton('⚙️ Kanalımız', url='https://t.me/NetdBots'),
                InlineKeyboardButton('🧩 Sahip', url='https://t.me/Azerbesk'),
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_text(
        HELP,
        reply_markup=reply_markup
        )
    await mp.delete(message)
