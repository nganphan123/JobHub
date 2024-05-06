import scrapy
import urllib.parse as urlparse
import re
import json


class IndeedSpider(scrapy.Spider):
    name = "Indeed"
    base_url = "https://www.indeed.com"
    per_page = 15  # FIXME: There might be more than 15 listings
    job_list_tag_regex = (
        r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});'
    )
    job_detail_tag_regex = r"_initialData=(\{.+?\});"
    default_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }
    empty_result = {
        "role": "",
        "company": "",
        "location": "",
        "describ": "",
    }

    def __init__(self, jobTitle, location, skills, page):
        self.jobTitle = jobTitle
        self.location = location
        self.skills = skills
        self.page = page

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
        # Again, Indeed does store job details in a hidden script
        job_json_data = re.findall(self.job_detail_tag_regex, response.text)

        def remove_tag(raw_description: str):
            return re.sub("<.+?>", "", raw_description)

        if len(job_json_data) > 0:
            job_data = json.loads(job_json_data[0])
            job = job_data["jobInfoWrapperModel"]["jobInfoModel"]

            if job is not None:
                job_header = job["jobInfoHeaderModel"]
                yield {
                    "role": job_header["jobTitle"],
                    "company": job_header["companyName"],
                    "location": job_header["formattedLocation"],
                    "describ": remove_tag(job["sanitizedJobDescription"]),
                }

        yield self.empty_result
