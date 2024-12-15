import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment, User


class Command(BaseCommand):
    help = "Импорт данных из CSV в базу данных"

    def handle(self, *args, **kwargs):
        self.load_categories()
        self.load_genres()
        self.load_users()
        self.load_titles()
        self.load_genre_titles()
        self.load_reviews()
        self.load_comments()

    def load_categories(self):
        with open('static/data/category.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS("Категории загружены!"))

    def load_genres(self):
        with open('static/data/genre.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(self.style.SUCCESS("Жанры загружены!"))

    def load_users(self):
        with open('static/data/users.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row.get('bio', ''),
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', '')
                )
        self.stdout.write(self.style.SUCCESS("Пользователи загружены!"))

    def load_titles(self):
        with open('static/data/titles.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
        self.stdout.write(self.style.SUCCESS("Произведения загружены!"))

    def load_genre_titles(self):
        with open('static/data/genre_title.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    title.genre.add(genre)  # Добавляем жанр через ManyToMany
                except Title.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Произведение с id {row['title_id']} не найдено."))
                except Genre.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Жанр с id {row['genre_id']} не найден."))
        self.stdout.write(self.style.SUCCESS("Связи 'Жанры - Произведения' загружены!"))

    def load_reviews(self):
        with open('static/data/review.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                author = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    id=row['id'],
                    title=title,
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date']
                )
        self.stdout.write(self.style.SUCCESS("Отзывы загружены!"))

    def load_comments(self):
        with open('static/data/comments.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                review = Review.objects.get(id=row['review_id'])
                author = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    id=row['id'],
                    review=review,
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date']
                )
        self.stdout.write(self.style.SUCCESS("Комментарии загружены!"))
