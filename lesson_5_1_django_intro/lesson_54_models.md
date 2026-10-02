# Заняття 5.4. Моделі, міграції та Django ORM

## Про що це заняття

На попередніх заняттях ми вже навчилися створювати Django-застосунок, налаштовувати URL, писати `view` та передавати з нього дані в HTML-шаблон.

Наприклад, у нашому проєкті `view` створює словник `context` і передає його в `render()`:

```python
def index(request):
    context = {
        "title": "Головна сторінка",
        "message": "Ласкаво просимо до POOLS/Django!",
    }

    return render(request, "home.html", context)
```

Отже, ми вже вміємо передавати **дані з Python у HTML**.

Але виникає головне питання:

> **Звідки ці дані беруться у реальному вебзастосунку?**

Наприклад, якщо ми створюємо блог, ми не хочемо вручну записувати:

```python
context = {
    "title": "Моя стаття",
    "content": "Текст статті..."
}
```

для кожної статті.

Статті повинні зберігатися в базі даних.

Користувач відкриває сторінку → Django звертається до бази даних → отримує статті → `view` передає їх у шаблон → шаблон показує їх користувачу.

Саме для цього нам потрібні:

* **моделі**;
* **база даних**;
* **міграції**;
* **Django ORM**.

---

# 1. Загальна схема Django-застосунку

Перед тим як говорити про моделі, потрібно зрозуміти загальний рух даних.

У спрощеному вигляді:

```text
Користувач
    ↓
Браузер
    ↓ HTTP request
URL
    ↓
View
    ↓
ORM
    ↓
Model
    ↓
База даних
    ↑
ORM
    ↑
View
    ↓
Context
    ↓
Template
    ↓
HTML response
    ↓
Браузер
```

Це одна з найважливіших схем у Django.

### Що тут відбувається?

Коли користувач відкриває:

```text
/articles/
```

запит потрапляє до Django.

Django визначає, який `view` повинен його обробити.

Наприклад:

```python
path("articles/", views.articles)
```

Далі `view` може звернутися до бази:

```python
articles = Article.objects.all()
```

Django ORM виконує необхідний SQL-запит.

База даних повертає записи.

Django перетворює їх на Python-об'єкти.

`view` передає ці об'єкти в `context`.

Шаблон використовує їх для формування HTML.

HTML повертається браузеру.

---

# 2. Що ми вже вміємо без моделей

На попередньому занятті ми вже працювали з `view`.

Наприклад:

```python
def index(request):
    context = {
        "title": "Головна сторінка",
        "message": "Ласкаво просимо до Django!",
    }

    return render(request, "home.html", context)
```

Тут дані створюються безпосередньо в Python-коді.

Умовно:

```text
Python
  ↓
context
  ↓
template
  ↓
HTML
```

Це добре для навчального прикладу.

Але у справжньому застосунку дані зазвичай зберігаються в базі даних.

Наприклад:

```text
BlogPost
-----------------------------
id | title | content
-----------------------------
1  | Django | Текст...
2  | Python | Текст...
3  | SQL    | Текст...
```

Тоді `view` вже не створює ці дані вручну.

Він отримує їх із бази:

```python
posts = BlogPost.objects.all()
```

І передає в шаблон:

```python
context = {
    "posts": posts
}
```

---

# 3. Що таке модель Django

**Модель Django — це Python-клас, який описує структуру даних, з якими працює застосунок.**

Наприклад:

```python
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

Можна думати про модель як про опис майбутньої таблиці.

Умовно:

```text
Python model
      ↓
   BlogPost
      ↓
-------------------------
| id                  |
| title               |
| content             |
| created_at          |
-------------------------
      ↓
