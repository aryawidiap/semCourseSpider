# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class CourseItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    course_code = Field()
    class_name = Field()
    credits = Field()
    course_name_in_English = Field()
    link_to_syllabus = Field()
    number_of_students = Field()
    upper_limit = Field()
    objective = Field()
    materials = Field()
    year = Field()
