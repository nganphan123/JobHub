# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from .linkedin import LinkedInSpider
from .indeed import IndeedSpider
from .items import PreItem, SpiderRequest
