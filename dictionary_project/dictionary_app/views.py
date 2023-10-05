from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from .forms import AddWordForm
from .models import Dict

@csrf_exempt

def home(request):
    return render(request, 'dictionary_app/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'dictionary_app/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('home')

def loginuser(request):
    if request.method == 'GET':
            return render(request, 'dictionary_app/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
             return render(request, 'dictionary_app/loginuser.html', {'form':AuthenticationForm(), 'error':'Wrong login or password.'})
        else:
             login(request, user)
             return redirect('home')
        
def logoutuser(request):
     if request.method == 'POST':
          logout(request)
          return redirect('home')
     
def dict(request):
    words = Dict.objects.filter(user=request.user)
    return render(request, 'dictionary_app/dict.html', {'words':words})
     
def addword(request):
    if request.method == 'GET':
        return render(request, 'dictionary_app/addword.html', {'form':AddWordForm()})
    else:
        try:
            form = AddWordForm(request.POST)
            newword = form.save(commit=False)
            newword.user = request.user
            newword.save()
            return redirect('home')
        except ValueError:
            return render(request, 'todo/addword.html', {'form':AddWordForm(), 'error':'Bad data passed in. Try again.'})
        
def viewword(request, word_pk):
    word = get_object_or_404(Dict, pk=word_pk, user=request.user)
    if request.method == 'GET':
        form = AddWordForm(instance=word)
        return render(request, 'dictionary_app/viewword.html', {'word':word, 'form':form})
    else:
        try:
            form = AddWordForm(request.POST, instance=word)
            form.save()
            return redirect('dict')
        except ValueError:
            return render(request, 'dictionary_app/viewword.html', {'word':word, 'form':form, 'error':'Bad data passed in. Try again.'})
        
def deleteword(request, word_pk):
    word = get_object_or_404(Dict, pk=word_pk, user=request.user)
    if request.method == 'POST':
        word.delete()
        return redirect('dict')
