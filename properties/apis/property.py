from rest_framework import viewsets
from accounts.permissions import IsAdmin, IsAdminOrBuilder
from properties.services.property import PropertyService

class PropertyViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAdminOrBuilder()]

    def list(self, request):
        return PropertyService(request).get_all_properties()
    
    def retrieve(self, request, pk=None):
        return PropertyService(request).retrieve_property(pk)
    
    def create(self, request):
        return PropertyService(request).create_property()

    def update(self, request, pk=None):
        return PropertyService(request).update_property(pk)

    def partial_update(self, request, pk=None):
        return PropertyService(request).update_property(pk, partial=True)

    def destroy(self, request, pk=None):
        return PropertyService(request).delete_property(pk)
   