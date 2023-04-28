from .base import BaseRecognizer


class ShortsRecognizer(BaseRecognizer):
    def __init__(self, predicted_objects, ocr_document, frame_size):
        BaseRecognizer.__init__(self, predicted_objects, ocr_document, frame_size)

    def get_confidence(self):
        features_checker = [
            (self._sorting_position, ),
            (self._check_label_exist, "camera"),
            (self._check_label_exist, "return"),
        ]
        matched_num = sum([func(*args) if args else func() for func, *args in features_checker])
        return matched_num / len(features_checker)

    def check_is_comment(self) -> bool:
        return self._match_keyword("留言")

    # Features
    def _sorting_position(self) -> bool:
        for label, confidence, box in self.predicted_objects:
            if label == "sorting":
                sorting_norm_pos = box[0] / self.frame_width
                if sorting_norm_pos < 0.95 and sorting_norm_pos > 0.85:
                    return True
        return False
