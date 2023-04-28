from google.cloud.vision import TextAnnotation
from typing import List, Tuple
from processor.text_processor.text_detection import (
    get_text_of_word,
    get_words_from_document,
)


class BaseRecognizer:
    def __init__(
        self,
        predicted_objects: List,
        ocr_document: TextAnnotation,
        frame_size: Tuple[float, float]
    ):
        self.predicted_objects = predicted_objects
        self.ocr_document = ocr_document
        self.frame_height = frame_size[0]
        self.frame_width = frame_size[1]

    def _check_label_exist(self, label: str):
        labels = [label for label, confidence, box in self.predicted_objects]
        return True if label in labels else False

    def _match_keyword(self, keyword: str):
        words = [
            get_text_of_word(word)
            for word in get_words_from_document(self.ocr_document)
        ]
        print(words)
        return True if keyword in words else False
