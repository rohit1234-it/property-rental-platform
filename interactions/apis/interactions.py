from rest_framework import viewsets
from rest_framework.decorators import action
from accounts.permissions import IsAdmin, IsAdminOrBuilder
from interactions.services.interactions import InteractionService

class InteractionViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAdminOrBuilder()]

    def list(self, request):
        return InteractionService(request).get_all_interactions()
    
    def retrieve(self, request, pk=None):
        return InteractionService(request).retrieve_interactions(pk)
    
    def create(self, request):
        return InteractionService(request).create_interactions()

    def update(self, request, pk=None):
        return InteractionService(request).update_interaction(pk)

    def partial_update(self, request, pk=None):
        return InteractionService(request).update_interaction(pk, partial=True)

    def destroy(self, request, pk=None):
        return InteractionService(request).delete_interactions(pk)
   