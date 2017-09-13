from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype("RobotoCondensed-Regular.ttf", 10)

for letter in range(ord('A'), ord('Z') + 1):
    image = Image.new('RGBA', [10, 10], (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((2, 0), chr(letter), font=font, fill=(0, 0, 0, 255))
    eject = 'll/' + chr(letter) + '.png'
    image.save(eject)

# image = Image.new('RGBA', [10, 10], (255, 255, 255, 255))
# draw = ImageDraw.Draw(image)
# draw.text((0, 0), "Y", font=font, fill=(0, 0, 0, 255))
# eject = 'll/Y.png'
# image.save(eject)

# image = Image.new('RGBA', [10, 10], (255, 255, 255, 255))
# draw = ImageDraw.Draw(image)
# draw.text((0, 0), "M", font=font, fill=(0, 0, 0, 255))
# eject = 'll/M.png'
# image.save(eject)

# image = Image.new('RGBA', [10, 10], (255, 255, 255, 255))
# draw = ImageDraw.Draw(image)
# draw.text((0, 0), "W", font=font, fill=(0, 0, 0, 255))
# eject = 'll/W.png'
# image.save(eject)