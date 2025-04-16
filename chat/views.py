from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def chat_view(request, username):
    return render(request, "chat/index.html", {
        "other_username": username
    })
