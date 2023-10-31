from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')
    #return HttpResponse("This is home page")

def about(request):
    return render(request, 'about.html')
   #return HttpResponse("This is about page")

def product(request):
    return HttpResponse("This is product page")

def resource(request):
    return HttpResponse("This is resource page")

def pricing(request):
    return HttpResponse("This is pricing page")