from django.test import TestCase
# from unittest import main


from Apps.users_app.models import Users


class UsersModelTest(TestCase):

    test_model = Users

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.test_model.objects.create(username='newUser', )
        obj = cls.test_model.objects.get(id=1)

    def test_image(self):
        obj = self.test_model.objects.get(id=1)
        field = self.test_model._meta.get_field('image')
        self.assertEquals(field.verbose_name, 'image')
        self.assertEquals(field.upload_to, 'users_photo/')
        self.assertEquals(field.blank, True)

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
    def test_object_name_is_username(self):
        obj = self.test_model.objects.get(id=1)
        expected_object_name = obj.username
        self.assertEquals(expected_object_name, str(obj))

