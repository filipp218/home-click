from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth import login, authenticate, logout
from .forms import AuthProfileForm, ProfileForm, AuthorForm
from .models import Task
from django.db.models import Q


class MainView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(
                request, "crm/main.html", {}
            )
        elif request.user.is_authenticated and not request.user.is_staff:
            return redirect(f"/client")

        elif request.user.is_authenticated and request.user.is_staff:
            return redirect(f"/worker")


class ProfileLogin(View):
    def get(self, request):
        form = AuthProfileForm()
        data = {'form': form}
        return render(request, 'crm/auth.html', data)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if request.path == '/client/auth':
            if user and user.is_active:
                login(request, user)
                return redirect(f"/client")
        elif request.path == '/worker/auth':
            if user and user.is_active and user.is_staff:
                login(request, user)
                return redirect(f"/worker")

        form = AuthProfileForm(request.POST)
        error = "The username or password were incorrect"
        data = {'error': error, 'form' : form}
        return render(request, 'crm/auth.html', data)


class ProfileLogout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class NewProfile(View):

    def get(self, request):
        if not request.path == '/client/registration':
            return redirect("/")
        form = ProfileForm()
        data = {'form': form}
        return render(request, 'crm/auth.html', data)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            username,password = form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        form = ProfileForm()
        error = "Какое-то поле не пустое или такой логин уже есть"
        data = {'error': error, 'form': form}
        return render(request, 'crm/auth.html', data)

class TaskCreate(CreateView):
    form_class = AuthorForm
    model = Task
    context_object_name = "form"
    success_url = "/"
    template_name = "crm/task_add.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'Открытая'
        return super(TaskCreate, self).form_valid(form)


class ClientList(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        queryset = Task.objects.filter(author=request.user)
        data = {"tasks":queryset}
        if not queryset:
            data["error"] = 'Пока вы не оставили ни одной заявки'
        return render(request, "crm/client_task.html", data)


class Types:

    def get_types(self):
        return Task.TYPE_CHOICES

    def get_status(self):
        return Task.STATUS_CHOICES


class WorkerList(ListView, Types):
    model = Task
    context_object_name = "tasks"
    template_name = "crm/worker_list.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):

        queryset = Task.objects.all()
        filters = Q()
        if "type" in self.request.GET and "status" in self.request.GET:
            types = self.request.GET.getlist("type")
            status = self.request.GET.getlist("status")
            for typ in types:
                for stat in status:
                    filters |= Q(type=typ, status=stat)

        elif "type" in self.request.GET:
            types = self.request.GET.getlist("type")
            for i in types:
                filters |= Q(type=i)

        elif "status" in self.request.GET:
            status = self.request.GET.getlist("status")
            for i in status:
                filters |= Q(status=i)
        if "from_date" in self.request.GET:
            date = self.request.GET["from_date"]
            if date:
                date = datetime.strptime(date,"%Y-%m-%d")
                queryset = queryset.filter(date__gte=date)
        if "to_date" in self.request.GET:
            date = self.request.GET["to_date"]
            if date:
                date = datetime.strptime(date,"%Y-%m-%d")
                queryset = queryset.filter(date__lte=date)
        queryset = queryset.filter(filters)
        return queryset


class TaskInProcess(View):
    def get(self, request, pk):
        if not request.user.is_staff:
            redirect('/')
        task = Task.objects.get(id=pk)
        task.status = 'В процессе'
        task.worker = request.user
        task.save()
        return redirect('/worker')

class TaskDone(View):
    def get(self, request, pk):
        if not request.user.is_staff:
            redirect('/')
        task = Task.objects.get(id=pk)
        if request.user == task.worker:
            task.status = 'Закрыта'
            task.worker = request.user
            task.save()
        return redirect('/worker')


class WorkerListId(ListView, Types):
    model = Task
    context_object_name = "tasks"
    template_name = "crm/worker_list.html"

    def get_queryset(self):
        if self.request.user.id == self.kwargs['pk']:
            queryset = Task.objects.filter(worker_id=self.kwargs['pk'])
        else:
            queryset = Task.objects.all()

        filters = Q()
        if "type" in self.request.GET and "status" in self.request.GET:
            types = self.request.GET.getlist("type")
            status = self.request.GET.getlist("status")
            for typ in types:
                for stat in status:
                    filters |= Q(type=typ, status=stat)

        elif "type" in self.request.GET:
            types = self.request.GET.getlist("type")
            for i in types:
                filters |= Q(type=i)

        elif "status" in self.request.GET:
            status = self.request.GET.getlist("status")
            for i in status:
                filters |= Q(status=i)

        queryset = queryset.filter(filters)

        return queryset