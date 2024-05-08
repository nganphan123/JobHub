from dataclasses import dataclass


@dataclass
class PreItem:
    """Item containing raw data fetched from pages"""

    role: str = None
    company: str = None
    location: str = None
    describ: list = None


@dataclass
class SpiderRequest:
    """Common request object for spiders to process"""

    page: int
    role: str = None
    location: str = None
    skills: list = None
