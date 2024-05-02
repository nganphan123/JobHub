from scrapy.crawler import CrawlerProcess
from spiders import LinkedInSpider
from scrapy.signalmanager import dispatcher
from scrapy import signals


def main():
    results = []  # scraped items

    def store_crawler_item(item):
        results.append(item)
    # store new scraped item to results
    dispatcher.connect(store_crawler_item, signal=signals.item_passed)
    process = CrawlerProcess()
    process.crawl(LinkedInSpider, "software engineer", "kelowna")
    process.start()
    print("results are ", results)


if __name__ == "__main__":
    main()
