
import os
import time
from random import choice, randint, randrange

from PIL import Image, ImageDraw, ImageFont

# 验证码图片文字的字符集
characters = '拾伍佰正仟万捌贰整陆玖圆叁零角分肆柒亿壹元'

def selectedCharacters(length):
    result = ''.join(choice(characters) for _ in range(length))
    return result


def getColor():
    r = randint(0, 100)
    g = randint(0, 100)
    b = randint(0, 100)
    return (r, g, b)


def main(size=(200, 100), characterNumber=6, bgcolor=(255, 255, 255)):
    # 创建空白图像和绘图对象
    imageTemp = Image.new('RGB', size, bgcolor)
    draw01 = ImageDraw.Draw(imageTemp)

    # 生成并计算随机字符串的宽度和高度
    text = selectedCharacters(characterNumber)
    print(text)
    font = ImageFont.truetype(font_path, 40)
    width, height = draw01.textsize(text, font)
    if width + 2 * characterNumber > size[0] or height > size[1]:
        print('尺寸不合法')
        return

    # 绘制随机字符串中的字符
    startX = 0
    widthEachCharater = width // characterNumber
    for i in range(characterNumber):
        startX += widthEachCharater + 1
        position = (startX, (size[1] - height) // 2)
        draw01.text(xy=position, text=text[i], font=font, fill=getColor())

    # 对像素位置进行微调，实现扭曲的效果
    imageFinal = Image.new('RGB', size, bgcolor)
    pixelsFinal = imageFinal.load()
    pixelsTemp = imageTemp.load()
    for y in range(size[1]):
        offset = randint(-1, 0)
        for x in range(size[0]):
            newx = x + offset
            if newx >= size[0]:
                newx = size[0] - 1
            elif newx < 0:
                newx = 0
            pixelsFinal[newx, y] = pixelsTemp[x, y]

    # 绘制随机颜色随机位置的干扰像素
    draw02 = ImageDraw.Draw(imageFinal)
    for i in range(int(size[0] * size[1] * 0.07)):
        draw02.point((randrange(0, size[0]), randrange(0, size[1])), fill=getColor())

    # 保存并显示图片
    imageFinal.save("dataset/images/%d_%s.jpg" % (round(time.time() * 1000), text))

if __name__ == '__main__':
    if not os.path.exists('dataset/images'):
        os.makedirs('dataset/images')

    # font_path = "font/鸿雷板书简体-Regular.ttf"
    # for _ in range(1):
