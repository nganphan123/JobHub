import scrapy
import urllib.parse as urlparse
from urllib.parse import urlencode

import scrapy.responsetypes


class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    baseUrl = "https://www.linkedin.com/jobs/search"

    def __init__(self, jobTitle, location):
        self.jobTitle = jobTitle
        self.location = location

    def prepareUrl(self) -> str:
        # params from user input
        params = {"keywords": self.jobTitle, "location": self.location}
        # encode params to url format
        query = urlencode(params)
        # parse url
        urlParts = urlparse.urlparse(self.baseUrl)
        # construct final url
        return urlParts._replace(query=query).geturl()

    def start_requests(self):
        url = self.prepareUrl()
        self.logger.info("Visited %s", url)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for job in response.css("div.base-card"):
            nextPage = job.css("a.base-card__full-link::attr(href)").get()
            if nextPage:
                yield scrapy.Request(url=nextPage, callback=self.parseJobDescrib)
            else:
                yield ({'error': 'no job description found'})

    def parseJobDescrib(self, response):
        self.logger.info("Visited next page %s", response.url)

        def extract_part(htmlQuery):
            return response.css(htmlQuery).get(default="").strip()
        item = ({
            "role": extract_part("div.top-card-layout__entity-info h1.top-card-layout__title::text"),
            "company": extract_part("a.topcard__org-name-link::text"),
            "location": extract_part("h4.top-card-layout__second-subline div.topcard__flavor-row span.topcard__flavor.topcard__flavor--bullet::text"),
            # "describ": extract_part("div.show-more-less-html__markup.relative.overflow-hidden")
        })
        yield item
