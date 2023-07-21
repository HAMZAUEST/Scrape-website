# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FirstscrapingPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        #strip all whitespaces from string except desc
        field_names=adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if isinstance(value, str):  # Check if the value is a string before applying strip()
                    adapter[field_name] = value.strip()              


        #category & product tyoe ---> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # review -> convert string to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string[0].split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == 'four':
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5

        return item
