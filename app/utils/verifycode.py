# _*_ coding:utf-8 _*_
import random
import string
from PIL import Image, ImageDraw, ImageFont


def rndColor():
    '''
    随即颜色
    :return: RGB(int, int, int)
    '''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def gene_text():
    '''
    生成4位随机验证码
    '''
    return ''.join(random.sample(string.ascii_letters+string.digits, 4))

def draw_lines(draw, num, width, height):
    ''' 划线 '''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill=rndColor(), width=1)

def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    # 图片大小 120*50
    width, height = 120, 50
    #新图片对象,白底
    im = Image.new('RGB',(width, height),'white')
    # 字体
    font = ImageFont.truetype('app/static/fonts/arial.ttf', 40)
    #draw 对象
    draw = ImageDraw.Draw(im)
    #绘制字符串
    for item in range(4):
        draw.text((5+random.randint(-3,3)+23*item,5+random.randint(-3,3)), text=code[item], fill=rndColor(), font=font)
    # draw_lines(draw, 30, random.randint(0, width),
    #            random.randint(0, height))  # 这一步自己添加的需要验证也可以给参数（draw, 2 , width, height）
    draw_lines(draw, 30, width,
               height)
    return im, code

