
**Преимущества CBV:**
- Повторное использование кода
- Четкая структура (методы для GET, POST и т.д.)
- Встроенная обработка ошибок
- Готовые решения для типовых задач
- Легкое расширение через миксины
## Базовые классы:

1. View
	* Базовый класс для всех CBV
	* Обрабатывает HTTP-методы (GET, POST и т.д.)
	- Используется для создания кастомных представлений

2.  TemplateViews
	* Отображает HTML-шаблон
	```python
	class HomePage(TemplateView):
	    template_name = 'home.html'
	```

3. RedirectView
	* Перенаправляет на другой url
	```python
	class OldUrlRedirect(RedirectView):
	    pattern_name = 'new-url-name'
	```

## **Представления для работы с моделями:**

1. ListView
	* Отображает список объектов модели
	* Пагинация, фильтрация, сортировка
	```python
	class BookListView(ListView):
	    model = Book
	    template_name = 'books/book_list.html'
	    context_object_name = 'books'  # Имя переменной в шаблоне
	    paginate_by = 10  # Пагинация по 10 элементов
	    ordering = ['-published_date']  # Сортировка по дате

	    def get_queryset(self):
	        # Фильтрация по автору через URL-параметр (?author=...)
	        queryset = super().get_queryset()
	        author = self.request.GET.get('author')
	        if author:
	            queryset = queryset.filter(author__icontains=author)
	        return queryset
	
	    def get_context_data(self, **kwargs):
	        # Добавление дополнительных данных в контекст
	        context = super().get_context_data(**kwargs)
	        context['total_books'] = Book.objects.count()
	        return context
	```

2. DetailView
	* Показывает детали одного объекта
	```python
	# views.py
	from django.views.generic import DetailView
	from .models import Book
	
	class BookDetailView(DetailView):
	    model = Book
	    template_name = 'books/book_detail.html'
	    context_object_name = 'book'
	
	    def get_object(self, queryset=None):
	        # Кастомная логика получения объекта
	        obj = super().get_object(queryset)
	        obj.views_count += 1  # Счетчик просмотров
	        obj.save()
	        return obj
	```

3. CreateView
	* Создание новых объектов через форму
	```python
	from django.views.generic import CreateView
	from django.urls import reverse_lazy
	from .models import Book
	
	class BookCreateView(CreateView):
	    model = Book
	    template_name = 'books/book_form.html'
	    fields = ['title', 'author', 'published_date']
	    success_url = reverse_lazy('book-list')  # Перенаправление после успеха
	
	    def form_valid(self, form):
	        # Дополнительные действия перед сохранением
	        form.instance.created_by = self.request.user
	        return super().form_valid(form)
	```

4. UpdateView
	* Редактирование существующих объектов
	```python
	# views.py
	from django.views.generic import UpdateView
	from django.contrib.messages.views import SuccessMessageMixin
	
	class BookUpdateView(SuccessMessageMixin, UpdateView):
	    model = Book
	    fields = ['title', 'author']
	    template_name = 'books/book_form.html'
	    success_message = "Книга успешно обновлена!"
	
	    def get_success_url(self):
	        # Динамический URL с использованием pk объекта
	        return reverse('book-detail', kwargs={'pk': self.object.pk})
	```

5. DeleteView
	* Удаление объектов с подтверждением
	```python
	# views.py
	from django.views.generic import DeleteView
	
	class BookDeleteView(DeleteView):
	    model = Book
	    template_name = 'books/book_confirm_delete.html'
	    success_url = reverse_lazy('book-list')
	
	    def delete(self, request, *args, **kwargs):
	        # Дополнительные действия перед удалением
	        messages.success(request, "Книга удалена!")
	        return super().delete(request, *args, **kwargs)
	```

## Работа с формами

1. FormView
	* Обработка произвольных форм (не привязанных к модели)
	```python
	# forms.py
	from django import forms
	
	class ContactForm(forms.Form):
	    name = forms.CharField(label='Ваше имя')
	    email = forms.EmailField(label='Email')
	    message = forms.CharField(widget=forms.Textarea)
	
	# views.py
	from django.views.generic import FormView
	from django.urls import reverse_lazy
	
	class ContactView(FormView):
	    template_name = 'contact.html'
	    form_class = ContactForm
	    success_url = reverse_lazy('thanks')
	
	    def form_valid(self, form):
	        # Обработка данных формы
	        name = form.cleaned_data['name']
	        email = form.cleaned_data['email']
	        message = form.cleaned_data['message']
	        send_contact_email(name, email, message)  # Ваша функция отправки
	        return super().form_valid(form)
	```

## Аутентификация

1. LoginView
	* Авторизация пользователей
	```python
	class CustomLoginView(LoginView):
	    template_name = 'accounts/login.html'
	```

2. LogoutView
	* Выход из системы
	```python
	class CustomLogoutView(LogoutView):
	    next_page = '/'
	```

3. PasswordChangeView
	* Смена пароля

4. PasswordResetView
	* Сброс пароля


## Миксины
1. ModelFormMixin
	* Миксин для работы с формами на основе моделей

2. LoginRequiredMixin
	* Требует авторизации для доступа
	```python
	class SecretView(LoginRequiredMixin, TemplateView):
	    template_name = 'secret.html'
	```

3. UserPassesTestMixin
	* Проверка прав доступа
	```python
	class AdminOnlyView(UserPassesTestMixin, View):
	    def test_func(self):
	        return self.request.user.is_superuser
	```

4. JsonResponseMixin
	* Возврат JSON-объектов
	```python
	class ApiView(JsonResponseMixin, View):
	    def get(self, request):
	        data = {'status': 'ok'}
	        return self.render_to_json_response(data)
	```

5. MultipleObjectMixin
	* Базовый функционал для работы с наборами объектов

## Другие полезные CBV

1. ArchiveIndexView
	* Для работы с архивами по датам (например, блог)
	```python
	class ArticleArchiveView(ArchiveIndexView):
	    model = Article
	    date_field = 'pub_date'
	```

2. YearArchiveView/MonthArchiveView/DayArchiveView
	* Фильтрация по датам


## **Пример иерархии наследования:**

View
├── TemplateView
├── RedirectView
├── FormView
│   ├── CreateView
│   └── UpdateView
└── BaseDetailView
    └── DetailView