from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название Категории")
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="Изображение Категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя Автора")
    description = models.TextField(blank=True, verbose_name="О Авторе")
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="Изображение Автора")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Series(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название Серии")
    description = models.TextField(blank=True, verbose_name="Описание")
    authors = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="series", verbose_name="Автор")
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="Изображение Серии")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Серия"
        verbose_name_plural = "Серии"

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название Книги")
    categories = models.ManyToManyField(Category, related_name="books", verbose_name="Категории")
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="Изображение Книги")
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Серия")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Автор")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    ebook_file = models.FileField(upload_to='books/ebooks/', verbose_name="Файл Книги (Ebook)")
    year_published = models.CharField(max_length=200, verbose_name="Год Публикации Книги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата Заказа")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Сумма Заказа")
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'В ожидании'),
            ('processing', 'В обработке'),
            ('shipped', 'Отправлен'),
            ('completed', 'Завершен'),
            ('cancelled', 'Отменен'),
        ],
        default='pending',
        verbose_name="Статус Заказа"
    )
    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за Единицу") # Store price at time of order
    # You might also store other details from the book at the time of the order (e.g., discount)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} в заказе #{self.order.pk}"

    class Meta:
        verbose_name = "Элемент Заказа"
        verbose_name_plural = "Элементы Заказа"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment", verbose_name="Заказ")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата Оплаты")
    payment_method = models.CharField(max_length=100, verbose_name="Способ Оплаты")  # e.g., "Credit Card", "PayPal"
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма Оплаты")
    transaction_id = models.CharField(max_length=200, blank=True, verbose_name="ID Транзакции")
    status = models.CharField(max_length=50, default="pending", verbose_name="Статус Оплаты") # e.g., "pending", "completed", "failed"

    def __str__(self):
        return f"Оплата заказа #{self.order.pk} ({self.status})"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
