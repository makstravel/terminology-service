from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status
from .models import RefBook, Version, Element


# тестовые данные
class RefbookAPITest(APITestCase):
    def setUp(self):
        self.refbook = RefBook.objects.create(
            code="test_code", name="Test RefBook", description="Test Description"
        )
        self.version1 = Version.objects.create(
            refbook=self.refbook, version="1.0", start_date=date(2023, 1, 1)
        )
        self.version2 = Version.objects.create(
            refbook=self.refbook, version="2.0", start_date=date(2023, 6, 1)
        )
        self.element1 = Element.objects.create(
            version=self.version1, code="E001", value="Element 1"
        )
        self.element2 = Element.objects.create(
            version=self.version2, code="E002", value="Element 2"
        )

    def test_refbook_list(self):
        # тестируем списка справочников по дате
        response = self.client.get('/api/refbooks/?date=2023-07-01')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["refbooks"]), 1)

    def test_element_list(self):
        # тестируем получения элементов по указанной версии
        response = self.client.get(f'/api/refbooks/{self.refbook.id}/elements/?version=1.0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)
        self.assertEqual(response.data['elements'][0]['code'], 'E001')

    def test_validate_element_valid(self):
        # тестируем проверки валидного элемента
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/check_element/?version=1.0&code=E001&value=Element 1'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_valid'])

    def test_validate_element_invalid(self):
        # тестируем проверки невалидного элемента
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/check_element/?version=1.0&code=E999&value=Invalid'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_valid'])




