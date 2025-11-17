from dataclasses import dataclass, field
from typing import List


@dataclass
class Site:
     url: str

@dataclass
class Track:
    title: str
    duration: str = None


@dataclass
class Album:
     id: int
     title: str
     url: str
     record_labels: List[str] = field(default_factory=list)
     track_count: int = 0
     tracks: List[Track] = field(default_factory=list)
     styles: List[str] = field(default_factory=list)
     genres: List[str] = field(default_factory=list)
     year: int = None

@dataclass
class Member:
     id: int
     name: str
     url: str

@dataclass
class Artist:
     id: int
     name: str
     url: str
     sites: List[Site] = field(default_factory=list)
     albums: List[Album] = field(default_factory=list)
     members: List[Member] = field(default_factory=list)

