import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import string


class Captcha(object):
    # 生成几位的验证码
    number = 4
    # 验证码图片的宽度和高度
    size = (110, 38)
    # 验证码字体的大小
    fontsize = 25
    # 加入干扰线的条数
    line_number = 2
    # 构建一个验证码源文本
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(10)))

    # 用户绘制干扰线
    @classmethod
    def _gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls._gene_random_color(), width=2)

    # 用于绘制干扰点
    @classmethod
    # cls, draw, point_chance, width, height
    def _gene_points(cls, draw, width, height, rate):
        # chance = min(100, max(0, int(point_chance)))  #大小限制在0-100
        # for w in range(width):
        #     for h in range(height):
        #         tmp = random.randint(0, 100)
        #         if tmp > chance:
        #             draw.point((w, h), fill=cls._gene_random_color())
        # 因为width为图形验证码的宽，height为图形验证码的高，整个图都是由点组成的
        # 点的x坐标范围：[0, 图形的宽度], y的坐标范围：[0, 图形的高度], 这样就能遍历图像的每一个像素点
        # rate 用来控制点生成的概率，大约100个点有rate个点被选中
        # point方法用来画点，参数1：点的坐标， 参数2：点的颜色
        for x in range(width):
            for y in range(height):
                if random.randint(1, 100) <= rate:
                    draw.point((x, y), fill=cls._gene_random_color())

    # 随机生成颜色
    @classmethod
    def _gene_random_color(cls, start=0, end=255):
        random.seed()
        return (random.randint(start, end), random.randint(start, end), random.randint(start, end))

    # 随机选择一个字体
    @classmethod
    def _gene_random_font(cls):
        fonts = [
            "arial.ttf",
            "bahnschrift.ttf",
            "ebrima.ttf",
        ]
        font = random.choice(fonts)
        return f"utils/captcha/{font}"

    #     随机生成一个字符串（包括英文和数字）
    @classmethod
    def gene_text(cls, number):
        return ''.join(random.sample(cls.source, number))

    #     生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片的宽和高
        width, height = cls.size
        # 创建图片
        image = Image.new('RGBA', (width, height), cls._gene_random_color(0, 100))
        # 验证码字体
        font = ImageFont.truetype(cls._gene_random_font(), cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text(cls.number)
        # font.getsize(text)获取字体的尺寸
        # pillow 版本10 会报这个错误， AttributeError: 'FreeTypeFont' object has no attribute 'getsize'
        # 降低版本为9.5,但是安装一直报Read timed out,所以直接取消掉
        # font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text((30, 5), text, font=font,
                  fill=cls._gene_random_color(150, 255))
        # 绘制干扰线
        for x in range(0, cls.line_number):
            cls._gene_line(draw, width, height)
        # 绘制噪点
        cls._gene_points(draw, width, height, 20)
        # with open('captcha.png', 'wb') as fp:
        #     image.save(fp)
        return text, image

# if __name__ == '__main__':
#     Captcha.gene_graph_captcha()