from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from Apps.crm_app.models import ProjectsList, ClientsInfo

User = get_user_model()
model = User
# Create your tests here.

# from Apps.crm_app.forms import ClientsInfoForm
from Apps.crm_app.views.project_views import ProjectUpdateView, ProjectDeleteView
from django.urls import reverse


class ProjectsTest(TestCase):

    def setUp(self):
        self.client = Client()

        # create user
        self.user_1 = User.objects.create_user(username='TestUser', email='lekt@ukr.net', password='PyPass-99')
        self.user_1.save()
        # create permission
        self.view_projectslist = Permission.objects.get(codename='view_projectslist')
        self.add_projectlist = Permission.objects.get(codename='add_projectslist')
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

        # self.factory = RequestFactory()
        # self.good_request = self.factory.post(
        #     '/crm/project/' + str(self.myProject.pk) + '/update/',
        #     data={
        #         # 'client': self.myClient,
        #         'p_name': 'myProject_new',
        #         'description': 'myDescription_1',
        #         'date_begin': '2020-12-12',
        #         'date_end': '2021-12-12',
        #         'value': 500,
        #         # 'created_by': self.user_1,
        #     }
        # )
        # self.good_request.user = self.user_1



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

    def test_ProjectsDetailView(self):
        # add permission
        self.user_1.user_permissions.add(self.view_projectslist)
        # check response from page (go to page)
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.myProject.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Detail of'))
        owner = self.myProject.created_by == self.user_1
        self.assertTrue(response.context['owner'] == owner)

    def test_ProjectsAddView(self):
        # add permission
        self.user_1.user_permissions.add(self.add_projectlist)
        # check response from page (go to page)
        response = self.client.get(reverse('project_add'))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertEqual(response.context['title'], 'Add new Project')




    def test_ProjectsUpdateView(self):
        # add permission
        self.user_1.user_permissions.add(self.change_projectslist)
        # check response from page (go to page)
        response = self.client.get(reverse('project_update', kwargs={'pk': self.myProject.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Update of'))
        # check url for get_queryset
        url = '/crm/project/' + str(self.myProject.pk) + '/update/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # check get_queryset
        request = RequestFactory().get(url)
        request.user = self.user_1
        view = ProjectUpdateView()
        view.setup(request)
        qs = view.get_queryset()
        qs_original = ProjectsList.objects.filter(created_by=request.user)
        self.assertQuerysetEqual(qs, qs_original)


        # factory = RequestFactory()
        # print('/crm/project/' + str(self.myProject.pk) + '/update/')
        # good_request = factory.post(
        #     # reverse('project_update', kwargs={'pk': self.myProject.pk, }),
        #     '/crm/project/' + str(self.myProject.pk) + '/update/',
        #     data={
        #         # 'client': self.myClient,
        #         'p_name': 'myProject_new',
        #         'description': 'myDescription_1',
        #         'date_begin': '2020-12-12',
        #         'date_end': '2021-12-12',
        #         'value': 500,
        #         # 'created_by': self.user_1,
        #     }
        # )
        # self.good_request.user = self.user_1
        # resp = ProjectUpdateView.as_view()(self.good_request)
        # self.assertEquals(response.status_code, 302)

        # login = self.client.login(username='TestUser', password='PyPass-99')
        #
        # # request = RequestFactory().post(url)
        # # request.data = {
        # #     'client': self.myClient,
        # #     'p_name': 'myProject_new',
        # #     'description': 'myDescription_1',
        # #     'date_begin': '2020-12-12',
        # #     'date_end': '2021-12-12',
        # #     'value': 500,
        # #     'created_by': self.user_1,
        # # }
        # # response = view(request)
        # # print(response)
        #
        # # def test_my_update(self):
        # myProject = ProjectsList.objects.create(
        #     client=self.myClient,
        #     p_name='myProject_1',
        #     description='myDescription_1',
        #     date_begin='2020-12-12',
        #     date_end='2021-12-12',
        #     value=500,
        #     created_by=self.user_1,
        # )
        # # myProject.save()
        # obj_project_1 = ProjectsList.objects.get(id=self.myProject.pk)
        # print(obj_project_1)
        # url = reverse('project_update', kwargs={'pk': self.myProject.pk, })
        # # print(url)
        # response = self.client.post(url, {
        #     # 'client': self.myClient,
        #     # 'p_name': 'myProject_new',
        #     'description': 'myDescription_1',
        #     'date_begin': '2020-12-12',
        #     'date_end': '2021-12-12',
        #     'value': 500,
        #     # 'created_by': self.user_1,
        # })
        #
        # # myProject.save()
        #
        # self.assertEqual(response.status_code, 200)
        # # myProject.refresh_from_db()
        # obj_project = ProjectsList.objects.get(id=self.myProject.pk)
        # print(obj_project)
        # self.assertEqual(self.myProject.p_name, 'myProject')

    def test_ProjectsDeleteView(self):
        # add permission
        self.user_1.user_permissions.add(self.delete_projectslist)
        # check response from page (go to page)
        response = self.client.get(reverse('project_delete', kwargs={'pk': self.myProject.pk, }))
        self.assertEqual(response.status_code, 200)
        # check get_context_data
        self.assertTrue(response.context['title'].startswith('Delete of'))
        # check url for get_queryset
        url = '/crm/project/' + str(self.myProject.pk) + '/delete/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check get_queryset
        request = RequestFactory().get(url)
        request.user = self.user_1
        view = ProjectDeleteView()
        view.setup(request)
        qs = view.get_queryset()
        qs_original = ProjectsList.objects.filter(created_by=request.user)
        self.assertQuerysetEqual(qs, qs_original)
