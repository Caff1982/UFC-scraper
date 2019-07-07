import scrapy
import time
from datetime import datetime
from ..items import EventItem, FightItem

class UFCScraper(scrapy.Spider):
	name = 'ufcstats'

	def start_requests(self):
		urls = [
			'http://ufcstats.com/statistics/events/completed'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):	
		# dates = response.xpath("//span[@class='b-statistics__date']/text()").extract()[1:] # skip the upcoming fight
		# venues = response.xpath("//td[@class='b-statistics__table-col b-statistics__table-col_style_big-top-padding']/text()").extract()[1:]
		# fights = response.xpath("//a[@class='b-link b-link_style_black']/text()").extract()
		# for date, venue, fight in zip(dates, venues, fights):
		# 	item = EventItem()
		# 	item['date'] = date.strip()
		# 	item['venue'] = venue.strip()
		# 	item['fight'] = fight.strip()
		# 	yield item
		
		event_urls = response.xpath("//a[@class='b-link b-link_style_black']/@href").extract()
		for event in event_urls[:3]:
			time.sleep(2)
			yield scrapy.Request(url=event, callback=self.parse_event, )

	def parse_event(self, response):
		banner = response.css('.b-list__box-list-item::text').getall()
		# remove empty items from list
		banner = [i.strip() for i in banner if i.strip() is not '']
		item = EventItem()
		obj_date = datetime.strptime(banner[0], '%B %d, %Y')
		item['date'] = datetime.strftime(obj_date, '%Y:%m:%d')
		item['location'] = banner[1]
		item['attendance'] = int(banner[2].replace(',', ''))
		fights = response.xpath("//tr/@data-link").extract()
		item['fight_count'] = len(fights)
		item['name'] = response.xpath('/html/body/section/div/h2/span/text()').get().strip()
		yield item

		for fight in fights[:3]:
			time.sleep(1)
			yield(scrapy.Request(url=fight, callback=self.parse_fight))

	def parse_fight(self, response):
		bout = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[2]/text()').extract()
		item = FightItem()
		item['bout_order'] = int(bout[1].strip())
		yield item

		
