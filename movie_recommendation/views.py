from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, logout, authenticate, get_user_model as usermd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas, joblib

mymodel = joblib.load("./model")
md = pandas.read_feather("./movies_final.feather")

model_large, genre_counts = mymodel["model"], mymodel["genre_counts"]
get_genre_movies = mymodel["get_genre_movies"]


def get_search_result(x):
    if len(x) > 2:
        return {
            title: idx
            for title, [idx, poster] in model_large.indices.items()
            if x.lower() in title.lower()
        }


def home(request, val={}):
    return render(request, "home.html", val)


def recommend(request, slug=None, val=dict()):
    if request.htmx:
        title = request.GET["title"]
        val["title"] = title
        val["recommendations"] = model_large.get_recommendations(title)
        return render(request, "htmx/recommend_results.html", val)
    return render(request, "recommend.html", val)


def ranking(request, val={}, *arg, **kwa):
    genre_select = request.GET.get("genre_select_option", None)
    page = request.GET.get("page", None)
    if not genre_select or not request.htmx:
        val["genres"] = genre_counts.keys()
        return render(request, "ranking.html", val)
    val["genre_select"] = genre_select
    genredf = get_genre_movies(genre_select)
    # print(genredf, type(genredf))
    # print(genre_select,page)
    paginator = Paginator(genredf, 30)
    try:
        page_obj = paginator.get_page(page)  # returns the desired page object
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    val["page_obj"] = page_obj
    # return render(request, "recommend.html", val)
    return render(request, "htmx/ranking_results.html", val)


# ---------------------------------------------------------------------- H T M X ------------------------------------------------------------------


def htmx_search_results(request, val={}):
    val["search_results"] = get_search_result(request.GET["search"])
    return render(request, "htmx/search_results.html", val)


def htmx_desc(request, val={}, *arg, **kwa):
    # print(arg, kwa)
    idx = model_large.indices[kwa["title"]][0]
    val["md"] = md.loc[idx]
    return render(request, "htmx/ranking_desc.html", val)
