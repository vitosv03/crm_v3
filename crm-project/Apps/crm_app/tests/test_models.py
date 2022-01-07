from django.test import TestCase
# from unittest import main

# Create your tests here.
# from ..models import Tags
from Apps.crm_app.models import Tags


# class Tags(models.Model):
#     tag = models.CharField(max_length=20)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
#     date_created = models.DateTimeField(auto_now_add=True, blank=True)
#     date_updated = models.DateTimeField(auto_now=True, blank=True)
#
#     def get_absolute_url(self):
#         return reverse('tag_detail', args=[str(self.id)])
#
#     class Meta:
#         verbose_name = 'Tags'
#         verbose_name_plural = 'Tags'
#         ordering = ['-date_created']
#
#     def __str__(self):
#         return self.tag


class TagsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Tags.objects.create(tag='myNewTag', )
        tag = Tags.objects.get(id=1)

    def test_tag(self):
        tag = Tags.objects.get(id=1)
        field = Tags._meta.get_field('tag')
        self.assertEquals(field.verbose_name, 'tag')
        self.assertEquals(field.max_length, 20)

    def test_created_by(self):
        created_by = Tags.objects.get(id=1)
        field = Tags._meta.get_field('created_by')
        self.assertEquals(field.verbose_name, 'created by')
        self.assertEquals(field.blank, True)
        self.assertEquals(field.null, True)

    def test_date_created(self):
        date_created = Tags.objects.get(id=1)
        field = Tags._meta.get_field('date_created')
        self.assertEquals(field.verbose_name, 'date created')
        self.assertEquals(field.auto_now_add, True)
        self.assertEquals(field.blank, True)
        # self.assertEquals(field.blank, False)

    def test_date_updated(self):
        date_updated = Tags.objects.get(id=1)
        field = Tags._meta.get_field('date_updated')
        self.assertEquals(field.verbose_name, 'date updated')
        self.assertEquals(field.auto_now, True)
        self.assertEquals(field.blank, True)
        # self.assertEquals(field.blank, False)

    # def __str__(self):
    def test_object_name_is_tag(self):
        tag = Tags.objects.get(id=1)
        expected_object_name = tag.tag
        self.assertEquals(expected_object_name, str(tag))

    def test_get_absolute_url(self):
        tag = Tags.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(tag.get_absolute_url(), '/crm/tag/1/detail/')

