from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Task(models.Model):
    TYPE_CHOICES = (
        ("Заявка на ремонт", "Заявка на ремонт"),
        ("Обслуживание", "Обслуживание"),
        ("Консультация", "Консультация"),
    )
    STATUS_CHOICES = (
        ("Открытая", "Открытая"),
        ("В процессе", "В процессе"),
        ("Закрыта", "Закрыта"),
    )

    description = models.TextField("Описание заявки", max_length=1000, blank=False)
    date = models.DateField("Дата заявки", default=date.today, blank=False)
    author = models.ForeignKey(
        User,
        verbose_name="Владелец заявки",
        on_delete=models.CASCADE,
        blank=False,
        related_name="author_id",
    )
    type = models.CharField("Тип", choices=TYPE_CHOICES, blank=False, max_length=16)
    status = models.CharField("Тип", choices=STATUS_CHOICES, blank=True, max_length=16)
    worker = models.ForeignKey(
        User,
        verbose_name="Работник",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="worker_id",
        blank=True,
    )

    def __str__(self):
        return f"{self.author.username} — {self.type} — {str(self.date)}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
