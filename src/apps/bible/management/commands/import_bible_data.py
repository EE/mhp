import os
import tempfile

from PIL import Image

from django.core.files import File
from django.conf import settings
from django.core.management.base import BaseCommand

from src.apps.bible.models import Bible, BiblePage


BIBLES = [
    {
        'title': 'Biblia Leopolity',
        'slug': 'leopolity',
        'cover': settings.BASE_DIR.path('src', 'static', 'img', 'bible', 'cover', 'leopolity.jpg'),
        'data_folder_name': 'Biblia_Leopolity',
        'num_initial_pages_to_skip': 5
    },
    {
        'title': 'Biblia Sacra',
        'slug': 'sacra',
        'cover': settings.BASE_DIR.path('src', 'static', 'img', 'bible', 'cover', 'sacra.jpg'),
        'data_folder_name': 'Biblia_Sacra',
        'num_initial_pages_to_skip': 11
    },
    {
        'title': 'Nowy Testament Pana Naszego',
        'slug': 'nowy-testament-pana-naszego',
        'cover': settings.BASE_DIR.path('src', 'static', 'img', 'bible', 'cover', 'nowy_testament_pana_naszego.jpg'),
        'data_folder_name': 'Nowy_Testament_Pana_Naszego',
        'num_initial_pages_to_skip': 4
    }
]


def downscale_image(source_path):
    output_path = tempfile.mktemp()
    im = Image.open(source_path)
    im.thumbnail((1000, 1000), Image.ANTIALIAS)
    im.save(output_path, format='JPEG', quality=65)
    return output_path


class Command(BaseCommand):
    '''
    import bible data
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-directory',
            help='Image location')

    def handle(self, *args, **options):
        data_directory = options['data_directory']

        Bible.objects.all().delete()
        BiblePage.objects.all().delete()

        for bible in BIBLES:
            obj = Bible()
            obj.title = bible['title']
            obj.slug = bible['slug']
            obj.cover.save(
                '%s.jpg' % bible['slug'],
                File(open(downscale_image(str(bible['cover'])), 'rb')))
            obj.save()

            bible_image_path = os.path.join(
                data_directory,
                'Kultura_Cyfrowa',
                'Biblie_MHP',
                bible['data_folder_name'],
                'JPEG'
            )
            bible_images = os.listdir(bible_image_path)

            i = 1
            for image_name in sorted(bible_images)[bible['num_initial_pages_to_skip']:]:
                if image_name.endswith('.jpg'):
                    img = BiblePage()
                    img.bible = obj
                    img.ordering = i
                    img.image_small.save(
                        image_name,
                        File(open(downscale_image(os.path.join(bible_image_path, image_name)), 'rb'))
                    )
                    img.save()
                    i += 1
