#!/usr/bin/python

import argparse
import os
from PIL import Image


#create iOS icon files
def ios(image, dst):
    name = [
        "iTunesArtwork", "iTunesArtwork@2x",
        "Icon-60@2x.png", "Icon-60@3x.png",
        "Icon-76.png", "Icon-76@2x.png", "Icon-83.5@2x.png",
        "Icon-Small-40.png", "Icon-Small-40@2x.png", "Icon-Small-40@3x.png",
        "Icon-Small.png", "Icon-Small@2x.png", "Icon-Small@3x.png"
    ]

    sizes = [
        512, 1024,
        120, 180,
        76, 152, 167,
        40, 80, 120,
        29, 58, 87
    ]

    for i in xrange(len(sizes)):
        icon = image
        icon = icon.resize((sizes[i], sizes[i]), Image.BILINEAR)
        icon.save(dst + "/" + name[i], "PNG")

#create Android icon files
def android(image, dst):
    folders = [
        "drawable-ldpi", "drawable-mdpi", "drawable-hdpi",
        "drawable-xhdpi", "drawable-xxhdpi", "drawable-xxxhdpi"
    ]

    sizes = [
        36, 48, 72,
        96, 144, 192
    ]

    for i in xrange(len(sizes)):
        icon = image
        icon = icon.resize((sizes[i], sizes[i]), Image.BILINEAR)
        path = dst + "/" + folders[i]
        if not os.path.exists(path):
            os.mkdir(path)
        icon.save(path + "/ic_launcher.png", "PNG")


def normalize_src(src, mask):
    try:
        image = Image.open(src)
    except IOError:
        print "Icon is not a png file"
        exit()

    if image.format != "PNG":
        print "Icon is not a png file"
        exit()

    width, height = image.size
    if width != height:
        print "Icon is not a 'Square'"
        exit()

    if mask:
        if width > 1500 or width < 1024:
            image = image.resize((1500, 1500), Image.BILINEAR)
            width = 1500
            height = 1500

        #replace transparent to white
        pixals = image.load()
        for h in xrange(height):
            for w in xrange(width):
                if pixals[w, h][3] is 0:
                    pixals[w, h] = (255, 255, 255, 255)

        #add fillet
        mask = Image.open('mask.png')
        mask = mask.resize((width, height), Image.BILINEAR)
        r, g, b, a = mask.split()
        image.putalpha(a)
    return image


def check(platform, src, dst, mask):
    if platform != "Android" and platform != "iOS":
        print "Platform must be Android or iOS"
        exit()
    if not os.path.isfile(src) or src is None:
        print "Icon file is not exist"
        exit()
    if not os.path.exists(dst) or dst is None:
        print "Destination folder is not exist"
        exit()

    image = normalize_src(src, mask)
    if platform == "Android":
        android(image, dst)
    elif platform == "iOS":
        ios(image, dst)


def main():
    parser = argparse.ArgumentParser(description="Android iOS Icon Maker")
    parser.add_argument("-p", "--platform", help="icon platform must be Android or iOS", dest="platform",
                        choices=["Android", "iOS"], default=None)
    parser.add_argument("-i", "--icon", help="icon file", dest="icon", default=None)
    parser.add_argument("-d", "--destination", help="destination folder", dest="dst", default=None)
    parser.add_argument("-m", "--mask", help="Need fillet mask", dest="mask", action="store_true", default=False)
    args = parser.parse_args()
    check(args.platform, args.icon, args.dst, args.mask)

if __name__ == '__main__':
    main()