таблиця в БД
```

---

# 4. Модель і таблиця — це не одне й те саме

Важливо не говорити студентам, що:

> «модель — це таблиця».

Точніше:

> **Модель описує структуру даних, а Django на її основі створює та використовує таблицю бази даних.**

Наприклад:

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

описує дані.

А після виконання міграцій Django створює відповідну структуру в базі.

У нашій міграції це видно буквально:

```python
migrations.CreateModel(
    name="BlogPost",
    fields=[
        ...
        ("title", models.CharField(max_length=200)),
        ("content", models.TextField()),
    ],
)
```

Тобто Django перетворює опис моделі на операцію створення структури БД.

---

# 5. Поля моделі

Кожне поле моделі описує один тип даних.

Наприклад:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

Тут:

| Поле           | Призначення           |
| -------------- | --------------------- |
| `title`        | короткий текст        |
| `content`      | довгий текст          |
| `is_published` | `True` / `False`      |
| `created_at`   | дата та час створення |

У базі даних це будуть відповідні колонки.

---

# 6. Звідки взявся `id`?

Студент часто запитує:

> «Ми `id` не створювали. Звідки він взявся?»

Django автоматично додає первинний ключ, якщо ми не визначили його самостійно.

Це видно у створеній Django міграції:

```python
"id",
models.BigAutoField(
    auto_created=True,
    primary_key=True,
    ...
)
```

Тобто навіть якщо модель має тільки:

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
```

у базі все одно буде ідентифікатор запису.

Наприклад:

```text
id | title
---+----------------
1  | Django
2  | Python
3  | PostgreSQL
```

---

# 7. Як модель потрапляє в базу даних?

Самого Python-класу недостатньо.

Django потрібно повідомити:

> «структура моделі змінилася — зміни структуру бази даних».

Для цього використовуються **міграції**.

---

# 8. Що таке міграція

Міграція — це файл, у якому Django описує зміни структури бази даних.

Наприклад, спочатку в нас була модель `BlogPost`.

Потім ми додали `Article` та `Tags`.

Django створив наступну міграцію:

```text
0002_article_tags.py
```

У ній є:

```python
migrations.CreateModel(
    name="Article",
    ...
)
```

та:

```python
migrations.CreateModel(
    name="Tags",
    ...
)
```

Тобто міграція — це своєрідна **інструкція для бази даних**.

---

# 9. `makemigrations` і `migrate`

Після зміни моделі:

```bash
python manage.py makemigrations
```

Django аналізує зміни в моделях і створює файл міграції.

Потім:

```bash
python manage.py migrate
```

Django застосовує ці зміни до бази даних.

Схема:

```text
models.py
    ↓
makemigrations
    ↓
0001_initial.py
0002_...
0003_...
    ↓
migrate
    ↓
База даних
```

---

# 10. Чому міграції не створюють самі дані?

Це важливе розмежування.

Міграції описують **структуру**.

Наприклад:

```text
створити таблицю Article
додати колонку title
додати колонку content
```

А ось:

```text
Створити статтю "Django"
Створити статтю "Python"
```

— це вже **дані**.

Тобто:

```text
Міграції → структура БД

ORM → робота з даними
```

---

# 11. Що таке ORM

ORM — Object-Relational Mapping.

Django ORM дозволяє працювати з даними бази через Python-об'єкти.

Без ORM нам довелося б писати SQL:

```sql
SELECT * FROM article;
```

З ORM:

```python
Article.objects.all()
```

SQL залишається «під капотом».

Ми працюємо з Python:

```python
Article.objects.filter(is_published=True)
```

а Django формує відповідний SQL-запит.

---

# 12. Найважливіше: хто викликає ORM?

Ось тут починається зв'язок із `view`.

ORM не працює сам по собі.

Зазвичай саме **view отримує дані з бази і вирішує, що з ними робити**.

Наприклад:

```python
from django.shortcuts import render
from .models import Article


def article_list(request):
    articles = Article.objects.all()

    context = {
        "articles": articles
    }

    return render(request, "articles.html", context)
```

Подивимося на цей код поетапно.

