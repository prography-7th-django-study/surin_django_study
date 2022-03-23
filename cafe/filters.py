from rest_framework.filters import BaseFilterBackend


class LimitedProductFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('limit'):
            return queryset.filter(is_limited=True)
        return queryset
