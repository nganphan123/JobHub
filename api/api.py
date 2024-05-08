from flask import Flask
from flask import request
from spider.args import get_provider, get_provider_handler
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from spider.spiders import SpiderRequest

app = Flask(__name__)

defaultPlatform = "linkedin"


@app.route("/api/job")
def get_job():
    jobTitle = request.args.get("job")
    location = request.args.get("location")
    skills = request.args.get("skills")
    platforms = request.args.get("platform", default=[defaultPlatform])
    page = request.args.get("page", 0)
    if platforms:
        platforms = platforms.split(",")
    if skills:
        skills = skills.split(",")

    results = []  # scraped items

    def store_crawler_item(item):
        results.append(item)

    # store new scraped item to results
    dispatcher.connect(store_crawler_item, signal=signals.item_scraped)
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    for platform in platforms:
        spider = get_provider_handler(get_provider(platform))
        request = SpiderRequest(
            role=jobTitle, location=location, skills=skills, page=page
        )
        process.crawl(spider, request)
    process.start()
