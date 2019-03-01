import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	'''初始化飞船并设置其初始位置'''
	def __init__(self,screen):
		super().__init__()
		self.screen=screen
		self.move_right=False
		self.move_left=False
		self.image=pygame.image.load('ship.png') #加载飞船图像并获取外接矩形
		self.rect=self.image.get_rect()
		self.screen_rect=self.screen.get_rect()
		self.rect.centerx=self.screen_rect.centerx #将飞船放在屏幕底部中央
		self.rect.bottom=self.screen_rect.bottom
		
	def blitme(self):
		'''在指定位置绘制飞船'''
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		'''定义飞船左右移动'''
		if self.move_right and self.rect.centerx<self.screen_rect.right-self.rect.width/2:
			self.rect.centerx+=1
		elif self.move_left and self.rect.centerx>self.rect.width/2:
			self.rect.centerx-=1
	def center_ship(self):
		'''新一轮重新将飞船放在屏幕底部中央'''
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom
