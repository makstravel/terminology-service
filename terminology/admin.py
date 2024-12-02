from django.contrib import admin
from .models import RefBook, Version, Element


class ElementInline(admin.TabularInline):
    """
    отображение элементов справочника
    """
    model = Element
    extra = 1  # Количество пустых строк для добавления новых записей
    fields = ['code', 'value']  # Поля, отображаемые в интерфейсе
    min_num = 0  # Минимальное количество записей
    verbose_name = "Элемент справочника"
    verbose_name_plural = "Элементы справочника"


class VersionInline(admin.TabularInline):
    """
    отображение версий справочника
    """
    model = Version
    extra = 1  # Количество пустых строк для добавления новых записей
    fields = ['version', 'start_date']  # Поля, отображаемые в интерфейсе
    show_change_link = True  # Включает ссылку для редактирования версии
    verbose_name = "Версия справочника"
    verbose_name_plural = "Версии справочника"


@admin.register(RefBook)
class RefbookAdmin(admin.ModelAdmin):
    """
    редактирования справочников
    """
    list_display = ('id', 'code', 'name', 'get_current_version', 'get_current_version_start_date')
    search_fields = ('code', 'name')  # Поля для поиска
    fields = ['code', 'name', 'description']  # Поля для редактирования справочника
    inlines = [VersionInline]  # Включение отображения версий

    def get_current_version(self, obj):
        """
        текущая версии справочника
        """
        current_version = obj.versions.order_by('-start_date').first()
        return current_version.version if current_version else None

    get_current_version.short_description = "Текущая версия"

    def get_current_version_start_date(self, obj):
        """
        дата начала действия текущей версии
        """
        current_version = obj.versions.order_by('-start_date').first()
        return current_version.start_date if current_version else None

    get_current_version_start_date.short_description = "Дата начала текущей версии"


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """
    редактирования версий справочников
    """
    list_display = ('id', 'refbook', 'version', 'start_date')
    search_fields = ('version',)
    fields = ['refbook', 'version', 'start_date']
    inlines = [ElementInline]  # Включение отображения элементов


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    """
    редактирования элементов справочников.
    """
    list_display = ('id', 'version', 'code', 'value')
    search_fields = ('code', 'value')
    fields = ['version', 'code', 'value']
