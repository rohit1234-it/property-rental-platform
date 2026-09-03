from rentals.apis.rentals import RentalViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("rentals",RentalViewSet,basename='rentals')

urlpatterns = router.urls
