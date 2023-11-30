from typing import Optional

from chat_downloader.sites.common import Chat as BaseChat
from chat_downloader.sites import YouTubeChatDownloader
from chat_downloader.formatting.format import ItemFormatter

from .utils import replace_emoji_in_string


__all__ = ['Chat', 'YTChat']


class Chat(BaseChat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatter = ItemFormatter()

    def format(self, item):
        return self.formatter.format(item, format_name='youtube')


class YTChat(YouTubeChatDownloader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.default_params = dict(
            max_attempts=15,
            message_groups=['messages'],
            buffer_size=4096,
            message_receive_timeout=0.1
        )

    def get_chat_by_video_id(self,
                             video_id,
                             params: Optional[dict] = None) -> str:
        """Get chat messages for a YouTube video, given its ID.

        :param video_id: YouTube video ID
        :type video_id: str
        :return: Chat object for the corresponding YouTube video
        :rtype: Chat
        """

        if params is None:
            params = self.default_params

        initial_info, ytcfg = self._get_initial_video_info(video_id, params)

        chat_object = Chat(
            self._get_chat_messages(initial_info, ytcfg, params),
            id=video_id,
            **initial_info
        )

        text_out = []
        for mess in chat_object:
            text = chat_object.format(mess)
            text = replace_emoji_in_string(text)
            text_out.append(text)

        text_out = "\n".join([txt for txt in text_out])
        return text_out
