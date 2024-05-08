from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import args
from spiders.items import SpiderRequest

"""Example to test spiders"""

exampleRequest = SpiderRequest(
    role="software engineer",
    location="canada",
    skills=["aws", "python", "java", "c++"],
    page=0,
)


def main():
    options = args.get_arg_parser().parse_args()
    results = []  # scraped items

    def store_crawler_item(item):
        results.append(item)

    # store new scraped item to results
    dispatcher.connect(store_crawler_item, signal=signals.item_scraped)
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    process.crawl(
        args.get_provider_handler(args.get_provider(options.provider)), exampleRequest
    )
    process.start()
    print("results are ", results)


if __name__ == "__main__":
    main()
