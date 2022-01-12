from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from Apps.crm_app.models import ProjectsList, ClientsInfo

User = get_user_model()
model = User
# Create your tests here.

# from Apps.crm_app.forms import ClientsInfoForm
# from Apps.crm_app.views.client_views import ProjectUpdateView
from django.urls import reverse


class ProjectsTest(TestCase):

    def setUp(self):
        # create user
        self.user_1 = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        self.user_1.save()
        # create permission
        self.view_projectslist = Permission.objects.get(codename='view_projectslist')
        self.add_projectslist = Permission.objects.get(codename='add_projectslist')
        self.change_projectslist = Permission.objects.get(codename='change_projectslist')
        self.delete_projectslist = Permission.objects.get(codename='delete_projectslist')
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
        obj_client = ClientsInfo.objects.get(id=1)
        obj_project = ProjectsList.objects.get(id=1)

    def test_ProjectsListView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_projectslist)
        # check response from page (go to page)
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertEqual(response.context['title'], 'Projects List')