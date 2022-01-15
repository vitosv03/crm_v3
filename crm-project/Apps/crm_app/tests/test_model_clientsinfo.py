from django.test import TestCase
from django.contrib.auth import get_user_model
# from unittest import main
User = get_user_model()
model = User

# Create your tests here.
# from ..models import Tags
from Apps.crm_app.models import ClientsInfo, ClientsEmails, ClientsPhones


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

    def setUp(self):
        # create user
        self.user_1 = User.objects.create_user(username='TestUser_2', email='lekt_2@ukr.net', password='PyPass-99')
        self.user_1.save()
        self.user_1.save()
        # create new client
        self.client_1 = ClientsInfo.objects.create(
            title='Company_2',
            head='Big Boss_2',
            summary='mySummary_2',
            address='Street_2',
            created_by=self.user_1,
        )

        # create new email_1
        self.email_1 = ClientsEmails.objects.create(email='mail_1@gmail.com', client=self.client_1,)
        # create new email_2
        self.email_2 = ClientsEmails.objects.create(email='mail_2@gmail.com', client=self.client_1,)

        # create new phone_1
        self.phone_1 = ClientsPhones.objects.create(phoneNumber='+380991234567', client=self.client_1,)
        # create new phone_2
        self.phone_2 = ClientsPhones.objects.create(phoneNumber='+380991234560', client=self.client_1,)


        obj_client_2 = ClientsEmails.objects.get(id=2)
        obj_email_1 = ClientsEmails.objects.get(id=1)
        obj_email_2 = ClientsEmails.objects.get(id=2)
        obj_phone_1 = ClientsPhones.objects.get(id=1)
        obj_phone_2 = ClientsPhones.objects.get(id=2)

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

    def test_display_email(self):
        obj_client_2 = ClientsInfo.objects.get(id=2)
        obj_email_1 = ClientsEmails.objects.get(id=1)
        obj_email_2 = ClientsEmails.objects.get(id=2)
        list_emails = ClientsEmails.objects.all().values_list('email', flat=True)
        emails = ", ".join([e for e in list_emails])
        self.assertEquals(obj_client_2.display_email(), emails)

    def test_display_phoneNumber(self):
        obj_client_2 = ClientsInfo.objects.get(id=2)
        obj_phone_1 = ClientsPhones.objects.get(id=1)
        obj_phone_2 = ClientsPhones.objects.get(id=2)
        list_phones = ClientsPhones.objects.all().values_list('phoneNumber', flat=True)
        phones = ", ".join([e for e in list_phones])
        self.assertEquals(obj_client_2.display_phoneNumber(), phones)