---

# 13. Крок 1 — браузер робить запит

Користувач відкриває:

```text
/articles/
```

Django отримує HTTP request.

URL повинен бути пов'язаний із `view`:

```python
path("articles/", views.article_list)
```

Отже:

```text
GET /articles/
       ↓
article_list()
```

---

# 14. Крок 2 — запускається view

Django викликає:

```python
def article_list(request):
```

Поки що ми знаходимося всередині Python-коду.

---

# 15. Крок 3 — view звертається до моделі

У `view` ми пишемо:

```python
articles = Article.objects.all()
```

Тут:

```python
Article
```

— наша модель.

А:

```python
objects
```

— менеджер моделі, через який ми виконуємо запити.

```python
all()
```

означає:

> отримати всі записи `Article`.

---

# 16. Крок 4 — Django звертається до БД

Коли Django виконує:

```python
Article.objects.all()
```

ORM формує SQL-запит.

У спрощеному вигляді:

```sql
SELECT
    id,
    title,
    content,
    is_published,
    created_at
FROM article;
```

База даних повертає рядки.

Наприклад:

```text
1 | Django | Вступ...
2 | Python | Основи...
3 | SQL    | Запити...
```

Django перетворює ці дані на Python-об'єкти.

---

# 17. Крок 5 — результат повертається у view

Тепер:

```python
articles = Article.objects.all()
```

містить QuerySet.

Наприклад:

```python
<QuerySet [
    <Article: Django>,
    <Article: Python>,
    <Article: SQL>
]>
```

Ми можемо перебирати його:

```python
for article in articles:
    print(article.title)
```

Результат:

```text
Django
Python
SQL
```

---

# 18. Крок 6 — view передає дані в context

Тепер:

```python
context = {
    "articles": articles
}
```

Це вже знайомий студентам механізм.

Раніше ми робили:

```python
context = {
    "title": "Головна сторінка"
}
```

Тепер значення `"articles"` отримане не з тексту в `view`, а з бази даних.

Тобто:

```text
БД
 ↓
ORM
 ↓
articles
 ↓
context
 ↓
template
```

---

# 19. Крок 7 — template показує дані

У шаблоні:

```html
<h1>Статті</h1>

{% for article in articles %}
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
{% endfor %}
```

Django бере об'єкти з:

```python
context["articles"]
```

і передає їх у шаблон.

---

# 20. Повний приклад

### `models.py`

```python
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
```

### `views.py`

```python
from django.shortcuts import render
from .models import Article


def article_list(request):
    articles = Article.objects.all()

    context = {
        "articles": articles
    }

    return render(request, "articles.html", context)
```

### `urls.py`

```python
from django.urls import path
from . import views


urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
]
```

### `articles.html`

```html
<h1>Статті</h1>

{% for article in articles %}
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>
{% endfor %}
```

Тепер можна показати студентам всю систему:

```text
GET /articles/
      ↓
urls.py
      ↓
article_list()
      ↓
Article.objects.all()
      ↓
Django ORM
      ↓
Database
      ↓
QuerySet
      ↓
context
      ↓
articles.html
      ↓
HTML
      ↓
Browser
```

---

# 21. Що таке QuerySet

`QuerySet` — це результат роботи ORM, який представляє набір записів.

Наприклад:

```python
articles = Article.objects.all()
```

або:

```python
articles = Article.objects.filter(is_published=True)
```

QuerySet можна комбінувати:

```python
articles = (
    Article.objects
    .filter(is_published=True)
    .order_by("-created_at")
)
```

Тут ми:

1. отримуємо `Article`;
2. залишаємо тільки опубліковані;
3. сортуємо від нових до старих.

---

# 22. `all()`, `filter()` і `get()`

### `all()`

```python
Article.objects.all()
```

Отримати всі записи.

### `filter()`

```python
Article.objects.filter(is_published=True)
```

