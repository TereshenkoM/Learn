Преимущества:
- **Повторное использование кода**: Наследование позволяет расширять базовые классы.
- **Структурированность**: Разделение логики для разных HTTP-методов (GET, POST и т.д.).
- **Абстракция**: Готовые решения для CRUD (Create, Read, Update, Delete) операций.
- **Интеграция с DRF**: Встроенная поддержка сериализаторов, аутентификации, прав доступа, пагинации.


## Иерархия классов в DRF

1.  **APIView** (Базовый класс, аналогичный Django `View`)
	*  Обрабатывает HTTP-методы через методы класса: `get()`, `post()`, `put()` и т.д.
	- Интегрирует механизмы аутентификации, разрешений, throttle.
	
	  ```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

2. **GenericAPIView**. Наследуется от `APIView` и добавляет функционал для работы с моделями и сериализаторами:
	* queryset: Определяет набор данных.
	- serializer_class: Указывает сериализатор.
	- Методы: get_queryset(), get_serializer(), get_object() (для детальных view).
	- **Используется вместе с миксинами** например, CreateModelMixin, ListModelMixin

	```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

class BookList(GenericAPIView, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
```

3. **Миксины (Mixins)**. Добавляют конкретное поведение:
	- CreateModelMixin: Реализует create() (POST)
	- ListModelMixin: Реализует list() (GET для списка)
	 - RetrieveModelMixin: Реализует retrieve() (GET для одного объекта)
	 - UpdateModelMixin: Реализует update() (PUT, PATCH)
	- DestroyModelMixin: Реализует destroy() (DELETE)
	
4. **Готовые Generic-классы**. Комбинации `GenericAPIView` и миксинов для стандартных операций:
	* ListCreateAPIView: GET (список) + POST.
	- RetrieveUpdateDestroyAPIView: GET (один объект) + PUT + PATCH + DELETE.
	- ListAPIView, CreateAPIView и т.д

	```python
from rest_framework.generics import ListCreateAPIView

class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

## ViewSets и Routers

1.**ViewSet**. Объединяет логику для связанных операций в одном классе. Например, `ModelViewSet` предоставляет все CRUD-методы:

```python
from rest_framework.viewsets import ModelViewSet

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

2.  **ReadOnlyModelViewSet**. Только для чтения (GET-запросы):

```python
from rest_framework.viewsets import ReadOnlyModelViewSet

class BookReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

3. **Роутеры**. Автоматически генерируют URL-маршруты для ViewSet:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)
urlpatterns = router.urls
```

Это создаст эндпоинты:

- `/books/` (GET, POST)
- `/books/{id}/` (GET, PUT, PATCH, DELETE)

## Кастомизация CBV

1. **Переопределение методов**
	```python
class BookList(ListCreateAPIView):
queryset = Book.objects.all()
serializer_class = BookSerializer

def perform_create(self, serializer):
	# Добавляем текущего пользователя как автора
	serializer.save(author=self.request.user)
```

2. Фильтрация и пагинация
```python
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'genre']
```

3. Права доступа
```python
from rest_framework.permissions import IsAuthenticated

class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
```

## Best Practices и Подводные камни

Практики:
- **APIView**: Используйте для нестандартной логики.
- **Generic-классы**: Для стандартных CRUD-операций.
- **ViewSet + Router**: Для минимизации кода и автоматизации маршрутов.
- **Миксины**: Для создания кастомных комбинаций поведения.

Подводные камни:
- **Порядок наследования миксинов**: Важен, так как методы могут переопределяться.
- **Избыточность**: Не используйте Generic-классы, если нужен полный контроль.
- **Производительность**: Оптимизируйте `queryset` (например, через `select_related` или `prefetch_related`).