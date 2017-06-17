from scrapy.http import FormRequest
from scrapy.spiders import Spider
from scrapy.shell import inspect_response
from collections import defaultdict

class ZipSpider(Spider):
  name = "zipspider"
  start_urls = ['https://www.unitedstateszipcodes.org/']
  
  cities = {
  'sanf':
        ['San Francisco', 'Daly city', 'San Mateo', 'palo alto', 'San Jose', 'Livermore', 'Walnut Creek', 'Berkeley', 'Richmond','Mill valley', 'Concord', 'Santa Rose'],

  'san diego':
        ['San Diego', 'Chula Vista', 'Carlsbad', 'Escondido', 'Ramona', 'El cajon', 'Alpine', 'boulevard'],

  'Sacramento':
        ['Sacramento', 'Roseville', 'Folsom', 'Davis', 'Elk Grove', 'Lincoln', 'Auburn Fairfield', 'Rio Vista', 'Lodi', 'Woodland'],

  'Pittsburgh':
        ['Pittsburgh', 'Moon', 'Monroeville', 'West Mifflin', 'Mt lebanon', 'Penn hills', 'West mifflin', 'Irwin', 'West Newton', 'Mckeesport'],

  'Chicago':
        ['Chicago', 'Evanston', 'Schaumburg', 'Naperville', 'Joliet','Gary', 'Kankakee', 'Rockford', 'Milwaukee'],

  'Phoenix':
        ['Phoenix', 'Glendale','Chandler', 'Goodyear','Surprise', 'Carefree','Mesa','Fountain Hills'],

  'Denver':
        ['Denver', 'Thornton', 'Aurora', 'Centennial', 'Boulder', 'Longmont'],

  }

  all_zips = defaultdict(list)

  def parse(self,response):
    for k,v in self.cities.items(): 
      for city in v:
        print(city)
        yield FormRequest(url='https://www.unitedstateszipcodes.org/',formdata={'q':city}, dont_filter=True,callback=self.parse_zip,meta={'great_city':k})

  def parse_zip(self,response):
    great_city = response.meta['great_city']
    zips = response.xpath('//h2[@id="zips-list"]/following-sibling::div[1]/table/tbody/tr/td[1]/a/text()').extract()
    for z in zips:
      self.all_zips[great_city].append(z)

  @staticmethod
  def close(spider, reason):
    for k,v in spider.all_zips.items():
      with open(k+".txt",'w') as f:
        f.write("\n".join(v))
    closed = getattr(spider, 'closed', None)
    if callable(closed):
      return closed(reason)
