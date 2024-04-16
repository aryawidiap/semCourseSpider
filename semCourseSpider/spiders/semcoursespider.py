import scrapy
import re

from semCourseSpider.items import CourseItem


class SemcoursespiderSpider(scrapy.Spider):
    name = "semcoursespider"
    allowed_domains = ["asia.edu.tw"]
    start_urls = ["https://webs.asia.edu.tw/course_eng/"]

    custom_settings = {
        'FEEDS': {
            'course_data.csv': {'format':'csv', 'overwrite': True}
        }
    }
    

    def parse(self, response):
        form_data = {
            'cos_setyear_q': '112',
            'cos_setterm_q': '2',
            'chk_eng': 'E',
            'dept_no_q': 'EE30',
            'Qry': 'Query',
        }
        return scrapy.FormRequest.from_response(
            response,
            formdata=form_data,
            clickdata={'name': 'Qry'},
            callback=self.parse_after_form
        )

    def parse_after_form(self, response):
        # Get courses' links from the page
        course_link_list = response.css('a[href^="course_outline.asp?"]::attr(href)').getall()
        # For each link, request the page and process with parse_table method
        for link in course_link_list:
            yield scrapy.Request("https://webs.asia.edu.tw/course_eng/"+link, self.parse_table)

    def parse_table(self, response):
        # Get the rows from main table element
        table = response.css('table.standard-table2 > tr')

        # Parse all rows from the main table
        attributeDict = {}
        for row in table:
            table_data = row.css('td')
            if(len(table_data) == 4):
                attributeDict[table_data[0].css('::text').get().strip()] = table_data[1].css('::text').extract()
                attributeDict[table_data[2].css('::text').get().strip()] = table_data[3].css('::text').extract()
            elif(len(table_data) == 2):
                attributeDict[table_data[0].css('::text').get().strip()] = table_data[1].css('::text').extract()

        # Assign the desired values from attributeDict to course_item
        course_item = CourseItem()
        for key in attributeDict:
            match key:
                case 'Course Code / Class':
                    code_and_class = attributeDict[key][0].split()
                    course_item['course_code'] = code_and_class[0]
                    course_item['class_name'] = code_and_class[2]
                case 'Title of Course':
                    course_item['course_name_in_English'] = attributeDict[key]
                case 'Credits':
                    course_item['credits'] = attributeDict[key]
                case 'Number of Students':
                    if(len(attributeDict[key]) > 0):
                        course_item['number_of_students'] = attributeDict[key][0].strip()
                case 'Upper Limit':
                    if(len(attributeDict[key]) > 0):
                        course_item['upper_limit'] = attributeDict[key][0].strip()
                case '一、教學目標(Objective)':
                    course_item['objective'] = attributeDict[key]
                case '三、教材內容(Materials)':
                    course_item['materials'] = attributeDict[key]
                case 'Department / Year':
                    match_group = re.search("\d", attributeDict[key][0])
                    if(match_group):
                        course_item['year'] = match_group.group()
                    else:
                        course_item['year'] = 0
        course_item['link_to_syllabus'] = response.request.url

        yield course_item