Отримати всі записи, які відповідають умові.

### `get()`

```python
article = Article.objects.get(id=1)
```

Отримати один конкретний об'єкт.

Наприклад, для сторінки конкретної статті:

```text
/articles/5/
```

можна отримати:

```python
article = Article.objects.get(id=5)
```

---

# 23. View як механізм вибору даних

Це дуже важливе поняття.

`view` — це не просто функція, яка повертає HTML.

У реальному застосунку `view` часто визначає:

> **які саме дані потрібно отримати для конкретного HTTP-запиту.**

Наприклад, сторінка всіх статей:

```python
def article_list(request):
    articles = Article.objects.all()

    return render(
        request,
        "articles.html",
        {"articles": articles}
    )
```

А сторінка однієї статті:

```python
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)

    return render(
        request,
        "article.html",
        {"article": article}
    )
```

Тобто два різних URL можуть використовувати одну модель, але отримувати різні дані.

---

# 24. Дані можуть приходити у view з URL

Наприклад:

```python
path(
    "articles/<int:article_id>/",
    views.article_detail
)
```

Користувач відкриває:

```text
/articles/15/
```

Django передає:

```python
article_id = 15
```

у:

```python
def article_detail(request, article_id):
```

Після цього `view` використовує це значення для пошуку в БД:

```python
article = Article.objects.get(id=article_id)
```

Отримуємо:

```text
URL
 ↓
article_id = 15
 ↓
view
 ↓
ORM
 ↓
Article з id=15
```

Це вже реальний зв'язок між HTTP та базою даних.

---

# 25. А звідки беруться дані для створення запису?

До цього ми розглядали тільки читання.

Але в реальному застосунку користувач повинен мати можливість створити дані.

Наприклад:

```text
Користувач відкрив:
Створити статтю

        ↓

Заповнив:

Title: Django ORM
Content: ORM дозволяє...

        ↓

Натиснув "Зберегти"

        ↓

Дані потрапили у БД
```

Для цього використовуються HTML-форми.

Цей механізм ми вже розглядали на наступному занятті, але зараз важливо зрозуміти його зв'язок із моделями.

---

# 26. HTML-форма як джерело даних

Найпростіший варіант:

```html
<form method="post">
    {% csrf_token %}

    <input type="text" name="title">

    <textarea name="content"></textarea>

    <button type="submit">
        Створити
    </button>
</form>
```

Користувач вводить:

```text
title = "Django ORM"
content = "ORM дозволяє..."
```

і браузер відправляє HTTP POST-запит.

---

# 27. View отримує дані форми

У `view`:

```python
def article_create(request):

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        Article.objects.create(
            title=title,
            content=content
        )

    return render(request, "article_form.html")
```

Тут уже можна побачити повний шлях **від користувача до бази**.

---

# 28. Повний шлях створення даних

```text
Користувач
     ↓
HTML form
     ↓
HTTP POST
     ↓
view
     ↓
request.POST
     ↓
Article.objects.create()
     ↓
Django ORM
     ↓
INSERT
     ↓
База даних
```

Наприклад:

```python
Article.objects.create(
    title="Django ORM",
    content="ORM дозволяє працювати з БД через Python"
)
```

створить новий запис.

У базі з'явиться приблизно:

```text
id | title       | content
---+-------------+----------------------
1  | Django ORM  | ORM дозволяє...
```

---

# 29. Таким чином, view працює у двох напрямках

Це ключова ідея заняття.

### Отримання даних

```text
БД
 ↓
ORM
 ↓
view
 ↓
context
 ↓
template
 ↓
Browser
```

### Запис даних

```text
Browser
 ↓
HTML form
 ↓
POST
 ↓
view
 ↓
ORM
 ↓
БД
```

Тому `view` можна розглядати як **посередника між HTTP-запитом і даними застосунку**.

---

# 30. Створення запису через ORM

ORM дозволяє створювати об'єкти кількома способами.

