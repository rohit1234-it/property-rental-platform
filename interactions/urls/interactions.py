from rest_framework.routers import DefaultRouter
from interactions.apis.interactions import InteractionViewSet

router=DefaultRouter()
router.register('interactions',InteractionViewSet,basename='interaction')

urlpatterns = router.urls
