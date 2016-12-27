
from django.shortcuts import render
from .models import Summary, Tasks, TaskDetail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
        queryset_list = Summary.objects.all()
        summary_title = "Test Run List"
        home = "activate"

        queryset = get_pagination_by_no(request, queryset_list, 15)

        context = {
                "title_summary":summary_title,
                "objects": queryset,
                "home": home,
        }

        return render(request, 'summary.html', context)

def tasks(request, ssid=None):
        queryset_list = Tasks.objects.filter(sid = ssid)
        task_title = "Task List"

        queryset = get_pagination_by_no(request, queryset_list, 25)

        context = {
                "title_tasks": task_title,
                "objects": queryset,
                "ssid": ssid,
        }

        return render(request, "tasks.html", context)

def task_detail(request, ssid=None, sssid=None):
        queryset_list = TaskDetail.objects.filter(task_id=sssid)
        task_detail_title = "Task Details List"

        queryset = get_pagination_by_no(request, queryset_list, 25)

        context = {
                "title_detail": task_detail_title,
                "objects": queryset,
                "ssid": ssid,
                "sssid": sssid,
        }

        return render(request, "task_detail.html", context)

def get_pagination_by_no(request, objects, number):
        paginator = Paginator(objects, number) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
                queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                queryset = paginator.page(paginator.num_pages)

        return queryset