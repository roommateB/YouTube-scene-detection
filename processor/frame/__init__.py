from typing import List, Dict, Tuple
from enum import Enum
from dataclasses import dataclass


DEFAULT_PERCENTAGE = 0.74


class FrameType(Enum):
    # Home Page
    HOME = "home"

    # Shorts
    SHORTS = "shorts"

    # Video
    VIDEO = "video"


@dataclass
class BasicInfo:
    picture_number: int
    user: str
    path: str
    qid: str
    frame_size: Tuple[float, float]


class Frame:
    last_code_id = -1
    
    def __init__(
        self, frame_type: FrameType, basic_info: BasicInfo, contexts: "list[str]",
    ):
        self.frame_type: FrameType = frame_type

        # schema
        self.basic_info = basic_info
        
        self.contexts: "list[str]" = contexts
        self.borders: str = ""
        self.percentages: "list[float]" = [DEFAULT_PERCENTAGE]
        self.biggests: "list[bool]" = [True]
        self.code_ids: "list[int]" = []

        # common
        self.is_news: bool = False
        self.is_comment: bool = False

        # video
        self._is_action: bool = False

        # home
        self._is_announcement: bool = False
        self._is_search: bool = False
        self._post_existed: bool = False
        # self._shorts_existed: bool = False

    def __str__(self) -> str:
        return str(self.get_attributes())

    @property
    def is_video(self):
        return True if self.frame_type == FrameType.VIDEO else False

    @property
    def is_shorts(self):
        return True if self.frame_type == FrameType.SHORTS else False

    @property
    def is_action(self):
        return self._is_action

    @is_action.setter
    def is_action(self, val: bool):
        self._is_action = val and self.frame_type == FrameType.VIDEO

    @property
    def is_announcement(self):
        return self._is_announcement

    @is_announcement.setter
    def is_announcement(self, val: bool):
        self._is_announcement = val and self.frame_type == FrameType.HOME

    @classmethod
    def get_new_code_id(cls):
        cls.last_code_id += 1
        return cls.last_code_id

    @property
    def is_search(self):
        return self._is_search

    @is_search.setter
    def is_search(self, val: bool):
        self._is_search = val and self.frame_type == FrameType.HOME

    # @property
    # def shorts_existed(self):
    #     return self._shorts_existed

    # @shorts_existed.setter
    # def shorts_existed(self, val: bool):
    #     self._shorts_existed = val and self.frame_type == FrameType.HOME

    @property
    def post_existed(self):
        return self._post_existed

    @post_existed.setter
    def post_existed(self, val: bool):
        self._post_existed = val and self.frame_type == FrameType.HOME

    def get_attributes(self) -> Dict:
        return self.__dict__.items()
