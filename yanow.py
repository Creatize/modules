__version__ = (1, 0, 1)

#
#                 █░░ █ ▀█▀ █▀▀
#                 █▄▄ █ ░█░ ██▄
#
#               © Copyright 2023
#
#          Licensed under the GNU AGPLv3
#      https://www.gnu.org/licenses/agpl-3.0.html


# meta developer: @ASNCT
# requires: git+https://github.com/MarshalX/yandex-music-api@dev aiohttp
# meta desc: Module for yandex music. Based on SpotifyNow


import logging
from asyncio import sleep

import aiohttp
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import Message
from yandex_music import ClientAsync

from .. import loader, utils

logger = logging.getLogger(__name__)
logging.getLogger("yandex_music").propagate = False


@loader.tds
class YaNowMod(loader.Module):
    """Module for work with Yandex Music. Based on SpotifyNow"""

    strings = {
        "name": "YaNow",
        "no_token": "<b>🚫 Specify a token in config!</b>",
        "playing": "<b>🎧 Now playing: </b><code>{}</code><b> - </b><code>{}</code>\n<b>🕐 {}</b>",
        "no_args": "<b>🚫 Provide arguments!</b>",
        "best_result": (
            "<b>🥇 Best result type: </b><code>{}</code>"
            "\n"
            "{}"
            "\n"
            "<b>Artists: </b><code>{}</code>"
            "\n"
            "<b>Tracks: </b><code>{}</code>"
            "\n"
            "<b>Albums: </b><code>{}</code>"
            "\n"
            "<b>Playlists: </b><code>{}</code>"
            "\n"
            "<b>Videos: </b><code>{}</code>"
            "\n"
            "<b>Users: </b><code>{}</code>"
            "\n"
            "<b>Podcasts: </b><code>{}</code>"
        ),
        "track": "Track",
        "podcast": "Podcast",
        "podcast_episode": "Episode",
        "user": "User",
        "video": "Video",
        "album": "Album",
        "playlist": "Playlist",
        "artist": "Artist",
        "no_results": "<b>☹ No results found :(</b>",
        "autobioe": "<b>🔁 Autobio enabled</b>",
        "autobiod": "<b>🔁 Autobio disabled</b>",
        "lyrics": "<b>📜 Lyrics: \n{}</b>",
        "already_liked": "<b>🚫 Current playing track is already liked!</b>",
        "liked": "<b>❤ Liked current playing track!</b>",
        "not_liked": "<b>🚫 Current playing track not liked!</b>",
        "disliked": "<b>💔 Disliked current playing track!</b>",
        "my_vibe": '<b>🌊 You listening to track in "My Vibe", i can\'t recognize it.</b>',
        "_cfg_yandexmusictoken": "Yandex.Music account token",
        "_cfg_autobiotemplate": "Template for AutoBio",
        "no_lyrics": "<b>🚫 Track doesn't have lyrics.</b>",
        "guide": (
            '<a href="https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781">'
            "Instructions for obtaining a Yandex.Music token</a>"
        ),
    }

    strings_ru = {
        "no_token": "<b>🚫 Укажи токен в конфиге!</b>",
        "playing": "<b>🎧 Сейчас играет: </b><code>{}</code><b> - </b><code>{}</code>\n<b>🕐 {}</b>",
        "no_args": "<b>🚫 Укажи аргументы!</b>",
        "best_result": (
            "<b>🥇 Тип лучшего результата: </b><code>{}</code>"
            "\n"
            "{}"
            "\n"
            "<b>Исполнителей: </b><code>{}</code>"
            "\n"
            "<b>Треков: </b><code>{}</code>"
            "\n"
            "<b>Альбомов: </b><code>{}</code>"
            "\n"
            "<b>Плейлистов: </b><code>{}</code>"
            "\n"
            "<b>Видео: </b><code>{}</code>"
            "\n"
            "<b>Пользователей: </b><code>{}</code>"
            "\n"
            "<b>Подкастов: </b><code>{}</code>"
        ),
        "no_results": "<b>☹ Ничего не найдено :(</b>",
        "track": "Трек",
        "podcast": "Подкаст",
        "podcast_episode": "Эпизод подкаста",
        "user": "Пользователь",
        "video": "Видео",
        "album": "Aльбом",
        "playlist": "Плейлист",
        "artist": "Исполнитель",
        "autobioe": "<b>🔁 Autobio включен</b>",
        "autobiod": "<b>🔁 Autobio выключен</b>",
        "lyrics": "<b>📜 Текст песни: \n{}</b>",
        "_cls_doc": "Модуль для Яндекс.Музыка. Основан на SpotifyNow",
        "already_liked": "<b>🚫 Текущий трек уже лайкнут!</b>",
        "liked": "<b>❤ Лайкнул текущий трек!</b>",
        "not_liked": "<b>🚫 Текущий трек не лайкнут!</b>",
        "disliked": "<b>💔 Дизлайкнул текущий трек!</b>",
        "my_vibe": "<b>🌊 Ты слушаешь трек в Моей Волне, я не могу распознать его.</b>",
        "_cfg_yandexmusictoken": "Токен аккаунта Яндекс.Музыка",
        "_cfg_autobiotemplate": "Шаблон для AutoBio",
        "no_lyrics": "<b>🚫 У трека нет текста!</b>",
        "guide": (
            '<a href="https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781">'
            "Инструкция по получению токена Яндекс.Музыка</a>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "YandexMusicToken",
                None,
                lambda: self.strings["_cfg_yandexmusictoken"],
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "AutoBioTemplate",
                "🎧 {}",
                lambda: self.strings["_cfg_autobiotemplate"],
                validator=loader.validators.String(),
            ),
        )

    async def on_dlmod(self):
        if not self.get("guide_send", False):
            await self.inline.bot.send_message(
                self._tg_id,
                self.strings["guide"],
            )
            self.set("guide_send", True)

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.db = db

        self._premium = getattr(await self.client.get_me(), "premium", False)

        if self.get("autobio", False):
            self.autobio.start()

    @loader.command(
        ru_doc="Получить текущий трек",
    )
    async def ynowcmd(self, message: Message):
        """Get now playing track"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return
        try:
            queues = await client.queues_list()
            last_queue = await client.queue(queues[0].id)
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return
        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return

        info = await client.tracks_download_info(last_track.id, True)
        link = info[0].direct_link

        artists = ", ".join(last_track.artists_name())
        title = last_track.title
        if last_track.version:
            title += f" ({last_track.version})"
        else:
            pass

        caption = self.strings["playing"].format(
            utils.escape_html(artists),
            utils.escape_html(title),
            f"{last_track.duration_ms // 1000 // 60:02}:{last_track.duration_ms // 1000 % 60:02}",
        )
        try:
            lnk = last_track.id.split(":")[1]
        except:
            lnk = last_track.id
        else:
            pass

        await self.inline.form(
            message=message,
            text=caption,
            reply_markup={
                "text": "song.link",
                "url": f"https://song.link/ya/{lnk}",
            },
            silent=True,
            audio={
                "url": link,
                "title": utils.escape_html(title),
                "performer": utils.escape_html(artists),
            },
        )

    @loader.command(
        ru_doc="Получить текст текущей песни",
    )
    async def ylyrics(self, message: Message):
        """Get now playing track lyrics"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return

        queues = await client.queues_list()
        last_queue = await client.queue(queues[0].id)

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return

        try:
            lyrics = await client.tracks_lyrics(last_track.id)
            async with aiohttp.ClientSession() as session:
                async with session.get(lyrics.download_url) as request:
                    lyric = await request.text()

            text = self.strings["lyrics"].format(utils.escape_html(lyric))
        except:
            text = self.strings["no_lyrics"]

        await utils.answer(message, text)

    @loader.command(
        ru_doc="Поиск треков, артистов, альбомов, плейлистов, пользователей, подкастов, видео"
    )
    async def ysearchcmd(self, message: Message):
        """Search tracks, artists, albums, playlists, users, podcasts, videos"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        results = await client.search(args)

        if results.best:
            type_ = results.best.type
            best = results.best.result

        if not results.best:
            await utils.answer(message, self.strings["no_results"])
            return

        if type_ in ["track", "podcast_episode"]:
            artists = ""
            if best.artists:
                artists = ", ".join(artist.name for artist in best.artists)
            best_result_text = (
                f"<code>{artists}</code><b> - </b><code>{best.title}</code>"
            )
        elif type_ == "artist":
            best_result_text = f"<code>{best.name}</code>"
        elif type_ in ["album", "podcast", "playlist", "video"]:
            best_result_text = f"<code>{best.title}</code>"

        await utils.answer(
            message,
            self.strings["best_result"].format(
                self.strings[type_],
                best_result_text,
                results.artists.total if results.artists else 0,
                results.tracks.total if results.tracks else 0,
                results.albums.total if results.albums else 0,
                results.playlists.total if results.playlists else 0,
                results.users.total if results.users else 0,
                results.videos.total if results.videos else 0,
                results.podcasts.total if results.podcasts else 0,
            ),
        )

    @loader.command(
        ru_doc="Отображение текущей песни в описании аккаунта",
    )
    async def ybio(self, message: Message):
        """Show now playing track in your bio"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return

        current = self.get("autobio", False)
        new = not current
        self.set("autobio", new)

        if new:
            await utils.answer(message, self.strings["autobioe"])
            self.autobio.start()
        else:
            await utils.answer(message, self.strings["autobiod"])
            self.autobio.stop()

    async def ylikecmd(self, message: Message):
        """❤"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            queues = await client.queues_list()
            last_queue = await client.queue(queues[0].id)
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return

        liked_tracks = await client.users_likes_tracks()
        liked_tracks = await liked_tracks.fetch_tracks_async()

        if isinstance(liked_tracks, list):
            if last_track in liked_tracks:
                await utils.answer(message, self.strings["already_liked"])
                return
            else:
                await last_track.like_async()
                await utils.answer(message, self.strings["liked"])
        else:
            await last_track.like_async()
            await utils.answer(message, self.strings["liked"])

    async def ydislikecmd(self, message: Message):
        """💔"""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            logging.info("Указан неверный токен!")
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            queues = await client.queues_list()
            last_queue = await client.queue(queues[0].id)
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except:
            await utils.answer(message, self.strings["my_vibe"])
            return

        liked_tracks = await client.users_likes_tracks()
        liked_tracks = await liked_tracks.fetch_tracks_async()

        if isinstance(liked_tracks, list):
            if last_track in liked_tracks:
                await last_track.dislike_async()
                await utils.answer(message, self.strings["disliked"])

            else:
                await utils.answer(message, self.strings["not_liked"])
                return

        else:
            await utils.answer(message, self.strings["not_liked"])
            return

    @loader.loop(interval=60)
    async def autobio(self):
        client = ClientAsync(self.config["YandexMusicToken"])

        await client.init()
        queues = await client.queues_list()
        last_queue = await client.queue(queues[0].id)

        try:
            last_track_id = last_queue.get_current_track()
            last_track = await last_track_id.fetch_track_async()
        except:
            return

        artists = ", ".join(last_track.artists_name())
        title = last_track.title

        text = self.config["AutoBioTemplate"].format(
            f"{artists} - {title}"
            + (f" ({last_track.version})" if last_track.version else "")
        )

        try:
            await self.client(
                UpdateProfileRequest(about=text[: 140 if self._premium else 70])
            )
        except FloodWaitError as e:
            logger.info(f"Sleeping {e.seconds}")
            await sleep(e.seconds)
            return

    @loader.command(
        ru_doc="Экспорт списка треков из плейлиста 'Мне нравится'",
    )
    async def yaexportcmd(self, message: Message):
        """Export list of tracks from 'Liked' playlist"""
        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return
        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return
        tracks: list[TracksList] = (await client.users_likes_tracks())[::-1]
        export_list = []
        for short_track in tracks:
            try:
                full_track: Track = await short_track.fetch_track_async()
                if not full_track.available:
                    continue
                if not full_track.artists:
                    continue
                if not full_track.title:
                    continue
                name = f"{full_track.artists[0].name} - {full_track.title}"
                export_list.append(name)
            except Exception as e:
                pass
        # Write the list to a file
        with open("export.txt", "w") as f:
            for track in export_list:
                f.write("%s\n" % track)
        # Send the file in the chat
        await self.client.send_file(
            message.chat_id,
            "export.txt",
            caption="Here's your exported list of tracks from the 'Liked' playlist.",
        )
        # Remove the file after sending
        os.remove("export.txt")
