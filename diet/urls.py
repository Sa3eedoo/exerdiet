from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('foods', views.FoodViewSet)
router.register('custom_foods',
                views.CustomFoodViewSet,
                basename='custom_foods')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('meals',
                views.MealViewSet,
                basename='meals')

recipes_router = routers.NestedDefaultRouter(router,
                                             'recipes',
                                             lookup='recipe')
recipes_router.register('food_instances',
                        views.RecipeFoodInstanceViewSet,
                        basename='recipes-food_instances')

meals_router = routers.NestedDefaultRouter(router,
                                           'meals',
                                           lookup='meal')
meals_router.register('recipes',
                      views.MealRecipeViewSet,
                      basename='meals-recipes')
meals_router.register('food_instances',
                      views.MealFoodInstanceViewSet,
                      basename='meals-food_instances')

# URLConf
urlpatterns = router.urls + recipes_router.urls + meals_router.urls
