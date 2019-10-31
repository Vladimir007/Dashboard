from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Action(MPTTModel):
    parent = TreeForeignKey('self', models.CASCADE, null=True, blank=True, related_name='children')
    phrases = ArrayField(models.CharField(max_length=128))

    @property
    def detail_url(self):
        return reverse('core:api-action-detail', args=[self.id])

    @property
    def children_url(self):
        return reverse('core:api-action-children', args=[self.id])

    @property
    def description_html(self):
        return '<br>'.join(self.phrases)

    class Meta:
        db_table = 'action'


class Unit(MPTTModel):
    parent = TreeForeignKey('self', models.CASCADE, null=True, blank=True, related_name='children')
    names = ArrayField(models.CharField(max_length=64))

    @property
    def detail_url(self):
        return reverse('core:api-unit-detail', args=[self.id])

    @property
    def children_url(self):
        return reverse('core:api-unit-children', args=[self.id])

    @property
    def description_html(self):
        return '<br>'.join(self.names)

    class Meta:
        db_table = 'unit'


class Category(MPTTModel):
    parent = TreeForeignKey('self', models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=64)

    @property
    def detail_url(self):
        return reverse('core:api-category-detail', args=[self.id])

    @property
    def children_url(self):
        return reverse('core:api-category-children', args=[self.id])

    @property
    def description_html(self):
        return self.name

    class Meta:
        db_table = 'category'


class TripleLink(models.Model):
    action = models.ForeignKey(Action, models.CASCADE)
    unit = models.ForeignKey(Unit, models.CASCADE)
    category = models.ForeignKey(Category, models.CASCADE)

    class Meta:
        db_table = 'triple_link'


class ActionAnomaly(models.Model):
    action1 = models.ForeignKey(Action, models.CASCADE, related_name='+')
    action2 = models.ForeignKey(Action, models.CASCADE, related_name='+')
    phrase1 = models.PositiveIntegerField()
    phrase2 = models.PositiveIntegerField()

    class Meta:
        db_table = 'action_anomaly'
