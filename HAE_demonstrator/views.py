from django.shortcuts import render


def home_page(request):
    print(request.user)
    return render(request, "homepage.html", context={
    		"current_page": "home"
    	})


def train_page(request):
    dic = {
    		"current_page": "train"
    }
    return render(request, "train_hae.html", dic)
