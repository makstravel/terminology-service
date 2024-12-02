from django.db import models
from django.utils.translation import gettext_lazy as _


class RefBook(models.Model):
    """
    Модель для справочников.
    """
    code = models.CharField(max_length=100, blank=False, unique=True, verbose_name=_("Код"),
                            help_text=_("Уникальный код справочника."))
    name = models.CharField(max_length=300, blank=False, verbose_name=_("Наименование"),
                            help_text=_("Наименование справочника."))
    description = models.TextField(blank=True, verbose_name=_("Описание"), help_text=_("Описание справочника."))

    class Meta:
        verbose_name = _("Справочник")
        verbose_name_plural = _("Справочники")

    def __str__(self):
        return self.name


class Version(models.Model):
    """
    Модель для версияй справочников.

    """
    refbook = models.ForeignKey(RefBook, on_delete=models.CASCADE, related_name="versions",
                                verbose_name=_("Справочник"))
    version = models.CharField(max_length=50, blank=False, verbose_name=_("Версия"))
    start_date = models.DateField(verbose_name=_("Дата начала действия версии"))

    class Meta:
        verbose_name = _("Версия справочника")
        verbose_name_plural = _("Версии справочников")
        unique_together = ("refbook", "version")  # Уникальность комбинации справочника и версии
        constraints = [
            models.UniqueConstraint(
                fields=["refbook", "start_date"],
                name="unique_start_date_per_refbook"
            )
        ]
        ordering = ["-start_date", "version"]

    def __str__(self):
        return f"{self.refbook.name} - {self.version}"


class Element(models.Model):
    """
    Модель для хранения элементов
    """
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name="elements", verbose_name=_("Версия"))
    code = models.CharField(max_length=100, blank=False, verbose_name=_("Код элемента"))
    value = models.CharField(max_length=300, blank=False, verbose_name=_("Значение элемента"))

    class Meta:
        verbose_name = _("Элемент справочника")
        verbose_name_plural = _("Элементы справочников")
        unique_together = ("version", "code")
        constraints = [
            models.UniqueConstraint(
                fields=["version", "code"],
                name="unique_code_per_version"
            )
        ]
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.value}"
