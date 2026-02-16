from math import floor
from PIL import Image, ImageDraw, ImageOps

def ponderify(file: str, save_path: str|None = None) -> None:
    im = Image.open(file)
    ponder = Image.open("ponder.webp")
    draw = ImageDraw.Draw(im)
    width, height = im.size
    x_offset, y_offset = 16, 12
    for x in range(0, width, 30):
        for y in range(0, height, 30):
            pixel = im.getpixel((min(x+x_offset, width-1), min(y+y_offset, height-1)))
            average = sum(pixel)/765
            draw.rectangle((x,y,x+30,y+30), (0,0,0,255))
            resized_ponder = ImageOps.fit(ponder, set_size(average), Image.Resampling.NEAREST)
            im.paste(resized_ponder, get_resized_pos(x, y, resized_ponder.size), resized_ponder)
    im.save([save_path, f"pondered {file}"][save_path is None])

def set_size(average: float) -> tuple[int,int]:
    size = max(round(30*average), 1)
    return size, size

def get_resized_pos(x :int, y: int, size: tuple) -> tuple[int, int, int, int]:
    return floor(x+15-size[0]/2), floor(y+15-size[1]/2), floor(x+15+size[0]/2), floor(y+15+size[1]/2)

ponderify("bean.jpg")