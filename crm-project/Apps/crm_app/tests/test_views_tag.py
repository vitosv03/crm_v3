from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.auth import get_user_model

from Apps.crm_app.models import Tags

User = get_user_model()
model = User
# Create your tests here.

# from Apps.crm_app.models import ClientsInfo, ClientsPhones, ClientsEmails
# from Apps.crm_app.views.client_views import ClientListView_2
from Apps.crm_app.views.tag_views import TagUpdateView, TagDeleteView
from django.urls import reverse


class TagsTest(TestCase):

    def setUp(self):
        # create user
        self.user_1 = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        self.user_1.save()
        # create permission
        self.view_tags = Permission.objects.get(codename='view_tags')
        self.add_tags = Permission.objects.get(codename='add_tags')
        self.change_tags = Permission.objects.get(codename='change_tags')
        self.delete_tags = Permission.objects.get(codename='delete_tags')
        self.user_1.save()
        # login user to our site
        login = self.client.login(username='TestUser', password='PyPass-99')
        # create new tag
        self.myNewTag = Tags.objects.create(tag='myNewTag', created_by=self.user_1)
        obj = Tags.objects.get(id=1)

    def test_TagListView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_tags)
        # check response from page (go to page)
        response = self.client.get(reverse('tag_list'))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertEqual(response.context['title'], 'Tags List')

    def test_TagDetailView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_tags)
        # check response from page (go to page)
        response = self.client.get(reverse('tag_detail', kwargs={'pk': self.myNewTag.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Detail of:'))
        owner = self.myNewTag.created_by == self.user_1
        self.assertTrue(response.context['owner'] == owner)

    def test_TagAddView(self):
        # add permission
        self.user_1.user_permissions.add(self.add_tags)
        # check response from page (go to page)
        response = self.client.get(reverse('tag_add'))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertEqual(response.context['title'], 'Add new Tag')

    def test_TagUpdateView(self):
        # add permission
        self.user_1.user_permissions.add(self.change_tags)
        # check response from page (go to page)
        response = self.client.get(reverse('tag_update', kwargs={'pk': self.myNewTag.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Update of'))
        # check url for get_queryset
        url = '/crm/tag/' + str(self.myNewTag.pk) + '/update/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check get_queryset
        request = RequestFactory().get(url)
        request.user = self.user_1
        view = TagUpdateView()
        view.setup(request)
        qs = view.get_queryset()
        qs_original = Tags.objects.filter(created_by=request.user)
        self.assertQuerysetEqual(qs, qs_original)

    def test_TagDeleteView(self):
        # add permission
        self.user_1.user_permissions.add(self.delete_tags)
        # check response from page (go to page)
        response = self.client.get(reverse('tag_delete', kwargs={'pk': self.myNewTag.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Delete of'))
        # check url for get_queryset
        url = '/crm/tag/' + str(self.myNewTag.pk) + '/delete/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check get_queryset
        request = RequestFactory().get(url)
        request.user = self.user_1
        view = TagDeleteView()
        view.setup(request)
        qs = view.get_queryset()
        qs_original = Tags.objects.filter(created_by=request.user)
        self.assertQuerysetEqual(qs, qs_original)
