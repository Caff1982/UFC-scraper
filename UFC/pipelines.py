# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class UfcPipeline(object):

	def __init__(self):
		self.create_connection()
		self.create_tables()

	def create_connection(self):
		self.conn = sqlite3.connect('data.db')
		self.curr = self.conn.cursor()

	def create_tables(self):
		self.curr.execute("""DROP TABLE IF EXISTS EVENTS""")
		self.curr.execute("""CREATE TABLE EVENTS(
							PRIMARY_KEY INT,
							DATE TEXT,
							LOCATION TEXT,
							ATTENDANCE INT,
							NAME TEXT,
							FIGHT_COUNT INT
						)""")
		self.curr.execute("""DROP TABLE IF EXISTS FIGHTS""")
		self.curr.execute("""CREATE TABLE FIGHTS(
							FIGHT_ID INT,
							EVENT_ID INT,
							BOUT_ORDER INT,
							WEIGHT_CLASS TEXT,
							TITLE_FIGHT INT,
							RED_FIGHTER_ID TEXT,
							BLUE_FIGHTER_ID TEXT,
							RESULT TEXT,
							END_METHOD TEXT,
							END_DETAILS TEXT,
							END_ROUND INT,
							END_TIME TEXT,
							TIME_FORMAT TEXT,
							REFEREE TEXT
						)""")
		self.curr.execute("""DROP TABLE IF EXISTS ROUNDS""")
		self.curr.execute("""CREATE TABLE ROUNDS(
							FIGHT_ID INT,
							EVENT_ID INT,
							ROUND_COUNT INT,
							RED_KD INT,
							RED_SIG_STR_ATTEMPTED INT,
							RED_SIG_STR_LANDED INT,
							RED_SIG_STR_PERC REAL,
							RED_TOTAL_STR_ATTEMPTED INT,
							RED_TOTAL_STR_LANDED INT,
							RED_TOTAL_STR_PERC REAL,
							RED_TD_LANDED INT,
							RED_TD_ATTEMPTED INT,
							RED_TD_PERC REAL,
							RED_SUB_ATTEMPTED INT,
							RED_PASS INT,
							RED_REV INT,
							RED_HEAD_LANDED INT,
							RED_LEG_ATTEMPTED INT,
							RED_LEG_LANDED INT,
							RED_DISTANCE_ATTEMPTED INT,
							RED_DISTANCE_LANDED INT,
							RED_CLINCH_ATTEMPTED INT,
							RED_CLINCH_LANDED INT,
							RED_GROUND_ATTEMPTED INT,
							RED_GROUND_LANDED INT,
							BLUE_KD INT,
							BLUE_SIG_STR_ATTEMPTED INT,
							BLUE_SIG_STR_LANDED INT,
							BLUE_SIG_STR_PERC REAL,
							BLUE_TOTAL_STR_ATTEMPTED INT,
							BLUE_TOTAL_STR_LANDED INT,
							BLUE_TOTAL_STR_PERC REAL,
							BLUE_TD_LANDED INT,
							BLUE_TD_ATTEMPTED INT,
							BLUE_TD_PERC REAL,
							BLUE_SUB_ATTEMPTED INT,
							BLUE_PASS INT,
							BLUE_REV INT,
							BLUE_HEAD_LANDED INT,
							BLUE_LEG_ATTEMPTED INT,
							BLUE_LEG_LANDED INT,
							BLUE_DISTANCE_ATTEMPTED INT,
							BLUE_DISTANCE_LANDED INT,
							BLUE_CLINCH_ATTEMPTED INT,
							BLUE_CLINCH_LANDED INT,
							BLUE_GROUND_ATTEMPTED INT,
							BLUE_GROUND_LANDED INT
						)""")
		self.curr.execute("""DROP TABLE IF EXISTS FIGHTERS""")
		self.curr.execute("""CREATE TABLE FIGHTERS(
							FIGHTER_ID TEXT,
							FIRST_NAME TEXT,
							LAST_NAME TEXT,
							NICK_NAME TEXT, 
							HEIGHT INT,
							REACH INT,
							WEIGHT INT,
							STANCE TEXT,
							DOB TEXT,
							SLPM REAL,
							STR_ACC REAL,
							SAPM REAL,
							STR_DEF REAL,
							TD_AVG REAL,
							TD_ACC REAL,
							TD_DEF REAL,
							SUB_AVG REAL,
							WINS INT,
							LOSSES INT,
							DRAW INT,
							NCS INT
						)""")

	def process_item(self, item, spider):
		if 'location' in item.keys():
			self.store_event(item)
		elif 'referee' in item.keys():
			self.store_fight(item)
		elif 'red_kd' in item.keys():
			self.store_round(item)
		elif 'fighter_id' in item.keys():
			self.store_fighter(item)
		return item

	def store_event(self, item):
		self.curr.execute("""INSERT INTO EVENTS VALUES (?,?,?,?,?,?)""",(
							item['primary_key'],
							item['date'],
							item['location'],
							item['attendance'],
							item['name'],
							item['fight_count']
							))
		self.conn.commit()

	def store_fight(self, item):
		self.curr.execute("""INSERT INTO FIGHTS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
							item['fight_id'],
							item['event_id'],
							item['bout_order'],
							item['weight_class'],
							item['title_fight'],
							item['red_fighter_id'],
							item['blue_fighter_id'],
							item['result'],
							item['end_method'],
							item['end_details'],
							item['end_round'],
							item['end_time'],
							item['time_format'],
							item['referee']
							))
		self.conn.commit()

	def store_round(self, item):
		self.curr.execute("""INSERT INTO ROUNDS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
							item['event_id'],
							item['fight_id'],
							item['round_count'],
							item['red_kd'],
							item['red_sig_str_attempted'],
							item['red_sig_str_landed'],
							item['red_sig_str_perc'],
							item['red_total_str_attempted'],
							item['red_total_str_landed'],
							item['red_total_str_perc'],
							item['red_td_landed'],
							item['red_td_attempted'],
							item['red_td_perc'],
							item['red_sub_attempted'],
							item['red_pass'],
							item['red_rev'],
							item['red_head_landed'],
							item['red_leg_attempted'],
							item['red_leg_landed'],
							item['red_distance_attempted'],
							item['red_distance_landed'],
							item['red_clinch_attempted'],
							item['red_clinch_landed'],
							item['red_ground_attempted'],
							item['red_ground_landed'],
							item['blue_kd'],
							item['blue_sig_str_attempted'],
							item['blue_sig_str_landed'],
							item['blue_sig_str_perc'],
							item['blue_total_str_attempted'],
							item['blue_total_str_landed'],
							item['blue_total_str_perc'],
							item['blue_td_landed'],
							item['blue_td_attempted'],
							item['blue_td_perc'],
							item['blue_sub_attempted'],
							item['blue_pass'],
							item['blue_rev'],
							item['blue_head_landed'],
							item['blue_leg_attempted'],
							item['blue_leg_landed'],
							item['blue_distance_attempted'],
							item['blue_distance_landed'],
							item['blue_clinch_attempted'],
							item['blue_clinch_landed'],
							item['blue_ground_attempted'],
							item['blue_ground_landed']
							))
		self.conn.commit()

	def store_fighter(self, item):
		self.curr.execute("""INSERT INTO FIGHTERS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
							item['fighter_id'],
							item['first_name'],
							item['last_name'],
							item['nickname'],
							item['height'],
							item['reach'],
							item['weight'],
							item['stance'],
							item['dob'],
							item['slpm'],
							item['str_acc'],
							item['sapm'],
							item['str_def'],
							item['td_avg'],
							item['td_acc'],
							item['td_def'],
							item['sub_avg'],
							item['wins'],
							item['losses'],
							item['draw'],
							item['ncs']
							))
		self.conn.commit()


