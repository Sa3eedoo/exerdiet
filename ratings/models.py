from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import Trainee, User
from django.utils import timezone


class RatingChoice(models.IntegerChoices):
    ONE = 1 
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = 'Rate this'
    
class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=Avg('value'))['average']

class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db)
    
    def avg(self):
        return self.get_queryset().avg()

class Rating(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    value = models.IntegerField(null=True, blank=True, choices=RatingChoice.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    active = models.BooleanField(default=True)
    active_update_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = RatingManager()
    
    class Meta:
        ordering = ['-timestamp']
        
def rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        _id = instance.id
        if instance.active:
            qs = Rating.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
                trainee=instance.trainee
            ).exclude(id=_id, active=True)
            if qs.exists():
                qs = qs.exclude(active_update_timestamp__isnull=False)
                # qs.update(active=False, active_update_timestamp=timezone.now())
            qs.delete()


post_save.connect(rating_post_save, sender=Rating)