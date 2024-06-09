from PIL import Image, ImageDraw, ImageFont
img = Image.open("Taylor-Swift.jpg")
draw = ImageDraw.Draw(img)

txt = "Hello,\nPablo"
font = ImageFont.truetype('OpenSans-Bold.ttf',50)
draw.text((50, 50), txt, font = font, fill=(0, 0, 0))
img.save('hello-Taylor.png')
img.show()