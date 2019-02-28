# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 16:27:39 2018

@author: Shishir
"""
import scrapy
#command to run is below
#scrapy runspider SpiderTest_fr.py -o Appareillage_saillie.xml
#scrapy shell <link> .... this is for scrapy shell only
url_fabien = 'https://www.rexel.fr/frx/Cat%C3%A9gorie/Appareillage-et-contr%C3%B4le-du-b%C3%A2timent/Appareillage-terminal/c/M2_0107'
url_Système_domotique = 'https://www.rexel.fr/frx/Cat%C3%A9gorie/Appareillage-et-contr%C3%B4le-du-b%C3%A2timent/Automatisme-du-b%C3%A2timent/Syst%C3%A8me-domotique/c/M2_010504'
class GetProductPage(scrapy.Spider):
    name = "Rexel_Products"
    allowed_domains = ['www.rexel.fr']
    start_urls = [url_Système_domotique,
                  ]
    def parse(self, response):
        urls = response.css('div.item-Name > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details )
        
        #following next page logic
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback = self.parse)       
                    
    def parse_details(self, response):  
        if response.css('td > table >tr > td > input '):
            count = 0
            for tt in response.css('td > table >tr > td > input '):
                item_spec = {
                        'tree':response.css('div.breadcrumb > ul >  li > a::text').extract(),
                        'ref_rexel': response.css('div.product-detail-label > span ::text').extract_first().replace(' ', ''),
                        'vendor_name': response.css('div.product-by-name.productDetail-by-name *::text')[1].extract().replace('\t', '').replace('\r', '').replace('\n', ''),
                        'product_name' : response.css('h1::text').extract_first().replace('\t', '').replace('\r', '').replace('\n', ''),
                        'product_cat' : response.css('div.headline::text').extract_first(),
                        'tech_name' : response.css('th.noBold::text').extract()[count],
                        'tech_value': tt.css('input ::attr(value)').extract_first()                        
                        }
                count = count + 1
                yield item_spec    
        else:
            #No Item SPecs available for the product
            item_spec = {     
                    'tree':response.css('div.breadcrumb > ul >  li > a::text').extract(),
                    'ref_rexel': response.css('div.product-detail-label > span ::text').extract_first().replace(' ', ''),
                    'vendor_name': response.css('div.product-by-name.productDetail-by-name *::text')[1].extract().replace('\t', '').replace('\r', '').replace('\n', ''),
                    'product_name' : response.css('h1::text').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')
                    }
            yield item_spec  

## response.css('th.noBold ::text').extract()