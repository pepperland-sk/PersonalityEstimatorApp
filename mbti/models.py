import uuid

from django.db import models
from django.utils import timezone

class Mbti(models.Model):
    class Meta:
        db_table = 'post'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'post'

    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False
        )
    content = models.TextField(
        verbose_name = 'post',
        max_length = 4000
    )
    type = models.TextField(
        verbose_name = 'type',
        blank = True,
        null = True
    )
    label = models.CharField(
        verbose_name = 'label',
        max_length = 4
    )
    score_ie = models.FloatField(
        verbose_name = 'score_ie',
        default=0.0
    )
    score_sn = models.FloatField(
        verbose_name = 'score_sn',
        default=0.0
    )
    score_tf = models.FloatField(
        verbose_name = 'score_tf',
        default=0.0
    )
    score_pj = models.FloatField(
        verbose_name = 'score_pj',
        default=0.0
    )
    created_at = models.DateTimeField(
        default = timezone.now
    )