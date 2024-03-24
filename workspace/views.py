from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.utils import timezone
from datetime import date, time, datetime, timedelta
from users.models import CustomUser
from .models import Dashboard, Notes, Calendar, Todo, RecentWorks, Deadlines, Storage
from django.views.generic import CreateView,DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import NotesForm, StorageFileForm, StorageFolderForm, CalendarForm, TodoForm, DeadlinesForm
from eduweb.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
import os, pytz
from users.views import login_required
from django.http import JsonResponse, HttpResponse


def logout_view(request):
    if request.user.is_authenticated:
        request.user.last_logout = timezone.now()
        request.user.save()
        time_for_single_session(request)
    logout(request)
    return redirect('home')


def workspace_view(request):
    size = RecentWorks.objects.filter(author=request.user).count()
    for i in range(size):
        if i>4:
            a = RecentWorks.objects.filter(author=request.user).first().delete()
        else:
            continue

    form1 = TodoForm()
    form2 = DeadlinesForm()
    recent_works = RecentWorks.objects.filter(author=request.user)
    DeadlinesList = Deadlines.objects.filter(author=request.user).order_by('ended_on')
    print(DeadlinesList)
    todolist = Todo.objects.filter(author=request.user).exclude(task__icontains='_completed')
    if request.method == 'POST':
        print('yo1')
        if 'form1_submit' in request.POST:
            print('yo2')
            form1 = TodoForm(request.POST)
            print(request.POST)
            print('yo3')
            if form1.is_valid():
                print('yo4')
                todo = Todo(
                    task=form1.cleaned_data['task'],
                    author=request.user
                )
                print('yo4')
                todo.save()

                recentworks = RecentWorks(
                    item='Task Created - '+form1.cleaned_data['task'],
                    author=request.user
                )
                print('yo5')
                recentworks.save()

                return redirect('workspace')
            else:
                print(form1.errors)
        elif 'form2_submit' in request.POST:
            form2 = DeadlinesForm(request.POST)
            if form2.is_valid():
                deadlines = Deadlines(
                    task=form2.cleaned_data['task'],
                    ended_on=form2.cleaned_data['ended_on'],
                    author=request.user
                )
                deadlines.save()

                recentworks = RecentWorks(
                    item='Deadline Created - ' + form2.cleaned_data['task'],
                    author=request.user
                )
                recentworks.save()

                return redirect('workspace')
            else:
                print(form2.errors)
    else:
        form1 = TodoForm()
        form2 = DeadlinesForm()

    context = {
        'todolist': todolist,
        'deadlinesList': DeadlinesList,
        'form1': form1,
        'form2': form2,
        'recent_works': recent_works
    }
    return render(request, 'workspace.html', context)


class EditTodo(LoginRequiredMixin,UpdateView):
    model = Todo
    fields = ['task']
    success_url = reverse_lazy('workspace')
    template_name = 'workspace.html'

    def form_valid(self, form):
        print('yo')
        self.object = form.save()
        recentworks = RecentWorks(
            item='Task Edited - ' + form.cleaned_data['task'],
            author=self.request.user
        )
        recentworks.save()
        return super().form_valid(form)


def move_to_trash(request):
    if request.method == 'POST':
        check = request.POST.getlist('checkbox')
        print(check)
        if check:
            results = Todo.objects.get(id__in=check)
            task = Todo.objects.filter(id__in=check).values_list('task')
            print(results)
            results.task = task[0][0]+'_completed'
            results.save()
            #completed = results[0][0]+'_complete'
    return redirect(reverse_lazy('workspace'))


