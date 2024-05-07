# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class JobItem:
    """Item produced from scrapy pipelines with processed data"""

    role: str = None
    company: str = None
    location: str = None
    skills: list = None
    describ: list = None
