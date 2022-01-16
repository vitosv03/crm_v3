from django.test import TestCase
from django.contrib.auth import get_user_model

# from unittest import main
User = get_user_model()
model = User

# Create your tests here.
# from ..models import Tags
from Apps.crm_app.models import ClientsInfo, ProjectsList


class ProjectsListModelTest(TestCase):
    test_model = ProjectsList
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
            client=client,
            p_name='myProject',
            description='myDescription',
            date_begin='2020-12-12',
            date_end='2021-12-12',
            value=50,
            created_by=user,
        )
        obj_1 = cls.test_model.objects.get(id=1)
        obj_2 = cls.test_client.objects.get(id=1)

    def test_is_active(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('is_active')
        self.assertEquals(field.verbose_name, 'is active')
        self.assertEquals(field.default, True)

    def test_client_field(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('client')
        self.assertEquals(field.verbose_name, 'client')

    def test_p_name(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('p_name')
        self.assertEquals(field.verbose_name, 'p name')
        self.assertEquals(field.max_length, 100)

    def test_description(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('description')
        self.assertEquals(field.verbose_name, 'description')

    def test_date_begin(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('date_begin')
        self.assertEquals(field.verbose_name, 'date begin')

    def test_date_end(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('date_end')
        self.assertEquals(field.verbose_name, 'date end')

    def test_value_field(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('value')
        self.assertEquals(field.verbose_name, 'value')
        self.assertEquals(field.max_digits, 10)
        self.assertEquals(field.decimal_places, 2)

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
    def test_object_name_p_name(self):
        obj = self.test_model.objects.get(id=1)
        expected_object_name = obj.p_name
        self.assertEquals(expected_object_name, str(obj))

    def test_get_absolute_url(self):
        obj = self.test_model.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(obj.get_absolute_url(), '/crm/project/1/detail/')