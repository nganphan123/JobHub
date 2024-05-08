from .spiders import SpiderRequest
from .args import get_provider, get_provider_handler
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings


def crawl_job(job: str, location: str, skills: list, platforms: list, page: int):
    results = []  # scraped items

    def store_crawler_item(item):
        results.append(item)

    # store new scraped item to results
    dispatcher.connect(store_crawler_item, signal=signals.item_scraped)
    process = CrawlerProcess(settings=get_project_settings())
    for platform in platforms:
        spider = get_provider_handler(get_provider(platform))
        spiderRequest = SpiderRequest(
            role=job, location=location, skills=skills, page=page
        )
        process.crawl(spider, spiderRequest)
    process.start()
    return results
