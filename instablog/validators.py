from os.path import splitext
from PIL import Image
from django.core.exceptions import ValidationError


def jpeg_validator(field):
   extension = splitext(field.name)[-1].lower()
   if extension not in ('.jpg', '.jpeg'):
       raise ValidationError('only JPEG is allowed.')

   image = Image.open(field)
   if image.format != 'JPEG':
       raise ValidationError('only JPEG is allowed.')
