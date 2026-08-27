from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm, CutoffSearchForm
from .models import College, Cutoff, StudentProfile, Application


def home(request):
    stats = {
        'college_count': College.objects.count(),
        'branch_count': Cutoff.objects.values('branch').distinct().count(),
        'cutoff_count': Cutoff.objects.count(),
    }
    return render(request, 'counseling/home.html', {'stats': stats})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
            StudentProfile.objects.create(
                user=user,
                community=data['community'],
                phone=data['phone'],
            )
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    applications = profile.applications.select_related('cutoff__college', 'cutoff__branch')
    return render(request, 'counseling/dashboard.html', {
        'profile': profile,
        'applications': applications,
    })


def college_list(request):
    colleges = College.objects.all()
    q = request.GET.get('q', '')
    if q:
        colleges = colleges.filter(name__icontains=q)
    return render(request, 'counseling/college_list.html', {'colleges': colleges, 'q': q})


def college_detail(request, pk):
    college = get_object_or_404(College, pk=pk)
    cutoffs = college.cutoffs.select_related('branch').order_by('branch__name', 'community')
    return render(request, 'counseling/college_detail.html', {'college': college, 'cutoffs': cutoffs})


def cutoff_search(request):
    results = None
    form = CutoffSearchForm(request.GET or None)
    if request.GET and form.is_valid():
        mark = form.cleaned_data['cutoff_mark']
        community = form.cleaned_data['community']
        branch = form.cleaned_data.get('branch')

        results = Cutoff.objects.select_related('college', 'branch').filter(
            community=community,
            cutoff_mark__lte=mark,
        )
        if branch:
            results = results.filter(branch=branch)
        results = results.order_by('-cutoff_mark')

    return render(request, 'counseling/cutoff_search.html', {'form': form, 'results': results})


@login_required
def apply_to_college(request, cutoff_id):
    cutoff = get_object_or_404(Cutoff, pk=cutoff_id)
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    application, created = Application.objects.get_or_create(student=profile, cutoff=cutoff)
    if created:
        messages.success(request, f"Saved {cutoff.college.name} ({cutoff.branch.name}) to your dashboard.")
    else:
        messages.info(request, "You've already saved this option.")
    return redirect('dashboard')