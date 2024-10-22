from rest_framework import viewsets
from .models import DataEntry
from .serializers import DataEntrySerializer

class DataEntryViewSet(viewsets.ModelViewSet):
    queryset = DataEntry.objects.all()
    serializer_class = DataEntrySerializer

