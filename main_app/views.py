from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Seed
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def finch_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', { 'finches': finches })

@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    seeds_finch_doesnt_have = Seed.objects.exclude(id__in = finch.seeds.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {'finch' : finch, 'feeding_form': feeding_form, 'seeds': seeds_finch_doesnt_have
    })

@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)
@login_required
def assoc_seed(request, finch_id, seed_id):
    Finch.objects.get(id=finch_id).seeds.add(seed_id)
    return redirect ('detail', finch_id=finch_id)

def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else: 
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'size', 'color', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['size', 'color', 'age']

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'

class SeedList(LoginRequiredMixin, ListView):
  model = Seed

class SeedDetail(LoginRequiredMixin, DetailView):
  model = Seed

class SeedCreate(LoginRequiredMixin, CreateView):
  model = Seed
  fields = '__all__'

class SeedUpdate(LoginRequiredMixin, UpdateView):
  model = Seed
  fields = ['name', 'color']

class SeedDelete(LoginRequiredMixin, DeleteView):
  model = Seed
  success_url = '/seeds/'