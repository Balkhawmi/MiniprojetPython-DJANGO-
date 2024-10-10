from rest_framework.routers import DefaultRouter
from .views import EmployeViewSet, DirigeantViewSet, CongeViewSet

router = DefaultRouter()
router.register('employes', EmployeViewSet)
router.register('dirigeants', DirigeantViewSet)
router.register('conges', CongeViewSet)

urlpatterns = router.urls
