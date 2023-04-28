from .base import BaseRecognizer


class VideoRecognizer(BaseRecognizer):
    def __init__(self, predicted_objects, ocr_document, frame_size):
        BaseRecognizer.__init__(self, predicted_objects, ocr_document, frame_size)

    def get_confidence(self):
        features_checker = [
            (self._check_height_width_ratio,),
            (self._check_label_exist, "next vedio"),
            (self._match_keyword, "回覆"),
            (self._match_keyword, "聊天"),
            (self._check_sorting_position,),
        ]
        matched_num = sum([func(*args) if args else func() for func, *args in features_checker])
        return matched_num / len(features_checker)

    def check_is_comment(self) -> bool:
        return self._check_sorting_position() and (self._match_keyword("留言") or self._match_keyword("聊天"))

    def check_is_action(self) -> bool:
        return self._check_label_exist("next vedio")

    # Features
    def _check_height_width_ratio(self) -> bool:
        return True if self.frame_height < self.frame_width else False

    def _check_sorting_position(self) -> bool:
        for label, confidence, box in self.predicted_objects:
            if label == "sorting":
                sorting_norm_pos = box[0] / self.frame_width
                if sorting_norm_pos < 0.85 and sorting_norm_pos > 0.75:
                    return True
        return False
