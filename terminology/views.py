from datetime import date, datetime

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import RefBook, Version, Element
from .serializers import RefbookSerializer, ElementSerializer
from drf_yasg.utils import swagger_auto_schema


class ElementService:

    @staticmethod
    def get_version(refbook, version=None):
        """
        получение версии справочника.
        """
        if version:
            # если указали версию то находим ее
            return refbook.versions.get(version=version)
        else:
            # если версия не указана, то берем последнюю версию справочника
            return refbook.versions.filter(start_date__lte=date.today()).order_by('-start_date').first()


class RefbookListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить все справочники",
    )
    def get(self, request):
        date_str = request.query_params.get('date', None)
        try:
            # Преобразуем строку в дату
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Не правильный формат данных, используйте YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        # справочники, у которых есть версия на указанную дату
        refbooks = RefBook.objects.all()
        filtered_refbooks = []

        for refbook in refbooks:
            # есть ли версия, актуальная на указанную дату
            active_version = refbook.versions.filter(start_date__lte=filter_date).order_by('-start_date').first()
            if active_version:
                filtered_refbooks.append(refbook)

        serializer = RefbookSerializer(filtered_refbooks, many=True)
        return Response({"refbooks": serializer.data}, status=status.HTTP_200_OK)


class ElementListView(APIView):
    """
    Получение элементов заданного справочника.
    """
    @swagger_auto_schema(
        operation_description="Получение элементов по версии",
    )
    def get(self, request, id):
        # получаем версию из параметров запроса
        version = request.query_params.get("version")
        refbook = RefBook.objects.filter(id=id).first()

        if not refbook:
            return Response({'error': 'RefBook not found'}, status=status.HTTP_404_NOT_FOUND)

        # используем метод из класса ElementListView
        version_obj = ElementService.get_version(refbook, version)

        # получение всех элементов справочника которые относятся к нужной версии
        elements = Element.objects.filter(version=version_obj)

        # сериализация списка элементов справочника
        serializer = ElementSerializer(elements, many=True)
        return Response({'elements': serializer.data}, status=status.HTTP_200_OK)


class ValidateElementView(APIView):
    """
    Валидация элемента справочника
    """
    @swagger_auto_schema(
        operation_description="Проверка наличия элемента в справочнике",
    )
    def get(self, request, id):
        # получаем код и значение из параметров запроса
        code = request.query_params.get('code')
        value = request.query_params.get('value')
        # получаем версию из параметров
        version = request.query_params.get('version')

        # проверка наличия справочника
        refbook = RefBook.objects.filter(id=id).first()

        if not refbook:
            return Response({'error': 'RefBook not found'}, status=status.HTTP_404_NOT_FOUND)

        # используем метод из другого класса
        version_obj = ElementService.get_version(refbook, version)

        if not version_obj:
            return Response({'error': 'Version not found'}, status=status.HTTP_404_NOT_FOUND)

        # если есть код и значение то проверяем их наличие
        if code and value:
            is_valid = Element.objects.filter(version=version_obj, code=code, value=value).exists()
            return Response({'is_valid': is_valid}, status=status.HTTP_200_OK)
        else:
            return Response({'is_valid': False}, status=status.HTTP_400_BAD_REQUEST)
