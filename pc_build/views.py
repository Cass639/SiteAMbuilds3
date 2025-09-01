from django.shortcuts import render

# Create your views here.
def pc_build(request):
    return render(request, "pc_build/index.html")