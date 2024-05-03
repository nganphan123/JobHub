import scrapy
import urllib.parse as urlparse
from urllib.parse import urlencode

import scrapy.responsetypes


class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    baseUrl = "https://www.linkedin.com/jobs/api/seeMoreJobPostings/search"

    def __init__(self, jobTitle, location, skills, page):
        self.jobTitle = jobTitle
        self.location = location
        self.skills = set(skills.split(","))
        self.page = page

    def prepareUrl(self, pageIdx) -> str:
        # params from user input
        # linkedin groups jobs in batch of 25
        params = {"keywords": self.jobTitle,
                  "location": self.location, "start": pageIdx*25}
        # encode params to url format
        query = urlencode(params)
        # parse url
        urlParts = urlparse.urlparse(self.baseUrl)
        # construct final url
        return urlParts._replace(query=query).geturl()

    def start_requests(self):
        firstBatch = self.prepareUrl(self.page*2)
        secondBatch = self.prepareUrl(self.page*2+1)
        self.logger.info("Visited %s", firstBatch)
        yield scrapy.Request(url=firstBatch, callback=self.parse)
        self.logger.info("Visited %s", secondBatch)
        yield scrapy.Request(url=secondBatch, callback=self.parse)

    def parse(self, response):
        for job in response.css("div.base-card"):
            nextPage = job.css("a.base-card__full-link::attr(href)").get()
            if nextPage:
                # remove query from url
                nextPage = urlparse.urljoin(
                    nextPage, urlparse.urlparse(nextPage).path)
                yield scrapy.Request(url=nextPage, callback=self.parseJobDescrib)
            else:
                yield ({'error': 'no job description found'})

    def parseJobDescrib(self, response):
        self.logger.info("Visited next page %s", response.url)

        def extract_part(htmlQuery):
            return response.css(htmlQuery).get(default="").strip()

        # extract listing items
        bullets = response.css(
            "section.show-more-less-html div.show-more-less-html__markup li::text").getall()
        yield ({
            'role': extract_part("div.top-card-layout__entity-info h1.top-card-layout__title::text"),
            'company': extract_part("a.topcard__org-name-link::text"),
            'location': extract_part("h4.top-card-layout__second-subline div.topcard__flavor-row span.topcard__flavor.topcard__flavor--bullet::text"),
            'describ': bullets
        })
