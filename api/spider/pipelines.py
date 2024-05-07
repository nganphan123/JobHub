# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from items import JobItem
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import asyncio
from spiders import PreItem


class SpiderPipeline:
    async def process_item(self, item: PreItem, spider):
        def skill_extractor_items(jobDesc):
            # skillNer
            # init params of skill extractor
            nlp = spacy.load("en_core_web_lg")
            # init skill extractor
            skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
            matchedSkills = set()  # user's skills that match the job post
            describ = []  # description containing the matched skills
            for job in jobDesc:
                # skillNer extracts technical skillss
                annotation = skill_extractor.annotate(job)
                # list of full matches skills
                extractedSkills = [
                    fullMatch["doc_node_value"]
                    for fullMatch in annotation["results"]["full_matches"]
                ]
                # list of ngram scored skills
                extractedSkills.extend(
                    [
                        ngramScored["doc_node_value"]
                        for ngramScored in annotation["results"]["ngram_scored"]
                    ]
                )
                # check if any user's skills matched
                matched = set(extractedSkills).intersection(spider.skills)
                if matched:
                    matchedSkills.update(matched)
                    describ.append(annotation["text"])
            return matchedSkills, describ

        async def async_wrapper(jobDesc):
            skills, describ = await asyncio.to_thread(skill_extractor_items, jobDesc)
            return skills, describ

        jobItem = JobItem(skills=[])
        skills, describ = await async_wrapper(item.describ)
        # if the job matches at least one skill, return. Else, drop item
        if skills:
            jobItem.company = item.company
            jobItem.role = item.role
            jobItem.location = item.location
            jobItem.describ = describ
            jobItem.skills = skills
            return jobItem
        else:
            raise DropItem(f"No skills matched in {item}")
