from typing import List, Tuple
from numpy import argmax
from google.cloud.vision import TextAnnotation
from processor.frame import Frame, FrameType, BasicInfo
from processor.frame.features import *
from processor.text_processor.text_detection import *

FRAME_TOP_BOUNDARY = 0.13
FRAME_BOTTOM_BOUNDARY = 0.87
VIDEO_PRIORITY_WEIGHTS = 2
SHORTS_PRIORITY_WEIGHTS = 2


class FrameRecognizer:
    def get_frame(
        self,
        basic_info: BasicInfo,
        predicted_objects: List,
        ocr_document: TextAnnotation,
    ) -> Frame:
        video_recognizer = VideoRecognizer(predicted_objects, ocr_document, basic_info.frame_size)
        shorts_recognizer = ShortsRecognizer(predicted_objects, ocr_document, basic_info.frame_size)
        home_recognizer = HomeRecognizer(predicted_objects, ocr_document, basic_info.frame_size)

        confidence_scores: dict[FrameType, int] = {}
        confidence_scores[FrameType.VIDEO] = VIDEO_PRIORITY_WEIGHTS * video_recognizer.get_confidence()
        confidence_scores[FrameType.SHORTS] = SHORTS_PRIORITY_WEIGHTS * shorts_recognizer.get_confidence()
        confidence_scores[FrameType.HOME] = home_recognizer.get_confidence()

        frame_type = max(confidence_scores, key=confidence_scores.get)
        frame = Frame(frame_type, basic_info, [get_post_context(ocr_document)])

        if frame_type == FrameType.VIDEO:
            if video_recognizer.check_is_comment():
                frame.is_comment = True
            if video_recognizer.check_is_action():
                frame.is_action = True

        elif frame_type == FrameType.SHORTS:
            if shorts_recognizer.check_is_comment():
                frame.is_comment = True

        elif frame_type == FrameType.HOME:
            if home_recognizer.check_is_comment():
                frame.is_comment = True
            if home_recognizer.check_post_existed():
                frame.post_existed = True
            if home_recognizer.check_is_announcement():
                frame.is_announcement = True
            if home_recognizer.check_is_search():
                frame.is_search = True
            
            frame_height = basic_info.frame_size[0]
            borders = self._split_frame(
                predicted_objects, ocr_document, frame, frame_height
            )
            borders = [frame_height*FRAME_TOP_BOUNDARY] + borders + [frame_height*FRAME_BOTTOM_BOUNDARY]
            frame.percentages = self._get_percentages_by_borders(borders, frame_height)
            frame.biggests = self._get_biggests_by_percentages(frame.percentages)
            borders_str = (
                ""
                if len(borders[1:-1]) == 0
                else "_".join([str(round(val)) for val in borders[1:-1]])
            )
            frame.borders = borders_str
            # Drop the areas before top boundary and after bottom boundary
            frame.contexts = get_posts_word_by_border(ocr_document, borders)[1:-1]

        return frame

    def _split_frame(
        self,
        predicted_objects: List,
        ocr_document: vision.TextAnnotation,
        frame: Frame,
        frame_height: float,
    ) -> List:

        objects = []
        for label, confidence, box in predicted_objects:
            if label == "3 dots" or label == "comment":
                y = box[1]
                h = box[3]
                object_position = y - h / 2
                objects.append((label, object_position))

        objects.extend(self._get_ocr_labels(ocr_document))
        objects = sorted(objects, key=lambda x: x[1])

        # Special case
        if frame.is_search or frame.is_announcement:
            for object in objects:
                if object[0] == "3 dots":
                    objects.remove(object)
                    break
                
        elif frame.post_existed:
            pre = ("", 0)
            for object in objects:
                if object[0] == "comment" and pre[0] == "3 dots":
                    objects.remove(pre)
                    break
                pre = object
                
        # General case
        borders = []
        for object in objects:
            label = object[0]
            if label == "3 dots":
                border = object[1] + frame_height / 8.5
            elif label == "comment":
                border = object[1] + frame_height * 0.05
            elif label == "shorts":
                border = object[1] + frame_height * 0.35

            if self._check_new_border_legal(frame, borders, border, frame_height):
                borders.append(border)
        
        return borders

    def _get_ocr_labels(self, ocr_document: vision.TextAnnotation) -> List:
        res = []
        for word in get_words_from_document(ocr_document):
            if get_text_of_word(word) == "Shorts":
                y_val = mean_of_bounding_box(word.bounding_box)
                res.append(("shorts", y_val))
        return res

    def _check_new_border_legal(
        self, frame: Frame, borders: List, new_coming: float, frame_height: float
    ) -> bool:
            
        if len(borders) == 0 and (
            new_coming >= frame_height * FRAME_TOP_BOUNDARY
            and new_coming <= frame_height * FRAME_BOTTOM_BOUNDARY
        ):
            return True
        
        if (
            new_coming < frame_height * FRAME_TOP_BOUNDARY
            or new_coming > frame_height * FRAME_BOTTOM_BOUNDARY
        ):
            return False
        
        if new_coming < borders[-1]:
            return False
        
        if (not frame.is_announcement) and (not frame.is_search):
            if (new_coming - borders[-1]) < frame_height / 5.5:
                return False
        
        return True

    def _get_percentages_by_borders(self, borders: "list[float]", frame_height: float) -> "list[float]":
        return [(borders[idx] - borders[idx-1]) / frame_height for idx in range(1, len(borders))]

    def _get_biggests_by_percentages(self, percentages: "list[float]"):
        max_idx = argmax(percentages)
        return [True if idx == max_idx else False for idx, _ in enumerate(percentages)]