### Варіант 1

```python
article = Article.objects.create(
    title="Django",
    content="Вивчаємо Django"
)
```

Об'єкт одразу зберігається в БД.

### Варіант 2

```python
article = Article(
    title="Django",
    content="Вивчаємо Django"
)

article.save()
```

Тут:

```text
Article(...)
    ↓
Python object
    ↓
save()
    ↓
БД
```

---

# 31. Читання, зміна та видалення

ORM дозволяє виконувати основні CRUD-операції.

### Create

```python
Article.objects.create(
    title="Django",
    content="..."
)
```

### Read

```python
articles = Article.objects.all()
```

### Update

```python
article = Article.objects.get(id=1)

article.title = "Новий заголовок"

article.save()
```

### Delete

```python
article = Article.objects.get(id=1)

article.delete()
```

Отже:

```text
C — Create
R — Read
U — Update
D — Delete
```

---

# 32. Як працює Update

Наприклад:

```python
article = Article.objects.get(id=1)
```

Ми отримали Python-об'єкт.

Потім:

```python
article.title = "Новий заголовок"
```

Змінили Python-об'єкт.

Але база даних ще не змінилася.

Для збереження:

```python
article.save()
```

Схема:

```text
БД
 ↓
get()
 ↓
Python object
 ↓
зміна атрибута
 ↓
save()
 ↓
БД
```

---

# 33. Зв'язок між моделями

У реальному проєкті дані пов'язані.

Наприклад:

```text
Category
   │
   ├── Article
   ├── Article
   └── Article
```

Одна категорія може містити багато статей.

Для цього використовується:

```python
category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE
)
```

---

# 34. ForeignKey

Наприклад:

```python
class Category(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
```

Тепер стаття має категорію.

Наприклад:

```text
Category
---------
1 | Django
2 | Python

Article
-------------------------
1 | Models       | 1
2 | ORM          | 1
3 | Functions    | 2
```

Остання колонка — посилання на категорію.

---

# 35. Отримання пов'язаних даних через ORM

Можна знайти всі статті категорії:

```python
articles = Article.objects.filter(
    category__name="Django"
)
```

Або отримати категорію статті:

```python
article.category
```

Наприклад:

```python
print(article.category.name)
```

Отримаємо:

```text
Django
```

---

# 36. Many-to-many

Іноді одна стаття може мати декілька тегів.

Наприклад:

```text
Article
   │
   ├── Django
   ├── ORM
   └── Python
```

І один тег може використовуватися в багатьох статтях.

Для цього:

```python
class Tag(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=200)

    tags = models.ManyToManyField(Tag)
```

---

# 37. Параметри полів

Модель не тільки описує тип даних.

Вона також може задавати правила.

Наприклад:

```python
class Task(models.Model):

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

    description = models.TextField(
        blank=True,
        null=True
    )

    priority = models.IntegerField(
        default=0
    )

    email = models.EmailField(
        unique=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
```

---

# 38. `default`, `blank`, `null`, `unique`

### `default`

```python
priority = models.IntegerField(default=0)
```

Якщо значення не передали, використовується `0`.

### `blank=True`

Дозволяє не заповнювати поле під час валідації форми.

### `null=True`

Дозволяє зберігати `NULL` у базі даних.

### `unique=True`

Значення повинні бути унікальними.

Наприклад:

```python
email = models.EmailField(unique=True)
```

Два записи з однаковим email створити не можна.

---

# 39. `choices`

Для значень, які повинні бути обмежені певним списком:

```python
STATUS_CHOICES = [
    ("new", "Нове"),
    ("in_progress", "У процесі"),
    ("done", "Готово"),
]
```

і:

```python
status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="new"
)
```

Важливо розуміти різницю:

```text
"new"
```

— значення, яке зберігається.

```text
"Нове"
```

— текстове представлення для користувача.

---

