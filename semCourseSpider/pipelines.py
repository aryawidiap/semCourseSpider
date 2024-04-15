# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SemcoursespiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Combine objective to paragraph with numbered list, instead of array
        objectives = adapter.get('objective')
        value = '\n'.join(objectives)
        adapter['objective'] = value

        return item
