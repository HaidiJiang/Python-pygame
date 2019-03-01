import pygame
from pygame.locals import *
import sys
from settings import Settings
from ship import Ship
import game_functions as gf #引入函数包并附简化名字gf
from pygame.sprite import Group #Group用来存储精灵sprite
from geme_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	ai_settings=Settings() #创建一个设置类
	'''初始化游戏并创建屏幕对象'''
	pygame.init()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height)) #绘制窗口大小，调用settings文件包
	pygame.display.set_caption('Alien Invasion')
	ship=Ship(screen)#创建一个飞船对象
	
	#alien=Alien(ai_settings,screen)#创建单个外星人对象
	aliens=Group()#创建一个外星人群
	gf.create_fleet(ai_settings,screen,aliens,ship)
	
	stats=GameStats(ai_settings)
	
	bullets=Group()#创建一个用于存储子弹的编组
	play_button=Button(ai_settings,screen,'PLAY')
	
	sb=Scoreboard(ai_settings,screen,stats)#创建一个得分
	
	while True: #主程序运行
		
		gf.check_event(ai_settings,screen,sb,ship,bullets,aliens,stats,play_button) #调用函数用来实现退出事件
		if stats.game_active:
			gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens) #调用删除出屏幕子弹函数
			gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
		
		gf.update_screen(ai_settings,screen,sb,ship,bullets,aliens,play_button,stats)#调用绘制屏幕函数
run_game()
