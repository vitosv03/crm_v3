from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from Apps.crm_app.models import ClientsInfo

User = get_user_model()
model = User
# Create your tests here.

# from Apps.crm_app.models import ClientsInfo, ClientsPhones, ClientsEmails
# from Apps.crm_app.views.client_views import ClientListView_2
from Apps.crm_app.views.tag_views import TagUpdateView
from django.urls import reverse


class ClientInfoTest(TestCase):

    def setUp(self):
        # create user
        self.user_1 = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        self.user_1.save()
        # create permission
        self.view_clientsinfo = Permission.objects.get(codename='view_clientsinfo')
        self.add_clientsinfo = Permission.objects.get(codename='add_clientsinfo')
        self.change_clientsinfo = Permission.objects.get(codename='change_clientsinfo')
        self.delete_clientsinfo = Permission.objects.get(codename='delete_clientsinfo')
        self.user_1.save()
        # login user to our site
        login = self.client.login(username='TestUser', password='PyPass-99')
        # create new tag
        self.myClient = ClientsInfo.objects.create(
            title='Company',
            head='Big Boss',
            summary='mySummary',
            address='Street',
            created_by=self.user_1,
        )
        obj = ClientsInfo.objects.get(id=1)

    def test_ClientInfoListView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_clientsinfo)
        # check response from page (go to page)
        response = self.client.get(reverse('client_list_2'))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertEqual(response.context['title'], 'Clients List_2')

    def test_ClientInfoDetailView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_clientsinfo)
        # check response from page (go to page)
        response = self.client.get(reverse('client_detail', kwargs={'pk': self.myClient.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Detail of:'))
        owner = self.myClient.created_by == self.user_1
        self.assertTrue(response.context['owner'] == owner)