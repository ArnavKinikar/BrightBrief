from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Optional


class JobStatus(str, Enum):
    STARTED = "started"
    INGESTING = "ingesting"
    SUMMARIZING = "summarizing"
    SCRIPTING = "scripting"
    GENERATING_AUDIO = "generating_audio"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class JobRun:
    """
    Represents a single execution of the daily BrightBrief pipeline.
    Used for tracking progress, failures, and retries.
    """

    run_id: str
    episode_date: date
    status: JobStatus

    started_at: datetime
    finished_at: Optional[datetime]

    error_message: Optional[str]