# 40. Автоматичні поля дат

Наприклад:

```python
created_at = models.DateTimeField(
    auto_now_add=True
)
```

Дата встановлюється під час створення запису.

А:

```python
updated_at = models.DateTimeField(
    auto_now=True
)
```

оновлюється під час збереження.

Це зручно для моделей, де потрібно знати:

```text
коли створили запис
коли востаннє його змінювали
```

---

# 41. `Meta`

У моделі можна налаштовувати її поведінку через вкладений клас `Meta`.

Наприклад:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"
```

`ordering` означає:

> за замовчуванням отримувати статті від нових до старих.

Тому:

```python
Article.objects.all()
```

вже буде повертати їх у заданому порядку.

---

# 42. Методи моделі

Модель — це Python-клас.

Тому вона може мати методи.

Наприклад:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def get_preview(self, length=100):
        return self.content[:length] + "..."
```

Тепер:

```python
article.get_preview()
```

може повернути короткий фрагмент статті.

Це ще раз показує головну ідею Django:

> **Запис із бази після отримання через ORM стає Python-об'єктом.**

---

# 43. Важливе уточнення до нашого прикладу

У навчальному `models.py` є методи:

```python
def increment_views(self):
    self.views += 1
```

та:

```python
@property
def is_popular(self):
    return self.views > 1000
```

Але в моделі `BlogPost` поле `views` не оголошене.

Тобто такий код у поточному вигляді викличе помилку при використанні цих методів.

Якщо ми хочемо використовувати перегляди, модель повинна містити:

```python
views = models.IntegerField(default=0)
```

Наприклад:

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def increment_views(self):
        self.views += 1
        self.save()
```

Після зміни моделі знову:

```bash
python manage.py makemigrations
python manage.py migrate
```

Це хороший практичний приклад того, **навіщо потрібні міграції**.

---

# 44. ORM і SQL

Важливо розуміти, що ORM не «знищує» SQL.

Він просто дозволяє працювати з базою через Python.

Наприклад:

```python
Article.objects.filter(
    is_published=True
)
```

концептуально відповідає:

```sql
SELECT *
FROM article
WHERE is_published = TRUE;
```

Тому знання SQL залишається важливим.

Особливо коли запити стають складними або потрібно оптимізувати застосунок.

---

# 45. Пошук та фільтрація

Наприклад:

```python
Article.objects.filter(
    title__icontains="django"
)
```

`icontains` означає пошук за входженням без врахування регістру.

Можна комбінувати умови:

```python
articles = Article.objects.filter(
    is_published=True,
    title__icontains="django"
)
```

Можна сортувати:

```python
articles = Article.objects.order_by(
    "-created_at"
)
```

---

# 46. Реальний приклад view для списку

Тепер об'єднаємо все разом.

```python
from django.shortcuts import render
from .models import Article


def article_list(request):

    articles = (
        Article.objects
        .filter(is_published=True)
        .order_by("-created_at")
    )

    context = {
        "articles": articles
    }

    return render(
        request,
        "articles.html",
        context
    )
```

Тут уже є практично вся логіка заняття:

```text
request
   ↓
view
   ↓
Article
   ↓
ORM
   ↓
БД
   ↓
QuerySet
   ↓
context
   ↓
template
```

---

# 47. Шаблон

`articles.html`:

```html
<h1>Опубліковані статті</h1>

{% for article in articles %}

    <article>
        <h2>{{ article.title }}</h2>

        <p>
            {{ article.content }}
        </p>

        <small>
            {{ article.created_at }}
        </small>
    </article>

{% empty %}

    <p>Статей поки немає.</p>

