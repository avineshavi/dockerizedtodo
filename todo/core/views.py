from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from core.models import Todo
from core.forms import CreateForm, EmailForm
from django.core.mail import send_mail
from django.template import Template, Context
from datetime import date

# Create your views here.
# def root(request):
#     return HttpResponse("<h1>WELCOME</h1>")


def index(request):
    task = Todo.objects.all()
    return render(request, 'dashboard.html', context={'tasks': task})


def todo_create_view(request):

    if request.method == "POST":  
        form = CreateForm(request.POST)  
        if form.is_valid():  
            Todo.objects.create(
                    name= form.cleaned_data.get('name'),
                    description = form.cleaned_data.get('description'),
                    due_date = form.cleaned_data.get('due_date'),
                    repeat = form.cleaned_data.get('repeat'),
            )
        return redirect('/')
    else:  
        form = CreateForm()
        return render(request,'create.html',{'form':form})
    


def todo_update_view(request, id):
    task = Todo.objects.filter(id=id).first()
    if request.method == "POST":  
        form = CreateForm(request.POST)  
        if form.is_valid():
            task.name=form.cleaned_data.get('name')
            task.description=form.cleaned_data.get('description')
            task.due_date=form.cleaned_data.get('due_date')
            task.repeat=form.cleaned_data.get('repeat')
            task.save()
        return redirect('/index')
    else:
        if task:
            data = {
                "name": task.name,
                "description": task.description,
                "due_date": task.due_date,
                "repeat": task.repeat,
            }

        form = CreateForm(initial=data)
        return render(request,'create.html',{'form':form})
    

def delete_view(request, id):

    if request.method =="DELETE":
        try:
            obj = Todo.objects.get(id=id)
            obj.delete()
            return JsonResponse({"success": True})
        except ObjectDoesNotExist:
            return JsonResponse({"success": False})
        

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            curr_date = date.today()
            tasks = Todo.objects.filter(due_date=curr_date)
            if not tasks.exists():
                return
            template = '''<table class="table">
    <thead>
      <tr>
        <th scope="col"><i class="fa-solid fa-circle-up"></i>TASK NAME</th>
        <th scope="col"><i class="fa-solid fa-circle-up"></i>DATE</th>
        <th scope="col"><i class="fa-solid fa-circle-up"></i>REPEAT</th>
        <th scope="col"><i class="fa-solid fa-circle-up"></i>DESCRIPTION</th>
        <th scope="col"><i class="fa-solid fa-circle-up"></i>ACTION</th>
      </tr>
    </thead>
    <tbody>
    {% for task in tasks %}
      <tr>
        <th scope="row">{{task.name}}</th>
        <td>{{task.due_date}}</td>
        <td>{{task.repeat}}</td>
        <td>{{task.description}}</td>

        </td>

      </tr>
      {% endfor %}
    </tbody>
  </table>'''
            msg = template.render(Context(tasks))
            # Send the email
            send_mail(
                "Todays Task",
                msg,
                email,
            )

            # Optionally, you can show a success message or redirect the user to a thank you page
            return render(request, 'contact/success.html')

    else:
        form = EmailForm()

    return render(request, 'email.html', {'form': form})


from django.http import JsonResponse
from django.db.models import Q
from datetime import date, timedelta

def filter_records(request):
    filter_option = request.GET.get('filter_option')

    current_date = date.today()

    if filter_option == 'this_week':
        start_date = current_date - timedelta(days=current_date.weekday())
        end_date = start_date + timedelta(days=6)
        filtered_records = Todo.objects.filter(due_date__range=[start_date, end_date])

    elif filter_option == 'this_month':
        start_date = current_date.replace(day=1)
        end_date = current_date.replace(day=1, month=current_date.month+1) - timedelta(days=1)
        filtered_records = Todo.objects.filter(due_date__range=[start_date, end_date])

    elif filter_option == 'current_date':
        filtered_records = Todo.objects.filter(due_date=current_date)

    else:
        # Handle the case for no filter option selected
        filtered_records = Todo.objects.all()

    data = {'filtered_records': list(filtered_records.values())}
    return JsonResponse(data)


