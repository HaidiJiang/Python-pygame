import pygame
from pygame.locals import *
import sys
import random
#初始化
pygame.init()

#常量
num=3 #要创建3行3列的图
pintu=num*num
bgcolor=(224,255,255)
black=(0,0,0)
maxRandTime=100 #最多可以移动100次

'''
手动打乱图片顺序，并去掉一张图片
border=[0,6,5,3,4,2,1,7,-1]
if border[i]==-1:
	continue
	hangArea=int(border[i]/num)
	lieArea=int(border[i]%num)
'''

#加载图片
bgimg=pygame.image.load('../pic.jpg')
bgimgRect=bgimg.get_rect() #获取图片宽高
ceilwidth=int(bgimgRect.width/num) #获取每行的三张图片的宽度
ceilheight=int(bgimgRect.height/num) #获取每行的三张图片的高度

#设置窗口
screen=pygame.display.set_mode((bgimgRect.width,bgimgRect.height))#窗口宽高按照获取的图片宽高来取
pygame.display.set_caption('Hello 拼图')

#设置游戏盘
def newGameBoard():
	'''定义随机新生成的杂序图片'''
	board=[]
	for i in range(pintu):
		board.append(i) #将所有9块小图片添加进去
	blackCell=pintu-1 #blackCell 记录空白块，初始位置是pintu-1，8的位置，就是最后一个
	board[blackCell]=-1
	for i in range(maxRandTime):  #让图片移动，最多可移动100次
		direction=random.randint(0,3) #产生四个随机方向
		if(direction==0):
			blackCell=moveLeft(board,blackCell)
		elif(direction==1):
			blackCell=moveRight(board,blackCell)
		elif(direction==2):
			blackCell=moveUp(board,blackCell)
		elif(direction==3):
			blackCell=moveDown(board,blackCell)
	return board,blackCell

def moveLeft(board,blackCell):
	'''若空白图像块不在最右边，则将白块右边的图像块向左移动到白块位置'''
	if blackCell % num==num-1: #若空白块对3取模等于num-1，
		return blackCell
	board[blackCell+1],board[blackCell]=board[blackCell],board[blackCell+1]
	return blackCell+1
	
def moveRight(board,blackCell):
	'''若空白图像块不在最左边，则将白块左边的图像块向右移动到白块位置'''
	if blackCell % num==0:
		return blackCell
	board[blackCell-1],board[blackCell]=board[blackCell],board[blackCell-1]
	return blackCell-1

def moveUp(board,blackCell):
	'''若空白图像块不在最下边，则将白块下边的图像块向上移动到白块位置'''
	if blackCell>=pintu-num:
		return blackCell
	board[blackCell+num],board[blackCell]=board[blackCell],board[blackCell+num]
	return blackCell+num

def moveDown(board,blackCell):
	'''若空白图像块不在最上边，则将白块上边的图像块向下移动到白块位置'''
	if blackCell<num:
		return blackCell
	board[blackCell-num],board[blackCell]=board[blackCell],board[blackCell-num]
	return blackCell-num

board,blackCell=newGameBoard()#调用随机生成的杂序函数

def isFinished(board):
	'''设置当所有图块拼完结束'''
	for i in range(len(board)-1):
		if i!=board[i]:
			return False
	return True
finish=False





#主游戏运行
while True:
	screen.fill(bgcolor)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		if finish:
			continue
		if event.type==pygame.KEYDOWN: #按方向键可以移动
			if event.key==K_LEFT or event.key==ord('a'):
				blackCell=moveLeft(board,blackCell)
			if event.key==K_RIGHT or event.key==ord('d'):
				blackCell=moveRight(board,blackCell)
			if event.key==K_UP or event.key==ord('w'):
				blackCell=moveUp(board,blackCell)
			if event.key==K_DOWN or event.key==ord('s'):
				blackCell=moveDown(board,blackCell)
			
		if event.type==pygame.MOUSEBUTTONDOWN and event.button==1: #获取鼠标点击事件，当按键等于1左鼠标键时
			x,y=pygame.mouse.get_pos() #获取X,Y坐标数
			hang=int(x/ceilwidth) #每一个小图片的行位置等于X除以图片的宽
			lie=int(y/ceilheight) #每一个小图片的列位置等于Y除以图片的高
			index=lie*num+hang #每个图片的具体位置在几个，需要列的位置乘以3加上前面几个行
			if index==blackCell-1 or index==blackCell+1 or index==blackCell+num or index==blackCell-num: #当图片等于白块减一时或
				board[index],board[blackCell]=board[blackCell],board[index] #图片与白块交换
				blackCell=index #经过移动后，index变成白块，将白块的新值赋值给index
		
	if(isFinished(board)): #调用结束函数，让白块恢复成原本最后一块
		board[blackCell]=pintu-1
		finish=True
		
		
	for i in range(pintu): #循环pintu的块数，9
		hangDst=int(i/num) #每一行从0到8除以num3，0/3等于0、1/3等于0、2/3等于0所以在第一行0的位置上有三张图片，第二行和第三行依此类推
		lieDst=int(i%num) #每一列对3取模，除不尽的就是数的本身，0/3等于0、1/3等于1、2/3等于2、3/3等于0
		
		rectDst=pygame.Rect(lieDst*ceilwidth,hangDst*ceilheight,ceilwidth,ceilheight) #pygame.Rect 创建一个矩形区域
		#第一组参数0，0是图片显示在窗口的位置，第二组参数ceilwidth,ceilheight显示的区域
		if board[i]==-1: #将第8个小图设成-1后，当等于-1时，跳过不显示
			continue
		hangArea=int(board[i]/num)
		lieArea=int(board[i]%num)
		rectArea=pygame.Rect(lieArea*ceilwidth,hangArea*ceilheight,ceilwidth,ceilheight)
		#要显示的位置及区域：第一组参数0，0是图片显示在窗口的位置，第二组参数ceilwidth,ceilheight显示的区域
		
		screen.blit(bgimg,rectDst,rectArea)
	for i in range(num+1): #画横线
		pygame.draw.line(screen,black,(ceilwidth*i,0),(ceilwidth*i,bgimgRect.height))
		
	for i in range(num+1): #画竖线
		pygame.draw.line(screen,black,(0,ceilheight*i),(bgimgRect.width,ceilheight*i))

	pygame.display.update()
	
