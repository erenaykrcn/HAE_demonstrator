from django.shortcuts import render
from .constants import MW_measure, SIM_expr, N_PARAMS
import json


def home_page(request):
    print(request.user)
    return render(request, "homepage.html", context={
    		"current_page": "home"
    	})


def train_page(request):
    dic = {
    		"current_page": "train",
    }
    dic = dic | MW_measure
    dic = dic | SIM_expr


    return render(request, "train_hae.html", dic)


def train_page_qvc(request):
    dic = {
            "current_page": "train",
    }
    dic = dic | MW_measure
    dic = dic | SIM_expr
    dic = dic | N_PARAMS


    return render(request, "train_qvc.html", dic)
