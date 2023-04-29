from .base import BaseRecognizer


class HomeRecognizer(BaseRecognizer):
    def __init__(self, predicted_objects, ocr_document, frame_size):
        BaseRecognizer.__init__(self, predicted_objects, ocr_document, frame_size)

    def get_confidence(self):
        features_checker = [(self._check_label_exist, "home")]
        matched_num = sum([func(*args) if args else func() for func, *args in features_checker])
        return matched_num / len(features_checker)

    def check_is_search(self) -> bool:
        return self._check_3_dots_position() and self._check_label_exist("return")

    def check_is_announcement(self) -> bool:
        return (
            self.check_is_search()
            and len(
                [label for label, _, _ in self.predicted_objects if label == "3 dots"]
            )
            >= 7
        )

    def check_is_comment(self) -> bool:
        return self._match_keyword("貼文")

    def check_post_existed(self) -> bool:
        return self._check_label_exist("comment")

    # def check_shorts_existed(self) -> bool:
    #     return self._match_keyword("Shorts")

    # Features
    def _check_3_dots_position(self) -> bool:
        for label, confidence, box in self.predicted_objects:
            if label == "3 dots":
                _3_dots_norm_pos = float(box[1] / self.frame_height)
                if _3_dots_norm_pos < 0.1:
                    return True
        return False