def time_for_single_session(request):
    login_time = CustomUser.objects.filter(username=request.user).values_list('last_login')
    logout_time = CustomUser.objects.filter(username=request.user).values_list('last_logout')
    for i in login_time:
        for j in i:
            t1 = j

    for i in logout_time:
        for j in i:
            t2 = j

    logged_in_time = t2 - t1

    if t1.date() == t2.date():
        day = t1.strftime('%A')
        save_to_day, created = Dashboard.objects.get_or_create(user=request.user)
        print(save_to_day)
        total_time = getattr(save_to_day, day, timedelta())
        total_time += logged_in_time
        setattr(save_to_day, day, total_time)
        save_to_day.save()
        print(total_time)

    else:
        prev_day = t1.strftime('%A')
        next_day = t2.strftime('%A')
        midnight = datetime.combine(t2.date(), time(0, 0, 0), pytz.timezone('utc'))
        save_to_day, created = Dashboard.objects.get_or_create(user=request.user)
        get_prev_time = getattr(save_to_day, prev_day, timedelta())
        get_next_time = getattr(save_to_day, next_day, timedelta())
        prev_time = abs(midnight - t1)
        next_time = t2 - midnight
        get_prev_time = get_prev_time + prev_time
        get_next_time = get_next_time + next_time
        setattr(save_to_day, prev_day, get_prev_time)
        setattr(save_to_day, next_day, get_next_time)
        save_to_day.save()


