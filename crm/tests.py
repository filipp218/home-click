from django.http import QueryDict
from django.test import TestCase, RequestFactory
from .models import Task
import factory
from django.contrib.auth.models import User, AnonymousUser
from .views import MainView, TaskCreate, ClientList, WorkerList, TaskInProcess, TaskDone


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class CrmTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory(username="Filipp", is_staff=True)
        self.user2 = UserFactory(username="Sergey", is_staff=True)
        self.user3 = UserFactory(username="Andrey", is_staff=False)
        self.user4 = AnonymousUser()
        user = User.objects.get(username="Andrey")

    def test_response_main_worker(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user1
        response = MainView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/worker")

    def test_response_main_client(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user3
        response = MainView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/client")

    def test_response_main_unknown(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user4
        response = MainView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_task_create(self):
        form = {
            "description": "asdadasda",
            "type": "Обслуживание",
        }
        query_dict = QueryDict("", mutable=True)
        query_dict.update(form)
        factory = RequestFactory()
        request = factory.post("", query_dict)
        request.user = self.user3
        response = TaskCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_response_list_client(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user3
        response = ClientList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_list_client_anonym(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user4
        response = ClientList.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_response_list_worker_anonym(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user4
        response = WorkerList.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_response_list_worker(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user1
        response = WorkerList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_response_task_in_process(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user1
        TaskFactory(author=self.user3)
        id = Task.objects.get(author=self.user3)
        response = TaskInProcess.as_view()(request, pk=id.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/worker")

    def test_response_task_done(self):
        factory = RequestFactory()
        request = factory.get("")
        request.user = self.user1
        TaskFactory(author=self.user3, status="В процессе", worker=request.user)
        id = Task.objects.get(author=self.user3)
        response = TaskDone.as_view()(request, pk=id.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/worker")
