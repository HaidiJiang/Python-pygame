class Settings():
	'''存储《外星人入侵》的所有设置类'''
	def __init__(self):
		'''初始化屏幕设置'''
		#屏幕设置
		self.screen_width=800
		self.screen_height=600
		self.bg_color=(230,230,230)
	
		#子弹设置
		#self.bullet_speed_factor=1
		self.bullet_width=7
		self.bullet_height=15
		self.bullet_color=(60,60,60)

		#外星人设置
		#self.alien_speed_factor=0.3
		self.fleet_drop_speed=4
		#self.fleet_direction=1
		self.ship_limit=3
		self.speedup_scale=1.1 #以什么样的速度加快游戏节奏
		self.score_scale=1.5 #分数以1.5倍增加
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		'''不退出程序，重新开始游戏充值状态'''
		self.ship_speed_factor=1.5
		self.bullet_speed_factor=1
		self.alien_speed_factor=1
		self.fleet_direction=1
		#1表示向右移动，-1表示向左移动
		
		#设置每个击落的外星人分值为50分
		self.alien_points=50
		
	def increase_speed(self):
		'''初始化随游戏进行而变化的设置'''
		self.ship_speed_factor*=self.speedup_scale
		self.bullet_speed_factor*=self.speedup_scale
		self.alien_speed_factor*=self.speedup_scale
		self.alien_points*=self.score_scale
