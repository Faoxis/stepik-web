import logging
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404


def paginate(request, query_set):

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit %= 100

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(query_set, limit)
    logging.info(type(page))
    logging.info(type(paginator.num_pages))
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page, paginator
