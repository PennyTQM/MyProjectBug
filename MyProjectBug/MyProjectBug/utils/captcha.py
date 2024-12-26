from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


# 生成验证码的函数
def generate_captcha():
    # 创建一个新的白色图像
    image = Image.new('RGB', (120, 30), color='white')
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(image)
    # 定义验证码的字符集
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    # 生成随机验证码
    captcha_text = ''.join(random.choice(letters) for i in range(5))
    # 字体文件路径
    font = ImageFont.truetype('Myproject/arial.ttf', 20)
    # 绘制验证码文本
    for i in range(len(captcha_text)):
        draw.text((20 + i * 13, 5), captcha_text[i], font=font, fill=(0, 0, 255))

    # 为图像添加噪声干扰
    def create_noise(image):
        draw = ImageDraw.Draw(image)
        for i in range(5):
            x1, x2 = random.randint(0, 200), random.randint(0, 200)
            y1, y2 = random.randint(0, 40), random.randint(0, 40)
            draw.line((x1, y1, x2, y2), fill=100)

    create_noise(image)
    # 应用模糊滤镜
    image = image.filter(ImageFilter.BLUR)
    # 返回验证码文本和图像
    return captcha_text, image


# 使用函数生成验证码
if __name__ == '__main__':
    captcha_text, captcha_image = generate_captcha()
    # 保存验证码图像
    captcha_image.save('captcha.png')