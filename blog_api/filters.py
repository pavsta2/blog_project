def filter_by_author_id(queryset, author_id):
    return queryset.filter(author_id=author_id)