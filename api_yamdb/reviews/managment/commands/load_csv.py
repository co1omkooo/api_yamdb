import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.models import User


class Command(BaseCommand):
    help = 'Помогает загрузить данные с csv-файлов.'

    def handle(self, *args, **kwargs):
        CSV_DIR = Path('static', 'data')
        DATA = (
            ('category.csv', Category, {}),
            ('genre.csv', Genre, {}),
            ('users.csv', User, {}),
            ('titles.csv', Title, {'category': 'category_id'}),
            ('genre_title.csv', Title.genre.through, {}),
            ('review.csv', Review, {'author': 'author_id'}),
            ('comments.csv', Comment, {'author': 'author_id'}),
        )
        for csv_file, model, replace in DATA:
            self.stdout.write(f'Начало импорта из файла {csv_file}')
            try:
                with open(
                    Path(CSV_DIR, csv_file),
                    mode='r',
                    encoding='utf8',
                ) as csv_file_path:
                    reader = csv.DictReader(csv_file_path)
                    counter = 0
                    objects_to_create = []
                for row in reader:
                    counter += 1
                    args = dict(**row)
                    if replace:
                        for old, new in replace.items():
                            args[new] = args.pop(old)
                    objects_to_create.append(model(**args))
                model.objects.bulk_create(
                    objects_to_create,
                    ignore_conflicts=True,
                )
                self.stdout.write(
                    f'Добавлено объектов: {len(objects_to_create)}; '
                    f'строк в документе: {counter}'
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error processing file {csv_file_path}: {e}'
                    )
                )
                error_occurred = True

        if not error_occurred:
            self.stdout.write(
                self.style.SUCCESS('<===SUCCESSFULLY LOADED DATA===>')
            )
        else:
            self.stdout.write(
                self.style.ERROR('<===FAILED TO LOAD DATA===>')
            )
