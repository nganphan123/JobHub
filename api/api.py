from flask import Flask, request
from spider.spider.crawl import crawl_job

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
    results = crawl_job(
        job=jobTitle, location=location, skills=skills, platforms=platforms, page=page
    )

    return {"data": results}
