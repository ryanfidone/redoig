from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, _ = Group.objects.get_or_create(name="LibraryMember")
            user.groups.add(group)
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})
