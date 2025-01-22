import scrapy

from ..items import laptopItem

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LaptopSpider(scrapy.Spider):
    name = "laptopspiderV2"
    
    
    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': {"brand" : "brand" , "modelname" : "model", "screensize" : "screen_size",
                           "screen_resolution" : "screen_resolution",
                           "cpumodel" : "cpu", "cpu_clockrate" : "cpu_speed", "ram" : "ram", "harddisksize" : "memory",
                           "gpu" : "gpu","graphicscarddescription": "graphics_card_description", "operatingsystem": "OpSys", "item_weight" : "weight",
                           "color" : "color", "no_reviews" : "No_reviews", "ratings" : "ratings", "price":"price", "link_item" : "link_item"},
    
    'FEEDS' : {'data/%(name)s/%(name)s_Apple.csv' : {'format' : 'csv'}}
  }
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
            amazon_search_url = 'https://www.amazon.com/s?k=laptop&i=computers&brand=Apple&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page':1})
            
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
             last_page = int(response.css('span.s-pagination-item.s-pagination-disabled::text').getall()[1])
             for page_num in range(2,last_page+1):
                 amazon_search_url = f'https://www.amazon.com/s?k=laptop&i=computers&brand=Apple&page={page_num}'
                 yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})

    

    def parse_product_data(self, response):
        dic = {'brand': None, 'modelname' : None, 'screensize' : None, 'cpu_clockrate': None, 'cpumodel':None, 'harddisksize':None, 
               'ram' : None, 'gpu': None, 'operatingsystem' : None, "screen_resolution" : None, "item_weight" : None,
               'graphicscarddescription':None, 'ratings' : None, "no_reviews" : None, "color" : None} 
        laptopitem = laptopItem()
        table_item = response.css('#productDetails_expanderTables_depthLeftSections > div:nth-child(1) > div > div > table tr')
        table_memory = response.css('#productDetails_expanderTables_depthLeftSections > div:nth-child(2) > div > div > table tr')
        table_storage = response.css('#productDetails_expanderTables_depthLeftSections > div:nth-child(4) > div > div > table tr')
        table_display = response.css('#productDetails_expanderTables_depthRightSections > div:nth-child(1) > div > div > table tr')
        table_processor= response.css('#productDetails_expanderTables_depthRightSections > div:nth-child(3) > div > div > table tr')
        
        
        
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
        
        
            
         # --------- table_item--------------
         
          
        dic['modelname'] = table_item.css('th:contains("Model Number") + td::text').get()
        
        dic['brand'] = table_item.css('th:contains("Brand") + td::text').get()
                
         # modelname:
        dic['color'] = table_item.css('th:contains("Color") + td::text').get()
            
         # operating system:
        dic['operatingsystem'] = table_item.css('th:contains("Operating System") + td::text').get()
            
        #item weight:
        dic['item_weight'] = table_item.css('th:contains("Item Weight") + td::text').get()
        
        
        # --------------------table memory------------------
        dic['ram'] = table_memory.css('th:contains("Ram Memory Installed Size") + td::text').get()
        
        #------------------- table_storage -----------------
        dic['harddisksize'] = table_storage.css('th:contains("Hard Disk Size") + td::text').get()
        
        #------------------ Display table-------------------
        dic['screensize'] = table_display.css('th:contains("Screen Size") + td::text').get()
        
        dic['screen_resolution'] = table_display.css('th:contains("Screen Resolution") + td::text').get()
        
        dic['graphicscarddescription'] = table_display.css('th:contains("Card Description") + td::text').get()
        
        dic['gpu'] = table_display.css('th:contains("Graphics Coprocessor") + td::text').get()
        
        #------------------------- table_processor ----------------
        
        dic['cpumodel'] = table_processor.css('th:contains("CPU Model Number") + td::text').get()
        
        if dic['cpumodel'] is None:
            dic['cpumodel'] = table_processor.css('th:contains("CPU Model") + td::text').get()
        
        dic['cpu_clockrate'] = table_processor.css('th:contains("CPU Speed") + td::text').get()

        
        

        if table_item == []:
            table_rows3 = response.css('#btfContent31_feature_div > div > div:nth-child(3) > div > div:nth-child(1) > div > table tr')
            table_rows4 = response.css('#btfContent31_feature_div > div > div:nth-child(3) > div > div.a-column.a-span6.block-content.block-type-table.textalign-left.a-span-last > div > table tr')

            #-----------------------------------Different format--------------------------------------
            dic['ram'] = response.css('#variation_style_name > div > span::text').get()
            
            dic['harddisksize'] = response.css('#variation_size_name > div > span::text').get()
            
            dic['color'] =   response.css('#variation_color_name > div > span::text').get()
            
            # Access table and scrape object:
            
            dic['screensize'] = table_rows3.css('td:contains("Display") + td p::text').get().split()[0]
            
            screen_resolution = list(table_rows3.css('td:contains("Display") + td p::text').get().split())
            
            screen_resolution =  screen_resolution[screen_resolution.index('pixels')-3:screen_resolution.index('pixels')]
            
            screen_resolution = screen_resolution[0] + "x" + screen_resolution[2]
            
            dic['screen_resolution'] = screen_resolution
            
            
            dic['gpu'] = table_rows3.css('td:contains("Graphics and Video Support") + td p::text').get()
                        
            dic['item_weight'] = table_rows4.css('td:contains("Weight") + td p::text').get()
            
            dic['modelname'] = response.css('#content-grid-widget-v1\.0 > div > div:nth-child(2) > div > div > div > h3::text').get()
            
            dic['cpu_clockrate'] = 'depend'
            
            cpumodel = list(table_rows3.css('td:contains("Processor") + td p::text').get().split())
            
            cpumodel =  cpumodel[cpumodel.index('Apple'):cpumodel.index('Apple')+3]
            
            dic['cpumodel'] = " ".join(cpumodel)
            
            
            
            dic['operatingsystem'] = "mac_os"
            
            dic['brand'] = 'Apple'
            
            
            
        table = response.css('.a-normal.a-spacing-micro tr')
        for tr in table:
            key = tr.css('td.a-span3 span::text').get().lower()
            key = key.replace(" ", "")
            if key == 'rammemoryinstalledsize':
                key = 'ram'
            if key in dic and dic[key] is None: 
                dic[key] =  tr.css('td.a-span9 span::text').get()
                
        if dic['graphicscarddescription'] is None:
            dic['graphicscarddescription'] = 'dedicated'
                
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
            
        
        