@login_required
def ListNotes(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        print(request.GET)
        results = []
        if query:
            results = Notes.objects.filter(title__icontains=query, author=request.user)
        print(request.user)

        try:
            note = Notes.objects.get(pk=Notes.objects.filter(author=request.user).last().pk)
            notes = Notes.objects.filter(author=request.user).order_by('-pk')
            print('yo1')

        except:
            note = Notes.objects.get(pk=Notes.objects.first().pk)
            notes = Notes.objects.filter(author='jadepy').order_by('-pk')
            print('yo2')

        context = {'notes': notes,
                   'note': note,
                   'results': results
                   }
        return render(request, 'notes.html', context)


def notes(request, pk):
    note = Notes.objects.get(pk=pk)
    try:
        print('yo1')
        notes = Notes.objects.filter(author='jadepy').order_by('-pk')
    except:
        notes = Notes.objects.filter(author='jadepy').order_by('-pk')

    context = {'note': note,
               'notes': notes
               }
    return render(request, 'notes.html', context)


class EditNotes(LoginRequiredMixin,UpdateView):
    model = Notes
    success_url = reverse_lazy('notes')
    template_name = 'create_new.html'
    fields = ['content', 'title', 'explanation']

    def form_valid(self, form):
        self.object = form.save()
        recentworks = RecentWorks(
            item='Note Edited - ' + form.cleaned_data['title'],
            author=self.request.user
        )
        recentworks.save()
        return super().form_valid(form)


class DeleteNotes(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = reverse_lazy('notes')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        recentworks = RecentWorks(
            item='Note Deleted - ' + self.object.title,
            author=self.request.user
        )
        recentworks.save()
        self.object.delete()
        return redirect(self.get_success_url())


@login_required
def create_view(request):
    current_time = datetime.now()
    print(current_time)
    print('yo1')
    if request.method == 'POST':
        print('yo2')
        form = NotesForm(request.POST)
        print('yo3')
        if form.is_valid():
            print('yo4')
            note = Notes(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                explanation=form.cleaned_data['explanation'],
                saved=current_time,
                author=request.user
            )

            recentworks = RecentWorks(
                item='Note Created - ' + form.cleaned_data['title'],
                author=request.user
            )
            recentworks.save()
            print('yo5')
            note.save()
            print('yo6')
            return redirect('notes')
        else:
            print('yo7')
            print(form.errors)
    else:
        print('yo8')
        form = NotesForm
        print('yo9')
    return render(request, 'create_new.html', {'form': form})


@login_required
@csrf_exempt
def upload_image(request):
    print('yo1')
    if request.method == 'POST':
        print('yo2')
        file_obj = request.FILES['file']
        print('yo3')
        file_path = os.path.join(MEDIA_ROOT, file_obj.name)
        print('yo4')
        with open(file_path, 'wb+')as f:
            print('yo5')
            for chunk in file_obj.chunks():
                print('yo6')
                f.write(chunk)
        print(file_path)
    return JsonResponse({'location': file_path})


@login_required
def dashboard_view(request):
    DeadlinesList = Deadlines.objects.filter(author=request.user).order_by('ended_on')
    complete = Todo.objects.filter(task__icontains='_complete', author=request.user)
    not_complete = Todo.objects.filter(author=request.user).exclude(task__icontains='_complete')
    print(not_complete)
    print(complete)
    data = Dashboard.objects.filter(user=request.user).values_list()
    mon = data[0][2].hour*60+data[0][2].minute
    tue = data[0][3].hour*60+data[0][3].minute
    wed = data[0][4].hour*60+data[0][4].minute
    thu = data[0][5].hour*60+data[0][5].minute
    fri = data[0][6].hour*60+data[0][6].minute
    sat = data[0][7].hour*60+data[0][7].minute
    sun = data[0][8].hour*60+data[0][8].minute

    dat = [mon, tue, wed, thu, fri, sat, sun]

    context = {
        'data': dat,
        'complete': complete,
        'not_complete': not_complete,
        'deadlinesList': DeadlinesList,
    }

    return render(request, 'dashboard.html', context)


@login_required
def storage_view(request):
    folder = Storage.objects.filter(author=request.user, file='').values_list('folder')
    listfolder = []
    for item in folder:
        listfolder.append(item[0])
    print(folder)
    query = Q()
    for item in listfolder:
        query |= Q(file__icontains = item)
    query&=Q(author=request.user)

    print(query)
    file = Storage.objects.filter(query).values_list('file')
    print(file)
    listfile = []
    for item in file:
        listfile.append(item[0])
    print('yo1')
    if request.method == 'POST':
        print('1')
        form1 = StorageFolderForm(request.POST)
        form2 = StorageFileForm(request.POST)
        print(request.POST)
        if 'foldername' in request.POST:
            print('2')
            if form1.is_valid():
                print('3')
                storage = Storage(
                    folder=form1.cleaned_data['folder'],
                    author=request.user,
                    upload_time=timezone.now()
                )
                storage.save()
                print('4')
                return redirect('storage')
            else:
                print('5')
                print(form1.errors)
        else:
            print('yo2')
            form = StorageFileForm(request.POST, request.FILES)

            print('yo3')
            if form.is_valid():
                print('yo4')
                form.instance.folder = form.cleaned_data['folder']
                a = str(form.cleaned_data['folder'])
                form.instance.file = request.FILES['file']
                form.instance.file.name = form.instance.folder + '_' + request.FILES['file'].name
                form.instance.upload_time = timezone.now()
                form.instance.author = request.user
                form.save()

                return redirect('storage')
            else:
                print('yo5')
                print(form.errors)
    else:
        print('yo6')
        form = StorageFileForm()
        form1 = StorageFolderForm()

    context = {
        'form': form,
        'form1': form1,
        'folder': listfolder,
        'file': listfile
    }
    return render(request, 'storage.html', context)


@login_required
def calendar_view(request):
    print('yo1')
    if request.method == 'POST':
        print('yo2')
        form = CalendarForm(request.POST)
        print('yo3')
        if form.is_valid():
            print('yo4')
            calendar = Calendar(
                event=form.cleaned_data['event'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                author=request.user
            )
            print('yo5')
            calendar.save()
            print('yo6')
            return render(request, 'calendar.html', {'form': form})
        else:
            print('yo7')
            print(form.errors)
    else:
        print('yo8')
        form = CalendarForm
        print('yo9')
    return render(request, 'calendar.html')


def get_events(request):
    date = request.GET.get('date')
    events = Calendar.objects.filter(start_date=date)
    event_data = [{'title': event.event, 'start_date': event.start_date, 'end_date': event.end_date} for event in events]
    return JsonResponse(event_data, safe=False)


@login_required
def deadlines_view(request):
    return render(request, 'deadlines.html')


@login_required
def music_view(request):
    return render(request, 'music.html')


@login_required
def summarization_view(request):
    return render(request, 'summarization.html')


@login_required
def trash_view(request):
    return render(request, 'trash.html')