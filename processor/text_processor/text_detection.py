from multiprocessing import context
from tabnanny import check
from google.cloud import vision
# import dotenv
import errno
import os
import re
from statistics import mean
from bisect import bisect
from typing import Iterator
import cv2
#from . import typed_generators as tg


class EnvironmentVariableNotFoundError(Exception):
    """Exception raised when the environment variable needed is not set.

    Attributes:
        environ -- the needed environment variable
    """

    def __init__(self, environ: str):
        self.environ = environ
        super().__init__(
            f'Environment variable "{self.environ}" is not set.\nTry to setup an `.env` file.'
        )


def setup_credential():
    """Load credentail into environment variable and check whether the credentail file exists.

    Raises:
        text_detection.exceptions.EnvironmentVariableNotFoundError:
            If neither the environment variable nor .env file contains `GOOGLE_APPLICATION_CREDENTIALS`.

        FileNotFoundError: If the credential file specified in `GOOGLE_APPLICATION_CREDENTIALS` does not exist.
    """

    #dotenv.load_dotenv()
    
    # if (cred := os.getenv("GOOGLE_APPLICATION_CREDENTIALS")) is None:
    #     raise EnvironmentVariableNotFoundError("GOOGLE_APPLICATION_CREDENTIALS")
    # elif not os.path.exists(cred):
    #     raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cred)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"processor/text_processor/news-consumption-dce74dd88d4f.json"

    print("Environment Variable Set Successfully")


def filename_to_image(filename: str):
    """Return a vision.Image instance according to filename."""

    with open(filename, mode="rb") as image_file:
        content = image_file.read()

    return vision.Image(content=content)    
    
    
def annotate_image(imageFile: str) -> vision.AnnotateImageResponse:
    """Make an API call to Google OCR API with the image file.
    
    Args:
        imageFile: The filename of the image to be detected.

    Returns:
        google.cloud.vision.AnnotateImageResponse: Response to Google OCR API request.
    """

    client = vision.ImageAnnotatorClient()

    image = filename_to_image(imageFile)
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    request = vision.AnnotateImageRequest(image=image, features=[feature])

    return client.annotate_image(request)


def get_text_of_word(word: vision.Word) -> str:
    """Return the text in a vision.Word instance."""

    return "".join(symbol.text for symbol in word.symbols)


def mean_of_bounding_box(boundingBox: vision.BoundingPoly) -> int:
    """Return the mean of y-coordinates of a bounding box rounded to nearest integer."""

    yCoords = [vertex.y for vertex in boundingBox.vertices]
    return round(mean(yCoords))


def to_regex_string_list(strList: "list[str]") -> "list[str]":
    """Escape all regex metacharacters of strings in list."""

    return [re.escape(string) for string in strList]


def pages(document: vision.TextAnnotation, /) -> Iterator[vision.Page]:
    yield from document.pages


def blocks(page: vision.Page, /) -> Iterator[vision.Block]:
    yield from page.blocks


def paragraphs(block: vision.Block, /) -> Iterator[vision.Paragraph]:
    yield from block.paragraphs


def words(paragraph: vision.Paragraph, /) -> Iterator[vision.Word]:
    yield from paragraph.words


def symbols(word: vision.Word, /) -> Iterator[vision.Symbol]:
    yield from word.symbols


def get_words_from_document(
    document: vision.TextAnnotation, /
) -> Iterator[vision.Word]:
    for page in pages(document):
        for block in blocks(page):
            for paragraph in paragraphs(block):
                yield from words(paragraph)


def get_post_context(document):
    context = ''
    for word in get_words_from_document(document):
        context += get_text_of_word(word)
    
    return context


def get_posts_word_by_border(
    document: vision.TextAnnotation, bordersInPixel: "list[int]"
) -> "list[list[str]]":
    """Split the text in document with the given borders.

    Args:
        document: The attribute full_text_annotation from the return value of text_detection.detect_image().
            example: `document = text_detection.detect_image('my_image.png').full_text_annotation`

        bordersInPixel: The position of each border in pixel.

    Returns:
        list[str]: The text of each post.
            Normally, the length of the list should be len(bordersInPixel) + 1.
    """


    sortedBorders = sorted(bordersInPixel)  # make sure that borders are fit to bisect()
    result: "list[list[str]]" = [[] for _ in range(len(bordersInPixel) + 1)]
    
    for word in get_words_from_document(document):
        #print(get_text_of_word(word))
        index = bisect(sortedBorders, mean_of_bounding_box(word.bounding_box))
        result[index].append(get_text_of_word(word))

    for idx, sub_result in enumerate(result):
        result[idx] = ' '.join(sub_result)

    return result
    
    
def convert_words_to_context(words):
    context = ''
    for i in range(len(words)):
        context += words[i]
    
    return context
