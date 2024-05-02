# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class JobItem:
    role: str
    company: str
    location: str
    skills: list
    expand: str
