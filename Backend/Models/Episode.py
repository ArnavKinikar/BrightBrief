from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional


class EpisodeStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class StorySummary:
    """
    Represents a single news story covered in an episode.
    """
    headline: str
    summary: str
    source_url: str


@dataclass
class Episode:
    """
    Represents a single BrightBrief daily episode.
    This is a pure domain model (no DB or API logic).
    """

    episode_date: date
    title: str
    stories: List[StorySummary]
    audio_url: Optional[str]
    status: EpisodeStatus
