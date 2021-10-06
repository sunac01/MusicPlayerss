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

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from pyrogram import Client, emoji
from utils import mp, playlist
from config import Config


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



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await mp.get_admins(Config.CHAT)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "😒 Played Joji.mp3",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty Playlist"
        else:
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Toplam ilk 25 şarkı listeleniyor {len(playlist)} Şarkılar.\n"
                pl += f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(
                    f"{pl}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏯", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Toplam ilk 25 şarkı listeleniyor  {len(playlist)} Şarkılar.\n"
                pl += f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused\n\n{pl},",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="resume"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass
    
    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Toplam ilk 25 şarkı listeleniyor {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                    ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed\n\n{pl}",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            if len(playlist)>=25:
                tplaylist=playlist[:25]
                pl=f"Toplam ilk 25 şarkı listeleniyor {len(playlist)} songs.\n"
                pl += f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}"
                    for i, x in enumerate(tplaylist)
                ])
            else:
                pl = f"{emoji.PLAY_BUTTON} **Çalma listesi**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Tarafından talep edildi:** {x[4]}\n"
                    for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Skipped\n\n{pl}",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                        ],
                    ]
                )
            )
        except MessageNotModified:
            pass

    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('⚙️ Kanalımız', url='https://t.me/NetdBots'),
                InlineKeyboardButton('🧩 Sahip', url='https://t.me/Azerbesk'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        try:
            await query.edit_message_text(
                HELP,
                reply_markup=reply_markup

            )
        except MessageNotModified:
            pass

