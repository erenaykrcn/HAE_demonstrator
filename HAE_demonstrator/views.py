import os
dirname = os.path.dirname(__file__)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .constants import MW_measure, SIM_expr, N_PARAMS
import json

import sys
sys.path.append(os.path.join(dirname, '../../HAE/modules/'))
from preprocessing.preprocessing import sample_test_data
from metrics import metrics, predict
from preprocessing.visualize import plot_PCA_2D


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


def evaluate_hae(request):
    dic = {
        "current_page": "evaluate",
    }
    dic = dic | MW_measure
    dic = dic | SIM_expr
    
    files = {}
    for i in range(len(N_PARAMS.keys())):
        try:
            files["FILES" + str(i+1)] = json.dumps(os.listdir(os.path.join(dirname, "../../HAE/data/training_results/pqc" + str(i+1))))
        except FileNotFoundError:
            files["FILES" + str(i+1)] = []
    dic = dic | files

    return render(request, "evaluate_hae.html", dic)


def evaluate_qvc(request):
    dic = {
        "current_page": "evaluate",
    }
    dic = dic | MW_measure
    dic = dic | SIM_expr
    
    binary_files = {}
    multi_files = {}
    for i in range(len(N_PARAMS.keys())):
        try:
            binary_files["BINARY_FILES" + str(i+1)] = json.dumps(os.listdir(os.path.join(dirname, "../../HAE/data/training_results_QVC/pqc" + str(i+1) + "/binary_cl/")))
        except FileNotFoundError:
            binary_files["BINARY_FILES" + str(i+1)] = []

        try:
            multi_files["MULTI_FILES" + str(i+1)] = json.dumps(os.listdir(os.path.join(dirname, "../../HAE/data/training_results_QVC/pqc" + str(i+1) + "/multi_cl/")))
        except FileNotFoundError:
            binary_files["MULTI_FILES" + str(i+1)] = []
    dic = dic | binary_files
    dic = dic | multi_files

    return render(request, "evaluate_qvc.html", dic)


def visualize(request):
    dic = {
        "current_page": "visualize",
    }
    return render(request, "visualize.html", dic)
