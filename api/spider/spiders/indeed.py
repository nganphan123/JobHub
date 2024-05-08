import scrapy
import urllib.parse as urlparse
import re
import json
from .items import PreItem, SpiderRequest


class IndeedSpider(scrapy.Spider):
    name = "Indeed"
    base_url = "https://www.indeed.com"
    per_page = 15  # FIXME: There might be more than 15 listings
    job_list_tag_regex = (
        r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});'
    )
    default_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

    def __init__(self, request: SpiderRequest):
        self.jobTitle = request.role
        self.location = request.location
        self.skills = set(request.skills)
        self.page = request.page

    def extract_part(self, response, htlm_query, default=""):
        return response.css(htlm_query).get(default=default).strip()

    def extract_parts(self, response, htlm_query):
        return response.css(htlm_query).getall()

    def prepareUrl(self, pageIdx) -> str:
        params = {
            "q": self.jobTitle,
            "l": self.location,
            "start": pageIdx * self.per_page,
        }
        # encode params
        query = urlparse.urlencode(params)
        # construct final url
        return urlparse.urlparse(f"{self.base_url}/jobs")._replace(query=query).geturl()

    def start_requests(self):
        url = self.prepareUrl(self.page)
        yield scrapy.Request(url=url, headers=self.default_headers, callback=self.parse)

    def parse(self, response):
        # Indeed stores, in hidden script tag, the data
        # to render the job list
        jobs_json_data = re.findall(self.job_list_tag_regex, response.text)

        if len(jobs_json_data) > 0:
            job_data = json.loads(jobs_json_data[0])
            # Extract only necessary data
            job_list = job_data["metaData"]["mosaicProviderJobCardsModel"]["results"]

            if job_list is not None and len(job_list) > 0:
                for job in job_list:
                    url = f"{self.base_url}{job["viewJobLink"]}"
                    yield scrapy.Request(
                        url=url,
                        headers=self.default_headers,
                        callback=self.parse_job_description,
                    )
            else:
                yield ({"error": "job list is empty"})
        else:
            yield ({"error": "failed to find list of jobs"})

    def parse_job_description(self, response):
        bullets = self.extract_parts(
            response, "div.jobsearch-jobDescriptionText li::text"
        )

        item = PreItem(
            role=self.extract_part(
                response, '[data-testid="jobsearch-JobInfoHeader-title"] span::text'
            ),
            location=self.extract_part(
                response, '[data-testid="inlineHeader-companyLocation"] div::text'
            ),
            company=self.extract_part(
                response, '[data-testid="inlineHeader-companyName"] a::text'
            ),
            describ=bullets,
        )

        yield item
