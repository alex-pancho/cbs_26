## Заняття 40. Моделі, міграції та Django ORM

### Про що це заняття
Сьогодні ми навчимося описувати дані в Django, зберігати їх у базі даних і працювати з ними через зручний Python-інтерфейс. Для цього ми використаємо **моделі**, **міграції** та **ORM**.

### Що таке модель
Модель у Django — це Python-клас, який описує таблицю в базі даних.  
Кожне поле моделі — це окрема колонка таблиці.

Наприклад, якщо ми хочемо зберігати категорії курсів, можна створити таку модель:

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
```

Тут:
- `Category` — це назва моделі;
- `name` — короткий текст;
- `description` — довший текст;
- `__str__()` потрібен, щоб об’єкт красиво відображався в адмінці та консолі.

### Поля моделі
У моделях Django найчастіше використовують такі поля:
- `CharField` — для короткого тексту;
- `TextField` — для довгого тексту;
- `IntegerField` — для цілих чисел;
- `BooleanField` — для значень `True` або `False`;
- `DateField` і `DateTimeField` — для дат і часу;
- `ForeignKey` — для зв’язку з іншою моделлю.

Приклад моделі статті:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

У цьому прикладі:
- `title` — заголовок;
- `content` — текст статті;
- `is_published` — чи опублікована стаття;
- `created_at` — дата створення.

### Що таке міграції
Коли ми змінюємо модель, Django не змінює базу даних сам по собі.  
Для цього потрібні **міграції** — спеціальні файли, які описують зміни структури бази даних.

Основні команди:

```bash
python manage.py makemigrations
python manage.py migrate
```

Що вони роблять:
- `makemigrations` створює файл із описом змін;
- `migrate` застосовує ці зміни до бази даних.

Простими словами:
1. Ми змінюємо модель.
2. Django “записує”, що саме змінилося.
3. Потім ці зміни застосовуються до таблиць у базі даних.

### Що таке ORM
ORM — це інструмент, який дозволяє працювати з базою даних як із Python-об’єктами.  
Завдяки ORM ми можемо створювати, читати, змінювати та видаляти записи без написання SQL вручну.

Наприклад:

```python
category = Category.objects.create(name="Django", description="Уроки з Django")
```

Цей код створює новий запис у таблиці `Category`.

Отримати всі записи можна так:

```python
categories = Category.objects.all()
```

Знайти один запис:

```python
category = Category.objects.get(id=1)
```

Відфільтрувати записи:

```python
categories = Category.objects.filter(name__icontains="python")
```

### Що таке QuerySet
QuerySet — це набір об’єктів, який повертає Django після запиту до бази даних.  
Його можна сортувати, фільтрувати, об’єднувати та комбінувати.

Приклад:

```python
articles = Article.objects.filter(is_published=True).order_by("-created_at")
```

Тут ми:
- беремо тільки опубліковані статті;
- сортуємо їх від нових до старих.

Ще кілька корисних прикладів:

```python
Article.objects.count()
Article.objects.first()
Article.objects.last()
Article.objects.exists()
```

### Зв’язки між моделями
У реальних проєктах одна таблиця часто пов’язана з іншою. Django підтримує кілька типів зв’язків.

#### One-to-one
Один запис у першій таблиці відповідає одному запису в іншій.

Приклад:

```python
class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
```

Тут один користувач має один профіль.

#### Many-to-one
Багато записів належать одному запису іншої таблиці.

Приклад:

```python
class Article(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    title = models.CharField(max_length=200)
```

Тут багато статей можуть належати одній категорії.

#### Many-to-many
Один запис може бути пов’язаний із багатьма іншими, і навпаки.

Приклад:

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name="articles")
```

Тут одна стаття може мати багато тегів, а один тег може належати багатьом статтям.

### Практика на занятті
На практиці ми створимо кілька моделей для курсового проєкту. Наприклад:
- `Category`;
- `Course`;
- `Lesson`.

Приклад готового коду:

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
```

Після створення моделей виконаємо міграції:

```bash
python manage.py makemigrations
python manage.py migrate
```

Після цього можна працювати з базою даних через ORM:

```python
category = Category.objects.create(name="Web Development")

course = Course.objects.create(
    title="Django Basics",
    description="Початковий курс з Django",
    category=category
)

Lesson.objects.create(course=course, title="Вступ до Django", order=1)
Lesson.objects.create(course=course, title="Створення моделі", order=2)
```

### Як читати й змінювати дані
Отримати всі курси:

```python
courses = Course.objects.all()
```

Знайти курси певної категорії:

```python
web_courses = Course.objects.filter(category__name="Web Development")
```

Оновити запис:

```python
course.title = "Django for Beginners"
course.save()
```

Видалити запис:

```python
course.delete()
```

### Що потрібно запам’ятати
Модель описує структуру даних.  
Міграція переносить зміни з коду в базу даних.  
ORM дозволяє працювати з даними як із Python-об’єктами.


---

## Розширена теоретична частина

### Метаклас `Meta` — налаштування моделі

У моделі можна використовувати вложений клас `Meta` для налаштувань.

Найкорисніші опції:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Українська назва для одного об'єкта (в адмінці)
        verbose_name = "Стаття"
        
        # Українська назва для множини
        verbose_name_plural = "Статті"
        
        # Порядок за замовчуванням
        ordering = ["-created_at"]  # від нових до старих
        
        # Індекс для швидкого пошуку
        indexes = [models.Index(fields=["created_at"])]
```

**Залежно від потреб:**
- `ordering` — як сортувати об'єкти за замовчуванням
- `verbose_name` — як звертатися до моделі в адмінці
- `unique_together` — комбінація полів повинна бути унікальною
- `db_table` — назва таблиці в БД (якщо відрізняється від імені моделі)

### Методи моделі — коли використовувати

Крім `__str__()`, у моделі можна створити власні методи:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    # Метод для додавання перегляду
    def increment_views(self):
        self.views += 1
        self.save()
    
    # Метод для отримання короткого вурізу тексту
    def get_preview(self, length=100):
        return self.content[:length] + "..."
    
    # Властивість (property) — звертаємося як до атрибута
    @property
    def is_popular(self):
        return self.views > 1000
```

Використання:

```python
article = Article.objects.get(id=1)
article.increment_views()
print(article.get_preview())
print(article.is_popular)  # True або False
```

### Параметри полів — choices, default, null, blank

Крім типу поля, є додаткові параметри, які контролюють поведінку:

```python
class Task(models.Model):
    # Вибір зі списку (choices)
    STATUS_CHOICES = [
        ("new", "Нове"),
        ("in_progress", "У процесі"),
        ("done", "Готово"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    
    # Текст, який опціональний
    description = models.TextField(blank=True, null=True)
    
    # Число з нулевим значенням за замовчуванням
    priority = models.IntegerField(default=0)
    
    # Email, унікальний для всіх записів
    email = models.EmailField(unique=True)
    
    # Поле, яке оновлюється автоматично
    updated_at = models.DateTimeField(auto_now=True)
```

**Що значить:**
- `default` — значення за замовчуванням при створенні запису
- `blank=True` — поле опціональне при заповненні форми
- `null=True` — поле може бути NULL у базі даних
- `unique=True` — всі значення в цьому полі унікальні
- `auto_now_add=True` — встановлюється при створенні один раз
- `auto_now=True` — оновлюється кожний раз при збереженні

### Реєстрація моделей в адмін-панелі

Щоб модель відображалася в Django admin, потрібно зареєструвати її:

```python
# admin.py
from django.contrib import admin
from .models import Category, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "article_count"]
    search_fields = ["name"]
    
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Які поля показувати у списку
    list_display = ["title", "category", "is_published", "created_at"]
    
    # По яким полям шукати
    search_fields = ["title", "content"]
    
    # По яким полям фільтрувати
    list_filter = ["is_published", "category", "created_at"]
    
    # Порядок полів у формі редагування
    fieldsets = (
        ("Основна інформація", {
            "fields": ("title", "category", "content")
        }),
        ("Видимість", {
            "fields": ("is_published",)
        }),
    )
    
    # Лише для читання
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Comment)  # Простий варіант без налаштувань
```

### Фільтрування та пошук — QuerySet операції

Django ORM надає багато способів для роботи з даними:

```python
# Базовий пошук
Article.objects.get(id=1)  # Один запис (помилка якщо не знайдено)
Article.objects.filter(category=1)  # Всі записи, які відповідають

# Множинні умови
Article.objects.filter(is_published=True, category__id=1)

# Виключення
Article.objects.exclude(is_published=False)  # Все крім невпубліковано

# Пошук в тексті
Article.objects.filter(title__icontains="Django")  # Містить
Article.objects.filter(title__startswith="Django")  # Починається з
Article.objects.filter(created_at__year=2024)  # За роком

# Пошук в пов'язаних об'єктах (через ForeignKey)
Article.objects.filter(category__name="Web Development")

# Сортування
Article.objects.order_by("created_at")  # Від старих
Article.objects.order_by("-created_at")  # Від нових

# Комбінування
articles = (
    Article.objects
    .filter(is_published=True)
    .exclude(category__name="Draft")
    .order_by("-created_at")
)

# Отримати лише певні поля (для оптимізації)
articles = Article.objects.values_list("title", "created_at")

# Підрахувати записи
count = Article.objects.filter(is_published=True).count()

# Перевірити наявність
exists = Article.objects.filter(title="Django").exists()

# Перший та останній записи
first = Article.objects.first()
last = Article.objects.last()
```

### Агрегація та групування

Коли потрібна статистика:

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Скільки статей у кожної категорії
categories_with_counts = Category.objects.annotate(
    article_count=Count("articles")
)

# Середня оцінка всіх статей
avg_rating = Article.objects.aggregate(avg=Avg("rating"))["avg"]

# Сумарна кількість переглядів
total_views = Article.objects.aggregate(
    total=Sum("views"),
    max_views=Max("views")
)
```

### N+1 Problem — оптимізація запитів

**Неоптимізований код (много запитів):**
```python
# Це 1 запит до БД
articles = Article.objects.all()

# Це N запитів до БД (один для кожної статті!)
for article in articles:
    print(article.category.name)  # Запит для кожної статті
```

**Оптимізований код (мінімум запитів):**
```python
# Один запит, який завантажує й категорії
articles = Article.objects.select_related("category")

# Тепер це не 1+N запитів, а лише 1
for article in articles:
    print(article.category.name)  # Дані вже завантажені
```

Для Many-to-Many використовуйте `prefetch_related`:
```python
articles = Article.objects.prefetch_related("tags")
```

### Видалення та каскадне видалення

Що відбувається, коли видалити запис із ForeignKey:

```python
class Article(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # Видалити статті при видаленні категорії
        # on_delete=models.SET_NULL  # Поставити NULL
        # on_delete=models.PROTECT    # Заборонити видалення категорії
    )
```

- `CASCADE` — видалити залежні записи
- `SET_NULL` — поставити NULL (для опціональних полів)
- `PROTECT` — запобігти видаленню
- `SET_DEFAULT` — поставити значення за замовчуванням

### Тестування моделей у shell

У shell можна тестувати моделі:

```bash
python manage.py shell
```

```python
from myapp.models import Article, Category

# Створити категорію
cat = Category.objects.create(name="Web")

# Створити статтю
article = Article.objects.create(
    title="Django Tutorial",
    category=cat,
    content="Content here"
)

# Отримати всі
articles = Article.objects.all()

# Фільтрувати
web_articles = Article.objects.filter(category__name="Web")

# Видалити
article.delete()

# Вийти з shell
exit()
```

### Що потрібно запам'ятати
- Модель описує структуру даних.  
- Міграція переносить зміни з коду в базу даних.  
- ORM дозволяє працювати з даними як із Python-об'єктами.
- `select_related` і `prefetch_related` оптимізують запити.
- `Meta` клас налаштовує поведінку моделі.
- Адмін-панель потребує реєстрації моделей.
