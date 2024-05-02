# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from items import JobItem


class SpiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        jobItem = JobItem(skills=[])
        matchedList = dict()
        # find description containing skills
        # ISSUE: match all with "c" skill
        for skill in spider.skills:
            for i, desc in enumerate(adapter.get("describ")):
                if skill in desc.lower():
                    jobItem.skills.append(skill)
                    matchedList[i] = desc
                    break
        # if the job matches at least one skill, return. Else, drop item
        if matchedList:
            jobItem.company = adapter.get("company")
            jobItem.role = adapter.get("role")
            jobItem.location = adapter.get("location")
            jobItem.describ = matchedList.values()
            return jobItem
        else:
            raise DropItem(f"No skills matched in {item}")
