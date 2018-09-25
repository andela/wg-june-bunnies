from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from wger.nutrition.models import NutritionPlan


@receiver(post_delete, sender=NutritionPlan)
def reset_cache_nutrition_plan_on_delete(sender, instance, **kwargs):
    '''
    Resets the nutrition plan cache on delete.
    '''
    cache.clear()

@receiver(post_save, sender=NutritionPlan)
def reset_cache_nutrition_plan_on_save(sender, instance, **kwargs):
    '''
    Resets the nutrition plan cache on save.
    '''
    cache.clear()
    