from pelican import signals
from pelican.contents import Content
from PIL import Image
from bs4 import BeautifulSoup as bs
import cssutils, os, re

from pelican import signals
from pelican.readers import BaseReader

def cover_resize(cover_pictures_rel):
    quality_val = 60
    script_dir = os.path.dirname(__file__)
    print(cover_pictures_rel)
    script_dir_parent_1 = os.path.dirname(script_dir)
    print(script_dir_parent_1)
    script_dir_parent_2 = os.path.dirname(script_dir_parent_1)
    print(script_dir_parent_2)
    cover_pictures_abs = os.path.join(script_dir_parent_2, cover_pictures_rel)
    cover_pictures_abs_no_name = cover_pictures_abs.split("/")
    article_path = cover_pictures_abs_no_name[-2]
    print(article_path)
    cover_pictures_abs_no_name.pop()
    cover_pictures_abs_no_name = ('/').join(cover_pictures_abs_no_name)
    print(cover_pictures_abs)
    print(cover_pictures_abs_no_name)
    
    img = Image.open(cover_pictures_abs)
    img_width  = img.size[0]
    img_height = img.size[1]
    img_ratio = img_width / float(img_height)
    
    thumb_1x1_width = 680
    thumb_1x1_height = 680
    thumb_1x1_ratio = thumb_1x1_width / float(thumb_1x1_height)
    
    thumb_4x3_width = 906
    thumb_4x3_height = 680
    thumb_4x3_ratio = thumb_4x3_width / float(thumb_4x3_height)
    
    thumb_16x9_width = 1024
    thumb_16x9_height = 576
    thumb_16x9_ratio = thumb_16x9_width / float(thumb_16x9_height)
    
    thumb_ratio_dict = {thumb_1x1_ratio : ["1x1", thumb_1x1_width, thumb_1x1_height],
                        thumb_4x3_ratio : ["4x3", thumb_4x3_width, thumb_4x3_height],
                        thumb_16x9_ratio : ["16x9", thumb_16x9_width, thumb_16x9_height]
                        }

    for ratio in thumb_ratio_dict.iteritems():
        print(ratio)
        print(ratio[0])
        print(ratio[1])
        if img_ratio > ratio:
            new_width = int(ratio[0] * img_height)
            offset = (img_width - new_width) / 2
            resize = (offset, 0, img_width - offset, img_height)
        else:
            new_height = int(img_width / ratio[0])
            offset = (img_height - new_height) / 2
            resize = (0, offset, img_width, img_height - offset)

        thumb = img.crop(resize).resize((ratio[1][1], ratio[1][2]), Image.ANTIALIAS)
        thumb_name_theme_folder = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertina_" + ratio[1][0] + ".jpg"
        thumb.save(thumb_name_theme_folder)
    new_name = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertina.jpg"
    new_name_webp = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertina.webp"
    thumb_name = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/thumb.jpg"
    thumb_name_webp = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/thumb.webp"
    X1_name = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertinaX1.jpg"
    X1_name_webp = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertinaX1.webp"
    X2_name = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertinaX2.jpg"
    X2_name_webp = script_dir_parent_2 + "/" + "theme/dt/static/img/" + article_path + "/copertinaX2.webp"
    img.save(new_name_webp, 'webp', save_all=True, quality=quality_val)
    img.save(new_name, quality=quality_val)

    sizeX2 = 1400, 788
    sizeX2_img = img.resize(sizeX2, Image.ANTIALIAS)
    sizeX2_img.save(X2_name, "jpeg", optimize=True, quality=quality_val)
    sizeX2_img.save(X2_name_webp, "webp", optimize=True, quality=quality_val)

    sizeX1 = 700, 394
    sizeX1_img = img.resize(sizeX1, Image.ANTIALIAS)
    sizeX1_img.save(X1_name, "jpeg", optimize=True, quality=quality_val)
    sizeX1_img.save(X1_name_webp, "webp", optimize=True, quality=quality_val)

    size = 350, 198
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(thumb_name, quality=quality_val)
    img.save(thumb_name_webp, "webp", quality=quality_val)

# Create a new reader class, inheriting from the pelican.reader.BaseReader
class NewReader(BaseReader):
    enabled = True

    # The list of file extensions you want this reader to match with.
    # If multiple readers were to use the same extension, the latest will
    # win (so the one you're defining here, most probably).
    file_extensions = ['jpg']

    # You need to have a read method, which takes a filename and returns
    # some content and the associated metadata.
    def read(self, filename):
        print(filename)
        filename_encoded = filename.encode("utf-8")
        filename_splitted = filename_encoded.split("/")
        filename_file = filename_splitted[-1]
        filename_splitted.pop()
        filepath = ("/").join(filename_splitted)
        if filename_file == "copertina_raw.jpg":
            cover_resize(filename)
            new_name = filepath + "/copertina.jpg"
            print(new_name)
            os.rename(filename, new_name)
        else:
            print("copertina_raw not found")

def add_reader(readers):
    readers.reader_classes['jpg'] = NewReader

def register():
    signals.readers_init.connect(add_reader)