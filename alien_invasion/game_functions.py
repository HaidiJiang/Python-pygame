import pygame
import sys
from bullet import Bullet #引入子弹bullet文件包
from alien import Alien
from geme_stats import GameStats
from time import sleep

def check_keydown_events(ai_settings,screen,event,ship,bullets):
	'''当按下键盘时触发的事件'''
	if event.key==pygame.K_RIGHT:
		ship.move_right=True
	if event.key==pygame.K_LEFT:
		ship.move_left=True
	if event.key==pygame.K_SPACE: #按下空格键发射子弹
		fire_bullet(ai_settings,screen,ship,bullets)
		
def fire_bullet(ai_settings,screen,ship,bullets):
	'''发射多个子弹'''
	new_bullet=Bullet(ai_settings,screen,ship)
	bullets.add(new_bullet)
	
def check_keyup_events(event,ship):
	'''当按键弹起时'''
	if event.key==pygame.K_RIGHT:
		ship.move_right=False
	if event.key==pygame.K_LEFT:
		ship.move_left=False
		
def check_event(ai_settings,screen,sb,ship,bullets,aliens,stats,play_button):
	'''将退出事件封装函数，在主程序中调用'''
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit() 
		if event.type==pygame.KEYDOWN:
			check_keydown_events(ai_settings,screen,event,ship,bullets)
		if event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		if event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
			if button_clicked and stats.game_active==False: #stats.game_active==False当已经点击PLAY后再点击不会再重新开始
				#重置游戏设置
				ai_settings.initialize_dynamic_settings()
				#重置游戏统计信息
				stats.reset_stats()
				stats.game_active=True
				#清空外星人列表和子弹列表
				aliens.empty()
				bullets.empty()
				#创建一群新的外星人，并让飞船居中
				create_fleet(ai_settings,screen,aliens,ship)
				ship.center_ship()
				#隐藏光标
				pygame.mouse.set_visible(False)
				sb.prep_score()
				sb.show_score()
				sb.prep_ship()

def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens):
	'''将已出屏幕的子弹删除，当子弹与外星人碰撞时删除'''
	bullets.update() #引入子弹
	for bullet in bullets.copy(): #删除拷贝的，避免出错
		if bullet.rect.bottom<0:
			bullets.remove(bullet)
	#collsions=pygame.sprite.groupcollide(bullets,aliens,True,True)#sprite精灵中固有的碰撞方法，True,True当碰撞时删除
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	'''检查是否有子弹击中外星人，若有就删除子弹和外星人'''
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
	#collisions是一个字典，字典的键是子弹，它的值是外星人
	if collisions:
		for aliens in collisions.values(): #遍历字典的值-外星人
			stats.score+=ai_settings.alien_points*len(aliens)#得分等于50分乘以外星人的个数
			sb.prep_score() #调用更新函数
			check_high_score(stats,sb)
	
	if len(aliens)==0:
		#当外星人等于0时，删除现有子弹并新建一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings,screen,aliens,ship)
		stats.level+=1
		sb.prep_level()
	
def check_high_score(stats,sb):
	'''检查更新最高得分'''
	if stats.score>stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()	
	
			
def update_screen(ai_settings,screen,sb,ship,bullets,aliens,play_button,stats):
	'''将填充与投放到屏幕封装函数，在主程序中调用'''
	screen.fill(ai_settings.bg_color)
	aliens.draw(screen) #alien.blitme()单个显示外星人
	ship.blitme()
	ship.update()
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	pygame.display.flip()

def get_number_aliens_x(ai_settings,width):
	'''计算每行可容纳多少外星人'''
	available_space_x=ai_settings.screen_width-2*width
	number_aliens_x=int(available_space_x/(2*width))
	return number_aliens_x

def get_num_rows(ai_settings,ship_height,alien_height):
	'''计算屏幕可容纳多少行外星人'''
	available_space_y=ai_settings.screen_height-3*alien_height-ship_height
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(ai_settings,screen,aliens,row_number,alien_number):
	'''创建一个外星人并放入当前行'''
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)
	
def create_fleet(ai_settings,screen,aliens,ship):
	'''建立一个外星人群'''
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_num_rows(ai_settings,ship.rect.height,alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,row_number,alien_number)
	
def check_fleet_edges(ai_settings,aliens):
	'''检测边缘，到屏幕边缘时调用change_fleet_direction改变移动方向'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
		
def change_fleet_direction(ai_settings,aliens):
	'''改变外星人的移动方向，垂直移动'''
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
	stats.ships_life-=1
	sb.prep_ship()
	if stats.ships_life>0:
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		#创建一群新的外星人并将飞船放在屏幕底部中央
		create_fleet(ai_settings,screen,aliens,ship)
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)#当游戏结束时显示光标
		stats.reset_stats()
		sb.show_score()
		

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
	'''检测每次外星人位于屏幕底部时'''
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>screen_rect.bottom:
			ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
			break


		
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
	'''将外星人绘制到屏幕'''
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
	check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
