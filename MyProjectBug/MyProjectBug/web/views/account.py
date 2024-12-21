from django.shortcuts import render
from web.froms.account import RgeisterModelForm


def register(request):
    form = RgeisterModelForm()
    return render(request, 'web/register.html', {'form': form})