{% endfor %}
```

Тут `articles` — це саме те значення, яке `view` поклав у `context`.

---

# 48. Відповідність між Python та HTML

У `view`:

```python
context = {
    "articles": articles
}
```

У template:

```django
{% for article in articles %}
```

Потім:

```django
{{ article.title }}
```

відповідає:

```python
article.title
```

А:

```django
{{ article.content }}
```

відповідає:

```python
article.content
```

Тобто template отримує Python-об'єкти, які прийшли з ORM.

---

# 49. Повний життєвий цикл даних

Тепер можемо показати студентам найважливішу схему всього заняття.

## Читання

```text
1. Browser
       ↓
2. HTTP GET
       ↓
3. URL
       ↓
4. View
       ↓
5. ORM
       ↓
6. Database
       ↓
7. QuerySet
       ↓
8. Context
       ↓
9. Template
       ↓
10. HTML
       ↓
11. Browser
```

## Створення

```text
1. Browser
       ↓
2. HTML form
       ↓
3. HTTP POST
       ↓
4. View
       ↓
5. request.POST / Form
       ↓
6. ORM
       ↓
7. Database
```

Ці дві схеми — головний результат цього заняття.

---

# 50. Чому не можна покласти роботу з БД у template?

Template повинен в основному відповідати за представлення даних.

Не варто робити там логіку роботи з базою.

Правильніше:

```text
View
 ↓
отримати дані
 ↓
Context
 ↓
Template
 ↓
показати дані
```

А не:

```text
Template
 ↓
самостійно шукати дані в БД
```

Таким чином кожен компонент має свою відповідальність.

---

# 51. Що робить кожна частина Django

### URL

Визначає:

> який `view` потрібно викликати.

```python
path("articles/", views.article_list)
```

### View

Визначає:

> що потрібно зробити із запитом.

Наприклад:

```python
articles = Article.objects.all()
```

### Model

Описує:

> з якими даними ми працюємо.

```python
class Article(models.Model):
```

### ORM

Дозволяє:

> отримувати та змінювати дані через Python.

```python
Article.objects.all()
```

### Database

Фізично зберігає:

> записи.

### Template

Відповідає:

> як показати отримані дані користувачу.

---

# 52. Практична частина

Створимо простий список статей.

## Крок 1. Модель

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Крок 2. Міграції

```bash
python manage.py makemigrations
python manage.py migrate
```

## Крок 3. Додамо дані

На першому етапі можна використати Django shell:

```bash
python manage.py shell
```

```python
from polls.models import Article

Article.objects.create(
    title="Перша стаття",
    content="Мій перший текст",
    is_published=True
)

Article.objects.create(
    title="Друга стаття",
    content="Ще один текст",
    is_published=True
)
```

---

# 53. Перевіримо дані

У shell:

```python
articles = Article.objects.all()
```

Можна виконати:

```python
for article in articles:
    print(article.id, article.title)
```

Наприклад:

```text
1 Перша стаття
2 Друга стаття
```

Тепер дані вже знаходяться не в Python-коді `view`, а в базі даних.

---

# 54. Створимо view

```python
from django.shortcuts import render
from .models import Article


def article_list(request):

    articles = Article.objects.all()

    return render(
        request,
        "articles.html",
        {
            "articles": articles
        }
    )
```

---

# 55. Додамо URL

```python
path(
    "articles/",
    views.article_list,
    name="article_list"
)
```

Тепер:

```text
/articles/
```

викликає:

```python
article_list()
```

---

# 56. Створимо template

```html
<h1>Мої статті</h1>

{% for article in articles %}

    <h2>{{ article.title }}</h2>

    <p>
        {{ article.content }}
    </p>

{% endfor %}
```

Відкриваємо:

```text
http://127.0.0.1:8000/articles/
```

і бачимо записи з бази даних.

---

# 57. Тепер додамо створення статті

Найпростіший навчальний варіант:

```html
<form method="post">
    {% csrf_token %}

    <input
        type="text"
        name="title"
        placeholder="Заголовок"
    >

    <textarea
        name="content"
        placeholder="Текст"
    ></textarea>

    <button type="submit">
        Створити
    </button>
