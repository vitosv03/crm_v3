from django.test import TestCase
from django.contrib.auth import get_user_model
# from unittest import main
User = get_user_model()
model = User

# Create your tests here.
# from ..models import Tags
from Apps.crm_app.models import ClientsEmails, ClientsInfo


class ClientsEmailsModelTest(TestCase):

    test_model = ClientsEmails
    test_client = ClientsInfo

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        user.save()

        client = cls.test_client.objects.create(
            title='Company',
            head='Big Boss',
            summary='mySummary',
            address='Street',
            created_by=user,
        )
        cls.test_model.objects.create(
            email='mail@gmail.com',
            client=client,
        )
        obj_1 = cls.test_model.objects.get(id=1)
        obj_2 = cls.test_client.objects.get(id=1)

    def test_email(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('email')
        self.assertEquals(field.verbose_name, 'email')
        self.assertEquals(field.max_length, 100)

    def test_client_field(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('client')
        self.assertEquals(field.verbose_name, 'client')

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
    def test_object_name_is_email(self):
        obj = self.test_model.objects.get(id=1)
        expected_object_name = obj.email
        self.assertEquals(expected_object_name, str(obj))