import scrapy

from ..items import laptopItem

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LaptopSpider(scrapy.Spider):
    name = "laptopspiderV1"
    
    #brand = ["lenovo", "HP"]

    
    #custom_settings = {
    # specifies exported fields and order
# =============================================================================
#     'FEED_EXPORT_FIELDS': {"brand" : "brand" , "modelname" : "model", "screensize" : "screen_size",
#                            "screen_resolution" : "screen_resolution",
#                            "cpumodel" : "cpu", "cpu_clockrate" : "cpu_speed", "ram" : "ram", "harddisksize" : "memory",
#                            "gpu" : "gpu","graphicscarddescription": "graphics_card_description", "operatingsystem": "OpSys", "item_weight" : "weight",
#                            "color" : "color", "no_reviews" : "No_reviews", "ratings" : "ratings", "price":"price", "link_item" : "link_item"},
# =============================================================================
    
    #'FEEDS' : {'data/%(name)s/%(name)s_Apple.csv' : {'format' : 'csv'}}
  #}
    # =============================================================================
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
    # =============================================================================

    def start_requests(self):
        keyword_list = ['laptop']
        for keyword in keyword_list:
            #amazon_search_url = 'https://www.amazon.com/s?k=laptop&i=computers&brand=Apple&page=1'
            product_url = 'https://www.amazon.com/A315-24P-R7VH-Display-Quad-Core-Processor-Graphics/dp/B0BS4BP8FB/ref=sr_1_1?crid=2IJL28U105SIU&keywords=laptop&qid=1701881734&refinements=p_89%3Aacer&rnid=2528832011&s=electronics&sprefix=lapto%2Caps%2C418&sr=1-1&th=1'
            yield SeleniumRequest(url=product_url, callback=self.parse_product_data,
                                      meta={'keyword': keyword},
                                      wait_time=20,
                                      wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, '.a-price .a-offscreen ::text)')))
            #yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page':1})
            
    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 
        
        ## Discover Product URLs
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = ('https://www.amazon.com' + relative_url).split("?")[0]
            yield SeleniumRequest(url=product_url, callback=self.parse_product_data,
                                      meta={'keyword': keyword, 'page': page},
                                      wait_time=5,
                                      wait_until=EC.element_to_be_clickable((By.CSS_SELECTOR, '.a-price .a-offscreen ::text)')))
            
        ## Get All Pages
        if page == 1:
             #last_page = int(response.css('span.s-pagination-item.s-pagination-disabled::text').getall()[1])
             for page_num in range(2,46):
                 amazon_search_url = f'https://www.amazon.com/s?k=laptop&i=computers&brand=Apple&page={page_num}'
                 yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})


    def parse_product_data(self, response):
        dic = {'brand': None, 'modelname' : None, 'screensize' : None, 'cpu_clockrate': None, 'cpumodel':None, 'harddisksize':None, 
               'ram' : None, 'gpu': None, 'operatingsystem' : None, "screen_resolution" : None, "item_weight" : None,
               'graphicscarddescription':None, 'ratings' : None, "no_reviews" : None, "color" : None} 
        laptopitem = laptopItem()
        table_rows1 = response.css('#productDetails_expanderTables_depthLeftSections > div:nth-child(1) > div > div > table tr') 
        table_rows2 = response.css('#productDetails_techSpec_section_2 tr')
        
        print(table_rows1)
        print(table_rows2)
        
        
        price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        if not price or len(price) < 2:
            price = response.css('.a-price .a-offscreen ::text').get("")
            if not price:
                price = response.css('#price_inside_buybox ::text').get("")
        # Find rating of item:
        ratings = response.css('#acrPopover > span.a-declarative > a > span::text').get()
        dic["ratings"] = ratings
        
        # Find number of reviews
        no_reviews = response.css("#acrCustomerReviewText::text").get()
        dic["no_reviews"] = no_reviews
        
        
            
        dic['item_weight'] = table_rows1.css('th:contains("Item Weight") + td::text').get()
            
        if table_rows2 is not []:
            # brand:
            dic['brand'] = table_rows2.css('th:contains("Brand") + td::text').get()
                
            # modelname:
            dic['modelname'] = table_rows2.css('th:contains("Series") + td::text').get()
            
            # operating system:
            dic['operatingsystem'] = table_rows2.css('th:contains("Operating System") + td::text').get()
            
            #item weight:
            #dic['item_weight'] = table_rows2.css('th:contains("Item Weight") + td::text').get()
            
        # screensize:
        dic['screensize'] = table_rows1.css('th:contains("Standing screen display size") + td::text').get()
        
        # screensize:
        dic['screen_resolution'] = table_rows1.css('th:contains("Screen Resolution") + td::text').get()
            
        # cpu_model:
        cpu = table_rows1.css('th:contains("Processor") + td::text').get()
        if cpu: 
            cpu_list = cpu.split()
            if len(cpu_list) >= 3:
                dic['cpu_clockrate'] = cpu_list[0] + " " + cpu_list[1]
                dic['cpumodel'] = cpu_list[2]
            elif len(cpu_list) >= 2:
                dic['cpu_clockrate'] = cpu_list[0] + " " + cpu_list[1]
            else:
                dic['cpumodel'] = cpu
                
        # hard disk:
        hard_drive = table_rows1.css('th:contains("Hard Drive") + td::text').get()
        hard_drive_list = hard_drive.split() if hard_drive is not None else []
        if len(hard_drive_list) == 3:
            dic['harddisksize'] = hard_drive_list[0] +" "+hard_drive_list[1]
        # ram:
        ram =  table_rows1.css('th:contains("RAM") + td::text').get()
        ram_list = ram.split() if ram is not None else []
        if len(ram_list) == 3:
            dic['ram'] = ram_list[0] +" "+ram_list[1]
        
        # gpu:
        dic['graphicscarddescription'] =  table_rows1.css('th:contains("Card Description") + td::text').get()
        dic['gpu'] =  table_rows1.css('th:contains("Graphics Coprocessor") + td::text').get()
        
        

            
            
            
        table = response.css('.a-normal.a-spacing-micro tr')
        for tr in table:
            key = tr.css('td.a-span3 span::text').get().lower()
            key = key.replace(" ", "")
            if key == 'rammemoryinstalledsize':
                key = 'ram'
            if key in dic and dic[key] is None: 
                dic[key] =  tr.css('td.a-span9 span::text').get()
                
        count = 0
        for key, value in dic.items():
            laptopitem[key] = self.transform(value)
            if value == None:
                count += 1
        
        # If number of none value attribute means it's not laptop item
        # laptop but does't have any attribute -> discard it
        if count >= 6:
            return
            
        laptopitem['link_item'] = response.url
        laptopitem['price'] = price
        yield laptopitem
        
    def transform(self,data):
        if data is not None:
            data = data.strip()
            data = data.replace("\u200e", "")
        return data
            
        
        

