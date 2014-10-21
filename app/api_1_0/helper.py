# -*- coding: utf-8 -*-


def paginate(query, page, per_page=10):
    pages = int((len(query) + per_page - 1) / per_page)
    if page > pages or page < 1:
        return []
    else:
        return query[(page - 1) * per_page: page * per_page]