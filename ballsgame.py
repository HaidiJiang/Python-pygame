import pygame
import sys
from ballsgame_class import Ball
#建立两个圆
pygame.init()
screen=pygame.display.set_mode((700,700))
pygame.display.set_caption('balls')

bgcolor=(255,255,255)
speed=1
screen_rect=screen.get_rect()

def getball(balls):
	'''定义开始生成球时不重叠'''
	ball=Ball(screen_rect) #创建一个球，调用文件class
	for i in range(len(balls)):
		b_x=(balls[i].circle_point[0]-ball.circle_point[0])**2
		b_y=(balls[i].circle_point[1]-ball.circle_point[1])**2
		b_r=(balls[i].circle_radius*2)**2
		if (round((b_x+b_y),2)<=round(b_r,2)):  
			getball(balls)
			return
	balls.append(ball)

balls=[]
for i in range(5): #开始屏幕绘制5个球
	getball(balls)
	'''
	ball=Ball(screen_rect)
	balls.append(ball)
	'''

while True:
	screen.fill(bgcolor)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type==pygame.MOUSEBUTTONDOWN: 
			if event.button==1:  #当点击鼠标左键时添加一个球。调用函数
				getball(balls)
			elif event.button==3:  #当点击鼠标右键时删除一个球，删除列表中的元素
				balls.pop() 
				
		if event.type==pygame.KEYDOWN:  #当按下左方向键速度加快，右键减速
			if event.key==pygame.K_LEFT:
				speed+=0.1
			elif event.key==pygame.K_RIGHT:
				speed-=0.1	
	
	for i in range(len(balls)):
		pygame.draw.circle(screen,balls[i].circle_color,(int(balls[i].circle_point[0]),int(balls[i].circle_point[1])),balls[i].circle_radius) #将球绘制到屏幕上
		balls[i].circle_point[0]+=balls[i].circle_key[0]*speed #确定每个圆的新坐标x的值
		balls[i].circle_point[1]+=balls[i].circle_key[1]*speed #确定每个圆的新坐标y的值
			
		if balls[i].circle_point[0]+balls[i].circle_radius>=screen_rect.width:
			balls[i].circle_key[0]*=-1
			
		elif balls[i].circle_point[0]-balls[i].circle_radius<=0:
			balls[i].circle_key[0]*=-1

		if balls[i].circle_point[1]+balls[i].circle_radius>=screen_rect.height:
			balls[i].circle_key[1]*=-1
		
		elif balls[i].circle_point[1]-balls[i].circle_radius<=0:
			balls[i].circle_key[1]*=-1
			

	for j in range(len(balls)): #遍历圆的圆心
		for k in range((j+1),len(balls)): #遍历圆心，从j+1开始，就是j代表第一个圆，k代表第二圆
			b_x=(balls[j].circle_point[0]-balls[k].circle_point[0])**2 #求第一个圆心的x值减去第二个圆心的x值的平方
			b_y=(balls[j].circle_point[1]-balls[k].circle_point[1])**2 #求第一个圆心的y值减去第二个圆心的y值的平方
			b_r=(balls[i].circle_radius*2)**2 #求两个圆的半径的平方
			
			if (round((b_x+b_y),2)<=round(b_r,2)): #碰撞时向反方向走，交换值
				balls[j].circle_key[0],balls[k].circle_key[0]=balls[k].circle_key[0],balls[j].circle_key[0]
				balls[j].circle_key[1],balls[k].circle_key[1]=balls[k].circle_key[1],balls[j].circle_key[1]	
	
	
	pygame.display.update()
	


