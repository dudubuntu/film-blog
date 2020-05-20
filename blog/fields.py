from django.db.models.fields.files import ImageField, ImageFieldFile

from PIL import Image
import os
import time


def _add_thumb(s: str):
    fields = s.split('.')
    fields.insert(-1, 'thumb')
    if fields[-1] not in ['jpeg', 'jpg']:
        fields[-1] = 'jpg'
    return '.'.join(fields)


# def _generate_name(name: str, is_thumb: bool):
#     if name is None:
#         name = ''
#     return name + str(int(time.time()))


class ThumbnailImageFieldFile(ImageFieldFile):
    def get_thumb_url(self):
        return _add_thumb(self.url)
    thumb_url = property(get_thumb_url)

    def get_thumb_path(self):
        return _add_thumb(self.path)
    thumb_path = property(get_thumb_path)

    def save(self, ignore, content, save=True):
        super(ThumbnailImageFieldFile, self).save(self.name, content, save)
        img = Image.open(self.path)
        img.thumbnail((self.field.thumb_width, self.field.thumb_height), Image.ANTIALIAS)
        img.save(self.thumb_path, 'JPEG')

    def delete(self, save=False):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_height=128, thumb_width=128, name=None, *args, **kwargs):
        self.name = name
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)