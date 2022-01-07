from django.test import TestCase
# from unittest import main

# Create your tests here.
from Apps.crm_app.models import Tags
# from ..models import Tags


class TagsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Tags.objects.create(tag='myNewTag', )
        tag = Tags.objects.get(id=1)

    def test_tag_label(self):
        tag = Tags.objects.get(id=1)
        field_label = Tags._meta.get_field('tag').verbose_name
        self.assertEquals(field_label, 'tag')

    def test_created_by_label(self):
        created_by = Tags.objects.get(id=1)
        field_label = Tags._meta.get_field('created_by').verbose_name
        self.assertEquals(field_label, 'created by')

    def test_date_created_label(self):
        date_created = Tags.objects.get(id=1)
        field_label = Tags._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_date_updated_label(self):
        date_updated = Tags.objects.get(id=1)
        field_label = Tags._meta.get_field('date_updated').verbose_name
        self.assertEquals(field_label, 'date updated')

    def test_tag_max_length(self):
        tag = Tags.objects.get(id=1)
        max_length = Tags._meta.get_field('tag').max_length
        self.assertEquals(max_length, 20)

    def test_date_created_auto_now_add(self):
        tag = Tags.objects.get(id=1)
        auto_now_add = Tags._meta.get_field('date_created').auto_now_add
        self.assertEquals(auto_now_add, True)

    def test_date_updated_auto_now(self):
        tag = Tags.objects.get(id=1)
        auto_now = Tags._meta.get_field('date_updated').auto_now
        self.assertEquals(auto_now, True)

    # def test_date_created_blank(self):
    #     # tag = Tags.objects.get(id=1)
    #     blank = Tags._meta.get_field('date_created').blank
    #     self.assertEquals(blank, False)
    #
    # def test_date_updated_blank(self):
    #     # tag = Tags.objects.get(id=1)
    #     blank = Tags._meta.get_field('date_updated').blank
    #     self.assertEquals(blank, False)

    def test_created_by_blank_null_is_true(self):
        tag = Tags.objects.get(id=1)
        blank = Tags._meta.get_field('created_by').blank
        null = Tags._meta.get_field('created_by').null
        self.assertEquals(blank, True)
        self.assertEquals(null, True)

    # # -------------------------------
    #     def test_created_by_label_blank_null(self):
    #         field = Tags._meta.get_field('created_by')
    #         self.assertEquals(field.verbose_name, 'created by')
    #         self.assertEquals(field.blank, True)
    #         self.assertEquals(field.null, True)
    #
    #
    #     def test_created_by_label(self):
    #         field_label = Tags._meta.get_field('created_by').verbose_name
    #         self.assertEquals(field_label, 'created by')
    #
    #     def test_created_by_blank(self):
    #         blank = Tags._meta.get_field('created_by').blank
    #         self.assertEquals(blank, True)
    #
    #     def test_created_by_null(self):
    #         null = Tags._meta.get_field('created_by').null
    #         self.assertEquals(null, True)
    # # -------------------------------

    # def __str__(self):
    def test_object_name_is_tag(self):
        tag = Tags.objects.get(id=1)
        expected_object_name = tag.tag
        self.assertEquals(expected_object_name, str(tag))

    def test_get_absolute_url(self):
        tag = Tags.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(tag.get_absolute_url(), '/crm/tag/1/detail/')

    # if __name__ == '__main__':
    #     main()
