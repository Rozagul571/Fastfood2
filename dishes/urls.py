from rest_framework.routers import DefaultRouter
from dishes.views import DishViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls