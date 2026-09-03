from rest_framework import viewsets
from rest_framework.decorators import action
from accounts.permissions import IsAdmin, IsAdminOrBuilder
from rentals.services.rentals import RentalService

class RentalViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAdminOrBuilder()]

    def list(self, request):
        return RentalService(request).get_all_rents()
    
    def retrieve(self, request, pk=None):
        return RentalService(request).retrieve_rentals(pk)
    
    def create(self, request):
        return RentalService(request).create_rentals()

    def update(self, request, pk=None):
        return RentalService(request).update_rentals(pk)

    def partial_update(self, request, pk=None):
        return RentalService(request).update_rentals(pk, partial=True)

    def destroy(self, request, pk=None):
        return RentalService(request).delete_rental(pk)
   