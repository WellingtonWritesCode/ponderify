from math import floor
from PIL import Image, ImageDraw, ImageOps

ponder_mass = 16
ponder_mass_r = 6
ponder_mass_g = 9
ponder_mass_b = 12

def ponderify(file: str, save_path: str|None = None) -> None:
    im = Image.open(file)
    out = Image.new("RGB", ((floor(im.size[0]/ponder_mass)*ponder_mass), (floor(im.size[1]/ponder_mass)*ponder_mass)))
    ponder = Image.open("ponder.webp")
    width, height = im.size
    offset = floor(ponder_mass/2)
    for x in range(0, width, ponder_mass):
        for y in range(0, height, ponder_mass):
            pixel = im.getpixel((min(x+offset, width-1), min(y+offset, height-1)))
            average = sum(pixel)/765
            resized_ponder = ImageOps.fit(ponder, set_size(average), Image.Resampling.NEAREST)
            out.paste(resized_ponder, get_resized_pos(x, y, resized_ponder.size), resized_ponder)
    out.save([save_path, f"pondered {file}"][save_path is None])

def ponderify_rgb(file: str, save_path: str|None = None) -> None:
    im = Image.open(file)
    r, g, b = im.split()
    r = ponderify_single_color(r, ponder_mass_r)
    g = ponderify_single_color(g, ponder_mass_g)
    b = ponderify_single_color(b, ponder_mass_b)
    im = Image.merge("RGB", (r, g, b))
    im.save([save_path, f"rgb pondered {file}"][save_path is None])

def ponderify_single_color(im: Image.Image, local_ponder_mass) -> Image.Image:
    out = Image.new('L', ((floor(im.size[0]/ local_ponder_mass)*local_ponder_mass), (floor(im.size[1]/local_ponder_mass)*local_ponder_mass)))
    ponder = Image.open("ponder.webp")
    width, height = im.size
    offset = floor(local_ponder_mass/2)
    for x in range(0, width, local_ponder_mass):
        for y in range(0, height, local_ponder_mass):
            pixel = im.getpixel((min(x+offset, width-1), min(y+offset, height-1)))
            average = pixel/255
            resized_ponder = ImageOps.fit(ponder, set_size(average, local_ponder_mass), Image.Resampling.NEAREST)
            out.paste(resized_ponder, get_resized_pos(x, y, resized_ponder.size, local_ponder_mass), resized_ponder)
    return out

def set_size(average: float, local_ponder_mass: int = ponder_mass) -> tuple[int,int]:
    size = max(round(local_ponder_mass*average), 1)
    return size, size

def get_resized_pos(x :int, y: int, size: tuple, local_ponder_mass: int = ponder_mass) -> tuple[int, int, int, int]:
    offset = local_ponder_mass/2
    return floor(x+offset-size[0]/2), floor(y+offset-size[1]/2), floor(x+offset+size[0]/2), floor(y+offset+size[1]/2)

ponderify("bean.jpg")
ponderify_rgb("bean.jpg")