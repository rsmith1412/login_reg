from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# MESSAGE_TAGS = {
#     messages.LOGIN: ''
# }
# Create your views here.
def index(request):
    return render(request, "log_reg/index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect("/")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        pw = request.POST["password"]
        pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        request.session["user_id"] = new_user.id
        return redirect("/success")

def login(request):
    email = request.POST["email"]
    pw = request.POST["password_login"]
    users = User.objects.filter(email = email)
    if len(users) == 0:
        messages.error(request, "Invalid login.", extra_tags='login')
        return redirect("/")

    user = users[0]
    if bcrypt.checkpw(pw.encode(), user.password.encode()):
        request.session["user_id"] = user.id
        return redirect("/success")
    messages.error(request, "Invalid login.", extra_tags='login')
    return redirect("/")

def success(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session["user_id"])
        context = {"user" : user}
        return render(request, "log_reg/success.html", context)
    return redirect("/")
    # user = User.objects.get(id=id)
    # context = {"user" : user}
    # return render(request, "log_reg/success.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")
