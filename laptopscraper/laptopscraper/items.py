# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LaptopscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#         1 Company- String -Laptop Manufacturer
# 2 Product -String -Brand and Model
# 3 TypeName -String -Type (Notebook, Ultrabook, Gaming, etc.)
# 4 Inches -Numeric- Screen Size
# 5 ScreenResolution -String- Screen Resolution
# 6 Cpu- String -Central Processing Unit (CPU)
# 7 Ram -String- Laptop RAM
# 8 Memory -String- Hard Disk / SSD Memory
# 9 GPU -String- Graphics Processing Units (GPU)
# 10 OpSys -String- Operating System
# 11 Weight -String- Laptop Weight
# 12 Price_euros -Numeric- Price (Euro)


class laptopItem(scrapy.Item):
    brand = scrapy.Field()
    modelname = scrapy.Field()
    screensize = scrapy.Field()
    cpumodel = scrapy.Field()
    harddisksize = scrapy.Field()
    ram = scrapy.Field()
    gpu = scrapy.Field()
    operatingsystem = scrapy.Field()
    screen_resolution = scrapy.Field()
    item_weight = scrapy.Field()
    link_item = scrapy.Field()
    cpu_clockrate = scrapy.Field()
    graphicscarddescription = scrapy.Field()
    ratings = scrapy.Field()
    color = scrapy.Field()
    no_reviews = scrapy.Field()
    price = scrapy.Field()
    
