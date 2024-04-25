import django_filters


class PeopleFilter(django_filters.FilterSet):
  calories = django_filters.AllValuesFilter()