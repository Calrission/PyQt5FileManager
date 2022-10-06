from enum import Enum


class TypeFile(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    OTHER = "other"


types = {
    TypeFile.TEXT: ["txt"],
    TypeFile.VIDEO: ["mp3"],
    TypeFile.IMAGE: ["png", "jpeg", "jpg"]
}