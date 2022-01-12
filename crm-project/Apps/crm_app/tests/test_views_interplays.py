from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from Apps.crm_app.models import ProjectsList, ClientsInfo, Tags, InterPlaysList

User = get_user_model()
model = User
# Create your tests here.

# from Apps.crm_app.forms import ClientsInfoForm
from Apps.crm_app.views.interplay_views import InterplayUpdateView, InterplayDeleteView
from django.urls import reverse


class InterPlaysListTest(TestCase):
    def setUp(self):
        # create user
        self.user_1 = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        self.user_1.save()
        # create permission
        self.view_interplays = Permission.objects.get(codename='view_interplayslist')
        self.add_interplays = Permission.objects.get(codename='add_interplayslist')
        self.change_interplays = Permission.objects.get(codename='change_interplayslist')
        self.delete_interplays = Permission.objects.get(codename='delete_interplayslist')
        self.user_1.save()
        # login user to our site
        login = self.client.login(username='TestUser', password='PyPass-99')
        # create new client
        self.myClient = ClientsInfo.objects.create(
            title='Company',
            head='Big Boss',
            summary='mySummary',
            address='Street',
            created_by=self.user_1,
        )
        # create new Project
        self.myProject = ProjectsList.objects.create(
            client=self.myClient,
            p_name='myProject',
            description='myDescription',
            date_begin='2020-12-12',
            date_end='2021-12-12',
            value=50,
            created_by=self.user_1,
        )
        # create new tag_1
        self.tag_1 = Tags.objects.create(
            tag='tag_1',
            created_by=self.user_1
        )
        # create new tag_2
        self.tag_2 = Tags.objects.create(
            tag='tag_2',
            created_by=self.user_1
        )
        # create new interplay
        self.myInterplay = InterPlaysList.objects.create(
            project=self.myProject,
            link='cl',
            rating=0,
            created_by=self.user_1,
        )
        obj_client = ClientsInfo.objects.get(id=1)
        obj_project = ProjectsList.objects.get(id=1)
        obj_interplay = InterPlaysList.objects.get(id=1)
        obj_tag_1 = Tags.objects.get(id=1)
        obj_tag_2 = Tags.objects.get(id=2)

    def test_InterPlaysListListView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_interplays)
        # check response from page (go to page)
        response = self.client.get(reverse('interplay_list'))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertEqual(response.context['title'], 'Interplays List')

    def test_InterPlaysListDetailView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_interplays)
        # check response from page (go to page)
        response = self.client.get(reverse('interplay_detail', kwargs={'pk': self.myInterplay.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Detail of'))
        owner = self.myInterplay.created_by == self.user_1
        self.assertTrue(response.context['owner'] == owner)

