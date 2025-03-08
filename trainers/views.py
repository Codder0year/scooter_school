from django.shortcuts import render
from .models import Trainer


def trainers_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainers_list.html', {'trainers': trainers})


