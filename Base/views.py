from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from .models import ListItem, List
from django.contrib.auth import authenticate, login
from .forms import ListForm,UserListForm,RegistrationForm
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'loginregi.html', {})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_name'] = username  # Store username in session
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'loginregi.html', {})

    context = {}
    return render(request, 'loginregi.html', context)

def home(request):
    user_name = request.session.get('user_name', '')  # Retrieve username from session
    list_items = List.objects.all()
    return render(request, 'home.html', {'user_name': user_name, 'List': list_items})

def createtask(request):
    user_name = request.session.get('user_name', '')  # Retrieve username from session
    form = ListForm()
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'TaskForm.html', {'form': form, 'user_name': user_name.upper()})


def listRoom(request, pk):
    global id
    id = pk
    data =list(ListItem.objects.all().values())
    user_name = request.session.get('user_name', '')  # Retrieve username from session
    room = List.objects.get(id=pk)
    context = {'data':data,'user_name': user_name.upper(),"user_id" : request.user.id, 'List': List.objects.all(), 'room': room, 'pk':pk}
    return render(request, 'list.html', context)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        # Check if the request has a valid CSRF token
        if not request.META.get('HTTP_X_CSRFTOKEN'):
            return JsonResponse({'error': 'CSRF token missing or incorrect'}, status=403)

        # Check if the request has a JSON content type
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Invalid content type. Expected application/json'}, status=400)

        try:
            # Parse JSON data sent from frontend
            data = json.loads(request.body)
            obj = ListItem.objects.filter(list_id=id)
            obj.delete()
            print(data)
            for item_data in data:
                item = ListItem(**item_data)
                item.save()   
            return JsonResponse({'message': 'Data saved successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'GET':
        # Handle GET requests if needed
        return JsonResponse({'message': 'This endpoint accepts only POST requests'}, status=405)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def delete_item(request, item_id):
    print(request)
    # Retrieve the item from the database
    item = get_object_or_404(List, id=item_id)
    # Delete the item
    item.delete()
    # Redirect to the parent page URL
    return redirect(reverse('home'))

def dele(request,item_id):
    user_name = request.session.get('user_name', '')
    return render(request, 'ConfirmDelete.html', {'item_id': item_id,'user_name': user_name.upper()})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})
