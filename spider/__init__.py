from scrapy.crawler import CrawlerProcess
from spiders import LinkedInSpider
from scrapy.signalmanager import dispatcher
from scrapy import signals
import settings as customSettings


def main():
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
    process.crawl(LinkedInSpider, "software engineer",
                  "canada", "aws,python,java,c++")
    process.start()
    print("results are ", results)


if __name__ == "__main__":
    main()
