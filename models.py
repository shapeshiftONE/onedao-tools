# Document data structure
import string
import datetime
from dataclasses import dataclass, field
from bs4.element import Tag

@dataclass
class Document:
    title: str = None
    description: str = None
    originalDatetime: datetime.datetime = None
    currentDatetime: datetime.datetime = None
    author: str = None
    tags: list = field(default_factory=list)
    published: bool = True
    editor: str = 'markdown'
    htmlContent: Tag = None
    markDownContent: str = None
    originalURL: str = None
    slug: str = None
    
    @property
    def joinedTags(self) -> str:
        return ', '.join(self.tags)

    @property
    def originalDate(self) -> str:
        return self.originalDatetime.strftime('%Y-%m-%d')

    @property
    def originalDateShort(self) -> str:
        return self.originalDatetime.strftime('%B %Y')

    @property
    def currentISODatetime(self) -> str:
        # Force UTC by adding "Z", easier than setting the TZ in the datetime object.
        return self.currentDatetime.isoformat(timespec='milliseconds') + 'Z'

    @property
    def wordCount(self) -> int:
        # Tag words + Title + Content
        text = " ".join(self.tags) + self.title + " " + self.description + " " + self.htmlContent.get_text()
        text_noPunc = text.translate(str.maketrans("","", string.punctuation))
        words = text_noPunc.split()
        return len(words) + len(self.tags)