Ось конспект для студента з прикладами.

## CRUD і Django Forms

На цьому занятті ти вчишся працювати з формами в Django та керувати об’єктами у вебзастосунку: створювати, редагувати, переглядати й видаляти дані. Це одна з базових навичок у Django, бо майже будь-який сайт працює саме через такі дії.

### 1. Що таке CRUD

CRUD — це 4 основні дії з даними:

- **C**reate — створити новий об’єкт.
- **R**ead — переглянути об’єкти або один об’єкт.
- **U**pdate — змінити існуючий об’єкт.
- **D**elete — видалити об’єкт.

Приклад: якщо у тебе є сайт для нотаток, то:
- створити нотатку;
- показати список нотаток;
- змінити текст нотатки;
- видалити нотатку.

У Django ці дії зазвичай реалізують через views, templates, форми та ORM.

### 2. HTML-форми

HTML-форма — це спосіб отримати дані від користувача.

Приклад простого HTML-коду:

```html
<form method="post">
  <input type="text" name="title">
  <button type="submit">Зберегти</button>
</form>
```

Тут:
- `method="post"` означає, що дані будуть надіслані на сервер;
- `input` — поле вводу;
- `button` — кнопка відправки.

### 3. GET і POST

У веброзробці є два дуже важливі методи надсилання форми:

- **GET** — використовується, коли потрібно отримати дані. Наприклад, пошук або фільтр.
- **POST** — використовується, коли дані створюються або змінюються.

Приклад:
- `GET /tasks/?q=python` — пошук задач.
- `POST /tasks/create/` — створення нової задачі.

Зазвичай:
- для показу сторінки з формою використовують `GET`;
- для збереження даних після натискання кнопки — `POST`.

### 4. Django Form

`Form` у Django — це клас, який допомагає:
- описати поля форми;
- перевірити введені дані;
- показати помилки;
- отримати очищені дані.

Приклад форми:

```python
from django import forms

class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    is_done = forms.BooleanField(required=False)
```

Тут:
- `CharField` — текстове поле;
- `BooleanField` — логічне поле;
- `required=False` означає, що поле не обов’язкове.

### 5. Зв’язана і незв’язана форма

- **Незв’язана форма** — форма без даних. Вона просто відображається користувачу.
- **Зв’язана форма** — форма з даними, які користувач уже ввів.

Приклад:

```python
form = TaskForm()  
form = TaskForm(request.POST)
```

Перша форма — порожня.

Друга — отримала дані з запиту і готова до перевірки.

### 6. Валідація

Валідація — це перевірка правильності даних.

Наприклад:
- поле не може бути порожнім;
- email має бути у правильному форматі;
- число має бути в потрібному діапазоні.

Приклад перевірки у view:

```python
if form.is_valid():
    title = form.cleaned_data["title"]
```

`is_valid()` перевіряє форму.

`cleaned_data` — це вже очищені та перевірені дані.

### 7. Помилки форми

Якщо користувач ввів щось неправильно, Django покаже помилку.

Наприклад:
- поле не заповнене;
- введено занадто довгий текст;
- дані не відповідають типу поля.

У шаблоні можна показати помилку так:

```html
{{ form.errors }}
```

Або для окремого поля:

```html
{{ form.title.errors }}
```

### 8. Віджети

Віджет у Django — це спосіб відображення поля у HTML.

Приклади:
- текстове поле;
- checkbox;
- textarea;
- select.

Наприклад:

```python
class TaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea)
```

Віджет не лише визначає вигляд поля, а й допомагає зробити форму зручною для користувача.

### 9. Приклад форми в Django

```python
from django import forms

class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
```

View:

```python
from django.shortcuts import render

def task_create(request):
    form = TaskForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        print(title, description)

    return render(request, "task_form.html", {"form": form})
```

Шаблон:

```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Зберегти</button>
</form>
```

`csrf_token` потрібен для безпеки.

`form.as_p` виводить поля форми у вигляді абзаців.

### 10. CRUD через форму

#### Create
Створення нового об’єкта.

```python
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Task.objects.create(
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
        )
    return render(request, "task_form.html", {"form": form})
```

#### Update
Редагування існуючого об’єкта.

```python
def task_update(request, task_id):
    task = Task.objects.get(id=task_id)
    form = TaskForm(request.POST or None, initial={
        "title": task.title,
        "description": task.description,
    })

    if request.method == "POST" and form.is_valid():
        task.title = form.cleaned_data["title"]
        task.description = form.cleaned_data["description"]
        task.save()

    return render(request, "task_form.html", {"form": form})
```

#### Delete
Видалення об’єкта.

```python
def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "task_confirm_delete.html", {"task": task})
```

### 11. Як працює видалення

Видалення краще робити через форму з підтвердженням.

Приклад шаблону:

```html
<form method="post">
  {% csrf_token %}
  <p>Видалити задачу "{{ task.title }}"?</p>
  <button type="submit">Так, видалити</button>
</form>
```

Так користувач випадково не видалить дані одним кліком.

### 12. Типовий сценарій

Наприклад, є модель `Book`.

Користувач:
- відкриває сторінку створення книги;
- заповнює форму;
- натискає кнопку;
- Django перевіряє дані;
- якщо все правильно — запис зберігається в базу;
- якщо є помилки — форма показує повідомлення.

Саме так працює більшість CRUD-сторінок у Django.

### 13. Що треба запам’ятати

- `GET` — для отримання даних.
- `POST` — для створення або зміни даних.
- `Form` допомагає працювати з даними безпечно і зручно.
- `is_valid()` запускає перевірку форми.
- `cleaned_data` містить уже перевірені дані.
- CRUD — це основа роботи з об’єктами в вебзастосунку.

### 14. Міні-приклад для повторення

```python
from django import forms
from django.shortcuts import render, redirect

class NoteForm(forms.Form):
    text = forms.CharField(max_length=200)

def note_create(request):
    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Note.objects.create(text=form.cleaned_data["text"])
        return redirect("note_list")
    return render(request, "note_form.html", {"form": form})
```

Цей приклад показує повний цикл: форма, перевірка, збереження, перенаправлення. 