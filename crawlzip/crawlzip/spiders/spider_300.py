from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.shell import inspect_response
from collections import defaultdict

class ZipSpider(Spider):
  name = "zipspider2"
  start_urls = ['https://www.unitedstateszipcodes.org/']
  
  cities = []
  with open('city_300.csv') as f:
    for line in f:
      cities.append(line.strip('\n'))

  all_zips = defaultdict(list)

  def parse(self,response):
    for city in self.cities:
      print(city)
      yield FormRequest(url='https://www.unitedstateszipcodes.org/',formdata={'q':city}, dont_filter=True,callback=self.parse_zip,meta={'city':city})

  def parse_zip(self,response):
    city_name = response.meta['city']
    zips = response.xpath('//h2[@id="zips-list"]/following-sibling::div[1]/table/tbody/tr/td[1]/a/text()').extract()
    for z in zips:
      self.all_zips[city_name].append(z)

  @staticmethod
  def close(spider, reason):
    for k,v in spider.all_zips.items():
      with open(k+".txt",'w') as f:
        f.write("\n".join(v))
    closed = getattr(spider, 'closed', None)
    if callable(closed):
      return closed(reason)
