# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    primary_key = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    attendance = scrapy.Field()
    name = scrapy.Field()
    fight_count = scrapy.Field()

class FightItem(scrapy.Item):
	fight_id = scrapy.Field()
	event_id = scrapy.Field()
	bout_order = scrapy.Field()
	weight_class = scrapy.Field()
	title_fight = scrapy.Field()
	red_fighter_id = scrapy.Field()
	blue_fighter_id = scrapy.Field()
	result = scrapy.Field()
	end_method = scrapy.Field()
	end_details = scrapy.Field()
	end_round = scrapy.Field()
	end_time = scrapy.Field()
	time_format = scrapy.Field()
	referee = scrapy.Field()

class RoundItem(scrapy.Item):
	event_id = scrapy.Field()
	fight_id = scrapy.Field()
	round_count = scrapy.Field()
	red_kd = scrapy.Field()
	red_sig_str_attempted = scrapy.Field()
	red_sig_str_landed = scrapy.Field()
	red_sig_str_perc = scrapy.Field()
	red_total_str_attempted = scrapy.Field()
	red_total_str_landed = scrapy.Field()
	red_total_str_perc = scrapy.Field()
	red_td_landed = scrapy.Field()
	red_td_attempted = scrapy.Field()
	red_td_perc = scrapy.Field()
	red_sub_attempted = scrapy.Field()
	red_pass = scrapy.Field()
	red_rev = scrapy.Field()
	red_head_landed = scrapy.Field()
	red_leg_attempted = scrapy.Field()
	red_leg_landed = scrapy.Field()
	red_distance_attempted = scrapy.Field()
	red_distance_landed = scrapy.Field()
	red_clinch_attempted = scrapy.Field()
	red_clinch_landed = scrapy.Field()
	red_ground_attempted = scrapy.Field()
	red_ground_landed = scrapy.Field()
	blue_kd = scrapy.Field()
	blue_sig_str_attempted = scrapy.Field()
	blue_sig_str_landed = scrapy.Field()
	blue_sig_str_perc = scrapy.Field()
	blue_total_str_attempted = scrapy.Field()
	blue_total_str_landed = scrapy.Field()
	blue_total_str_perc = scrapy.Field()
	blue_td_landed = scrapy.Field()
	blue_td_attempted = scrapy.Field()
	blue_td_perc = scrapy.Field()
	blue_sub_attempted = scrapy.Field()
	blue_pass = scrapy.Field()
	blue_rev = scrapy.Field()
	blue_head_landed = scrapy.Field()
	blue_leg_attempted = scrapy.Field()
	blue_leg_landed = scrapy.Field()
	blue_distance_attempted = scrapy.Field()
	blue_distance_landed = scrapy.Field()
	blue_clinch_attempted = scrapy.Field()
	blue_clinch_landed = scrapy.Field()
	blue_ground_attempted = scrapy.Field()
	blue_ground_landed = scrapy.Field()


class FighterItem(scrapy.Item):
	fighter_id = scrapy.Field()
	first_name = scrapy.Field()
	last_name = scrapy.Field()
	nickname = scrapy.Field()
	height = scrapy.Field()
	reach = scrapy.Field()
	weight = scrapy.Field()
	stance = scrapy.Field()
	dob = scrapy.Field()
	slpm = scrapy.Field()
	str_acc = scrapy.Field()
	sapm = scrapy.Field()
	str_def = scrapy.Field()
	td_avg = scrapy.Field()
	td_acc = scrapy.Field()
	td_def = scrapy.Field()
	sub_avg = scrapy.Field()
	wins = scrapy.Field()
	losses = scrapy.Field()
	draw = scrapy.Field()
	ncs = scrapy.Field()

"""READ THIS: the range of rows in FighterItem from 'slpm' onwards are 
values that are updated with each fight, so what you see at the time that 
you look at a fighter might not be the same example values in the "fighters" 
sheet of this document. That is ok.
"""