</form>
```

View:

```python
def article_create(request):

    if request.method == "POST":

        title = request.POST["title"]
        content = request.POST["content"]

        Article.objects.create(
            title=title,
            content=content
        )

    return render(
        request,
        "article_create.html"
    )
```

---

# 58. Що відбулося після натискання кнопки?

Користувач ввів:

```text
title:
Django ORM

content:
ORM дозволяє працювати з базою через Python.
```

Натиснув:

```text
Створити
```

Браузер відправив:

```text
POST /articles/create/
```

Django передав запит у:

```python
article_create(request)
```

Дані опинилися в:

```python
request.POST
```

Після цього:

```python
Article.objects.create(...)
```

записав їх у БД.

Тобто ми пройшли весь шлях:

```text
HTML
 ↓
HTTP POST
 ↓
View
 ↓
request.POST
 ↓
ORM
 ↓
Model
 ↓
Database
```

---

# 59. Важливе зауваження про форми

Цей приклад спеціально спрощений.

У реальному Django-проєкті ми зазвичай не будемо вручну робити:

```python
request.POST["title"]
```

і самостійно перевіряти кожне поле.

Для цього Django має **Forms** та **ModelForms**.

Наприклад, модель:

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

може бути пов'язана з формою.

Форма бере інформацію про поля моделі та допомагає:

* створити HTML-форму;
* отримати дані;
* перевірити їх;
* показати помилки;
* створити або змінити об'єкт моделі.

Детально цей механізм ми розглянемо на занятті про Django Forms.

---

# 60. Що треба запам'ятати

### 1. Модель

Описує структуру даних:

```python
class Article(models.Model):
```

### 2. Міграція

Описує зміни структури БД:

```bash
python manage.py makemigrations
```

### 3. `migrate`

Застосовує зміни до БД:

```bash
python manage.py migrate
```

### 4. ORM

Дозволяє працювати з БД через Python:

```python
Article.objects.all()
```

### 5. View

Визначає, які дані отримати або змінити:

```python
def article_list(request):
```

### 6. Context

Передає дані в template:

```python
{
    "articles": articles
}
```

### 7. Template

Відображає дані:

```django
{{ article.title }}
```

---

# 61. Головна схема заняття

Якщо потрібно запам'ятати лише одну схему, нехай це буде:

```text
                 ┌──────────────┐
                 │   Browser    │
                 └──────┬───────┘
                        │
                     HTTP
                        │
                        ▼
                 ┌──────────────┐
                 │     URL      │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │     View     │
                 └──────┬───────┘
                        │
                   Django ORM
                        │
                        ▼
                 ┌──────────────┐
                 │   Database   │
                 └──────┬───────┘
                        │
                     QuerySet
                        │
                        ▼
                 ┌──────────────┐
                 │     View     │
                 └──────┬───────┘
                        │
                     Context
                        │
                        ▼
                 ┌──────────────┐
                 │   Template   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Browser    │
                 └──────────────┘
```

А при створенні даних:

```text
Browser
   │
   │ POST
   ▼
Form
   │
   ▼
View
   │
   ▼
ORM
   │
   ▼
Database
```

---

# Підсумок

Модель — це Python-клас, який описує структуру даних.

Міграції дозволяють синхронізувати структуру моделей зі структурою бази даних.

ORM дозволяє працювати з даними бази через Python.

Але модель сама по собі не показує дані користувачу.

У типовому Django-застосунку дані проходять через `view`:

```text
Database
    ↓
ORM
    ↓
View
    ↓
Context
    ↓
Template
    ↓
Browser
```

А дані від користувача можуть пройти зворотний шлях:

```text
Browser
    ↓
Form
    ↓
HTTP POST
    ↓
View
    ↓
ORM
    ↓
Database
```

Саме `view` зв'язує HTTP-рівень застосунку з даними, які зберігаються через моделі та ORM.
