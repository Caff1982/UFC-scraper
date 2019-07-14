import scrapy
import time
from datetime import datetime
from ..items import EventItem, FightItem, RoundItem, FighterItem

FIGHTER_TRACKER = set()

class UFCScraper(scrapy.Spider):
	name = 'ufcstats'

	def start_requests(self):
		urls = [
			'http://ufcstats.com/statistics/events/completed?page=all'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		event_urls = response.xpath("//a[@class='b-link b-link_style_black']/@href").extract()
		for pk, event in enumerate(event_urls):
			time.sleep(1.5)
			yield scrapy.Request(url=event, callback=self.parse_event, meta={"pk": pk})

	def parse_event(self, response):
		banner = response.css('.b-list__box-list-item::text').getall()
		# remove empty items from list
		banner = [i.strip() for i in banner if i.strip() is not '']
		item = EventItem()
		item['primary_key'] = response.meta["pk"]
		obj_date = datetime.strptime(banner[0], '%B %d, %Y')
		item['date'] = datetime.strftime(obj_date, '%Y:%m:%d')
		item['location'] = banner[1]
		if len(banner) == 3:
			item['attendance'] = int(banner[2].replace(',', ''))
		else:
			item['attendance'] = 0
		fight_urls = response.xpath("//tr/@data-link").extract()
		fighter_urls = response.xpath("//a[@class='b-link b-link_style_black']/@href").extract()
		item['fight_count'] = len(fight_urls)
		item['name'] = response.xpath('/html/body/section/div/h2/span/text()').get().strip()

		yield item

		for i, fight in enumerate(fight_urls):
			time.sleep(1.5)
			fight_id = fight.split('details/')[1]
			red_fighter_id = fighter_urls[2*i].split('details/')[1]
			blue_fighter_id = fighter_urls[2*i+1].split('details/')[1]
			yield(scrapy.Request(url=fight, callback=self.parse_fight, meta={"event_id": item['primary_key'],
																			"bout_order": i+1,
																			"fight_id": fight_id,
																			"red_fighter_id": red_fighter_id,
																			"blue_fighter_id": blue_fighter_id
																			}))

	def parse_fight(self, response):
		weight_class = response.xpath('/html/body/section/div/div/div[2]/div[1]/i/text()').extract()
		weight_class = [i.strip() for i in weight_class if i.strip() != '']
		title_pic_url = response.xpath("/html/body/section/div/div/div[2]/div[1]/i/img/@src").extract()
		fighter_urls = response.xpath("//h3[@class='b-fight-details__person-name']/a/@href").extract()
		results = response.xpath("//div[@class='b-fight-details__person']").extract()
		end_method = response.xpath("/html/body/section/div/div/div[2]/div[2]/p[1]/i[1]/i[2]/text()").extract_first()
		end_details = response.xpath("//p[@class='b-fight-details__text']")
		rounds = response.xpath("//div[@class='b-fight-details__bar-charts-row clearfix']")
		end_time = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[3]/text()').extract()
		referee = response.xpath('//html/body/section/div/div/div[2]/div[2]/p[1]/i[5]/span/text()').get().strip()
		time_format = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[1]/i[4]/text()').extract()

		fight_item = FightItem()
		fight_item['fight_id'] = response.meta['fight_id']
		fight_item['event_id'] = response.meta['event_id']
		fight_item['bout_order'] = response.meta['bout_order']
		fight_item['weight_class'] = weight_class[0]
		if title_pic_url and title_pic_url[0][-8:] == 'belt.png':
				fight_item['title_fight'] = 1
		else:
			fight_item['title_fight'] = 0

		if results[0].split('\n  </i>')[0].split(' ')[-1] == 'W':
			fight_item['result'] = 'red'
		elif results[0].split('\n  </i>')[0].split(' ')[-1] == 'L':
			fight_item['result'] = 'blue'
		elif results[0].split('\n  </i>')[0].split(' ')[-1] == 'D':
			fight_item['result'] = 'draw'
		elif results[0].split('\n  </i>')[0].split(' ')[-1] == 'NC':
			fight_item['result'] = 'nc'

		fight_item['red_fighter_id'] = response.meta['red_fighter_id']
		fight_item['blue_fighter_id'] = response.meta['blue_fighter_id']
		fight_item['end_method'] = end_method
		judges_scores = end_details[1].css('.b-fight-details__text-item::text').extract()
		if len(judges_scores) == 6: # check if points decision
			fight_item['end_details'] = ' '.join([i.strip() for i in  judges_scores if i.strip() != ''])
		else:
			path = response.xpath('/html/body/section/div/div/div[2]/div[2]/p[2]/text()').extract()
			fight_item['end_details'] = path[1].strip()

		fight_item['end_time'] = end_time[1].strip()
		fight_item['end_round'] = len(rounds)
		fight_item['time_format'] = time_format[1].strip()
		fight_item['referee'] = referee
		yield fight_item

		all_cols = response.xpath("//td[@class='b-fight-details__table-col']").css('.b-fight-details__table-text::text').extract()
		all_cols = [i.strip() for i in all_cols]

		top_cols = all_cols[18:18+18*len(rounds)]
		btm_idx = 18+18*len(rounds)+16
		btm_cols = all_cols[btm_idx:]

		for rnd in range(len(rounds)):
			round_item = RoundItem()
			fields = round_item.fields.keys()

			idx1 = rnd*18 # index for first rows, 18 selectors
			idx2 = rnd*16 # index for first rows, 16 selectors
			round_cols = top_cols[idx1:idx1+18] + btm_cols[idx2:idx2+16]

			round_item['event_id'] = response.meta['event_id']
			round_item['fight_id'] = response.meta['fight_id']
			round_item['round_count'] = rnd
			round_item['red_kd'] = int(round_cols[0])
			round_item['red_sig_str_attempted'] = int(round_cols[2].split(' ')[2])
			round_item['red_sig_str_landed'] = int(round_cols[2].split(' ')[0])
			round_item['red_sig_str_perc'] = int(round_cols[4].replace('%', ''))/100
			round_item['red_total_str_attempted'] = int(round_cols[6].split(' ')[2])
			round_item['red_total_str_landed'] = int(round_cols[6].split(' ')[0])
			if round_item['red_total_str_attempted'] == 0:
				round_item['red_total_str_perc'] = 0.0
			else:
				round_item['red_total_str_perc'] = round(round_item['red_total_str_landed']/round_item['red_total_str_attempted'], 2)
			round_item['red_td_landed'] = int(round_cols[8].split(' ')[0])
			round_item['red_td_attempted'] = int(round_cols[8].split(' ')[2])
			round_item['red_td_perc'] = int(round_cols[10].replace('%', ''))/100
			round_item['red_sub_attempted'] = int(round_cols[12])
			round_item['red_pass'] = int(round_cols[14])
			round_item['red_rev'] = int(round_cols[16])
			round_item['red_head_landed'] = int(round_cols[22].split(' ')[0])
			round_item['red_leg_attempted'] = int(round_cols[26].split(' ')[2])
			round_item['red_leg_landed'] = int(round_cols[26].split(' ')[0])
			round_item['red_distance_attempted'] = int(round_cols[28].split(' ')[2])
			round_item['red_distance_landed'] = int(round_cols[28].split(' ')[0])
			round_item['red_clinch_attempted'] = int(round_cols[30].split(' ')[2])
			round_item['red_clinch_landed'] = int(round_cols[30].split(' ')[0])
			round_item['red_ground_attempted'] = int(round_cols[32].split(' ')[2])
			round_item['red_ground_landed'] = int(round_cols[32].split(' ')[0])
			round_item['blue_kd'] = int(round_cols[1])
			round_item['blue_sig_str_attempted'] = int(round_cols[3].split(' ')[0])
			round_item['blue_sig_str_landed'] = int(round_cols[3].split(' ')[2])
			round_item['blue_sig_str_perc'] = int(round_cols[4].replace('%', ''))/100
			round_item['blue_total_str_attempted'] = int(round_cols[7].split(' ')[2])
			round_item['blue_total_str_landed'] = int(round_cols[7].split(' ')[0])
			if round_item['blue_total_str_attempted'] == 0:
				round_item['blue_total_str_perc'] = 0.0
			else:
				round_item['blue_total_str_perc'] = round(round_item['blue_total_str_landed']/round_item['blue_total_str_attempted'], 2)
			round_item['blue_total_str_attempted'] = int(round_cols[7].split(' ')[2])
			round_item['blue_td_landed'] = int(round_cols[9].split(' ')[0])
			round_item['blue_td_attempted'] = int(round_cols[9].split(' ')[2])
			round_item['blue_td_perc'] = int(round_cols[11].replace('%', ''))/100
			round_item['blue_sub_attempted'] = int(round_cols[13])
			round_item['blue_pass'] = int(round_cols[15])
			round_item['blue_rev'] = int(round_cols[17])
			round_item['blue_head_landed'] = int(round_cols[23].split(' ')[0])
			round_item['blue_leg_attempted'] = int(round_cols[27].split(' ')[2])
			round_item['blue_leg_landed'] = int(round_cols[27].split(' ')[0])
			round_item['blue_distance_attempted'] = int(round_cols[29].split(' ')[2])
			round_item['blue_distance_landed'] = int(round_cols[29].split(' ')[0])
			round_item['blue_clinch_attempted'] = int(round_cols[31].split(' ')[2])
			round_item['blue_clinch_landed'] = int(round_cols[31].split(' ')[0])
			round_item['blue_ground_attempted'] = int(round_cols[33].split(' ')[2])
			round_item['blue_ground_landed'] = int(round_cols[33].split(' ')[0])

			yield round_item

		if fight_item['red_fighter_id'] not in FIGHTER_TRACKER:
			time.sleep(1.5)
			yield(scrapy.Request(url='http://ufcstats.com/fighter-details/' + fight_item['red_fighter_id'], 
								callback=self.parse_fighter, meta={"fighter_id": fight_item['red_fighter_id']}))
			FIGHTER_TRACKER.add(fight_item['red_fighter_id'])
		if fight_item['blue_fighter_id'] not in FIGHTER_TRACKER:
			time.sleep(1.5)
			yield(scrapy.Request(url='http://ufcstats.com/fighter-details/' + fight_item['blue_fighter_id'], 
								callback=self.parse_fighter, meta={"fighter_id": fight_item['blue_fighter_id']}))
			FIGHTER_TRACKER.add(fight_item['blue_fighter_id'])
	
	def parse_fighter(self, response):
		item = FighterItem()
		item['fighter_id'] = response.meta['fighter_id']
		fullname = response.xpath("/html/body/section/div/h2/span[1]/text()")[0].extract().strip()
		item['first_name'] = fullname.split()[0]
		item['last_name'] = ' '.join(fullname.split()[1:]) # join incase several names
		item['nickname'] = response.xpath("//p[@class='b-content__Nickname']/text()")[0].extract().strip()
		height = response.xpath("/html/body/section/div/div/div[1]/ul/li[1]/text()")[1].extract().strip().split()
		weight = response.xpath("/html/body/section/div/div/div[1]/ul/li[2]/text()")[1].extract().strip().split(' ')[0]
		reach = response.xpath("/html/body/section/div/div/div[1]/ul/li[3]/text()")[1].extract().strip().replace('"', '')
		dob = response.xpath("/html/body/section/div/div/div[1]/ul/li[5]/text()")[1].extract().strip()
		try: # some of these fields have '--' on the website, treating them as optional fields in database
			item['height'] = 12 * int(height[0].replace("'", "")) + int(height[1].replace('"', ''))
			item['weight'] = int(weight)
			item['reach'] = int(reach)
			obj_date = datetime.strptime(dob, '%b %d, %Y')
			item['dob'] = datetime.strftime(obj_date, '%Y:%m:%d')
		except ValueError as e:
			pass

		item['stance'] = response.xpath("/html/body/section/div/div/div[1]/ul/li[4]/text()")[1].extract().strip()
		item['slpm'] = float(response.xpath("/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[1]/text()")[1].extract().strip())
		str_acc = response. xpath("/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[2]/text()")[1].extract().strip()
		item['str_acc'] = int(str_acc.replace('%', ''))/100
		item['sapm'] = float(response. xpath("/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[3]/text()")[1].extract().strip())
		str_def = response. xpath("/html/body/section/div/div/div[2]/div[1]/div[1]/ul/li[4]/text()")[1].extract().strip()
		item['str_def'] = int(str_def.replace('%', ''))/100
		item['td_avg'] = float(response.xpath("/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[2]/text()")[1].extract().strip())
		td_acc = response.xpath("/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[3]/text()")[1].extract().strip()
		item['td_acc'] = int(td_acc.replace('%', ''))/100
		td_def = response.xpath("/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[4]/text()")[1].extract().strip()
		item['td_def'] = int(td_def.replace('%', ''))/100
		item['sub_avg'] = float(response.xpath("/html/body/section/div/div/div[2]/div[1]/div[2]/ul/li[5]/text()")[1].extract().strip())
		records = response.xpath("/html/body/section/div/h2/span[2]/text()")[0].extract().strip().split('-')
		item['wins'] = int(records[0].split(' ')[1])
		item['losses'] = int(records[1])
		if records[2][-3:-1] == 'NC':
			item['draw'] = int(records[1])
			item['ncs'] = int(records[2].split(' ')[1].replace('(', ''))
		else:
			item['draw'] = records[2]
			item['ncs'] = 0

		yield item
