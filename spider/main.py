from scrapy.crawler import CrawlerProcess
from spiders import IndeedSpider, LinkedInSpider
from scrapy.signalmanager import dispatcher
from scrapy import signals
import settings as customSettings
import args


def get_provider_handler(provider):
    mapper = {
        args.Provider.INDEED: IndeedSpider,
        args.Provider.LINKEDIN: LinkedInSpider,
    }
    return mapper[provider]


def main():
    options = args.get_arg_parser().parse_args()
    results = []  # scraped items

    def store_crawler_item(item):
        results.append(item)

    # store new scraped item to results
    dispatcher.connect(store_crawler_item, signal=signals.item_scraped)
    settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": customSettings.REQUEST_FINGERPRINTER_IMPLEMENTATION,
        "TWISTED_REACTOR": customSettings.TWISTED_REACTOR,
        "FEED_EXPORT_ENCODING": customSettings.FEED_EXPORT_ENCODING,
        "ITEM_PIPELINES": customSettings.ITEM_PIPELINES,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(
        get_provider_handler(
            args.get_provider(options.provider, args.Provider.LINKEDIN)
        ),
        "software engineer",
        "canada",
        "aws,python,java,c++",
        0,
    )
    process.start()
    print("results are ", results)


if __name__ == "__main__":
    main()
