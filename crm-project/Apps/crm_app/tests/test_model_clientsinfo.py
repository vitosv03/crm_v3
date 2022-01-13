from django.test import TestCase
from django.contrib.auth import get_user_model
# from unittest import main
User = get_user_model()
model = User

# Create your tests here.
# from ..models import Tags
from Apps.crm_app.models import ClientsInfo


class ClientsInfoModelTest(TestCase):

    test_model = ClientsInfo

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        user.save()
        cls.test_model.objects.create(
            title='Company',
            head='Big Boss',
            summary='mySummary',
            address='Street',
            created_by=user,
        )
        obj = cls.test_model.objects.get(id=1)

    def test_is_active(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('is_active')
        self.assertEquals(field.verbose_name, 'is active')
        self.assertEquals(field.default, True)

    def test_title(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('title')
        self.assertEquals(field.verbose_name, 'title')
        self.assertEquals(field.max_length, 100)

    def test_head(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('head')
        self.assertEquals(field.verbose_name, 'head')
        self.assertEquals(field.max_length, 100)

    def test_summary(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('summary')
        self.assertEquals(field.verbose_name, 'summary')
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)

    def test_address(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('address')
        self.assertEquals(field.verbose_name, 'address')
        self.assertEquals(field.max_length, 100)

    def test_created_by(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('created_by')
        self.assertEquals(field.verbose_name, 'created by')
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)

    def test_date_created(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('date_created')
        self.assertEquals(field.verbose_name, 'date created')
        self.assertEquals(field.auto_now_add, True)
        self.assertEquals(field.blank, True)
        # self.assertEquals(field.blank, False)

    def test_date_updated(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('date_updated')
        self.assertEquals(field.verbose_name, 'date updated')
        self.assertEquals(field.auto_now, True)
        self.assertEquals(field.blank, True)
        # self.assertEquals(field.blank, False)

    # def __str__(self):
    def test_object_name_is_title(self):
        obj = self.test_model.objects.get(id=1)
        expected_object_name = obj.title
        self.assertEquals(expected_object_name, str(obj))

    def test_get_absolute_url(self):
        obj = self.test_model.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(obj.get_absolute_url(), '/crm/client/1/detail/')