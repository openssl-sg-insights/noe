from rest_framework import viewsets

from . import models as m
from . import serializers as s


class SampleViewSet(viewsets.ModelViewSet):
    queryset = m.Sample.objects.all()
    serializer_class = s.SampleSerializer
