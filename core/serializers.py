from django.db.models import Q
from rest_framework import serializers, exceptions

from Dashboard.api import DynamicFieldsModelSerializer
from core.models import Action, Unit, Category, TripleLink, ActionAnomaly


class ActionSerializer(DynamicFieldsModelSerializer):
    def update(self, instance, validated_data):
        ActionAnomaly.objects.filter(Q(action1=instance) | Q(action2=instance)).delete()
        return super(ActionSerializer, self).update(instance, validated_data)

    class Meta:
        model = Action
        fields = ('id', 'parent', 'phrases')


class UnitSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'parent', 'names')


class CategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'parent', 'name')


class TripleLinkSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        try:
            return TripleLink.objects.get(**validated_data)
        except TripleLink.DoesNotExist:
            return super(TripleLinkSerializer, self).create(validated_data)

    class Meta:
        model = TripleLink
        fields = '__all__'


class ActionAnomalySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        value = super(ActionAnomalySerializer, self).validate(attrs)
        if len(attrs['action1'].phrases) <= attrs['phrase1']:
            raise exceptions.ValidationError({'phrase1': 'Index is too big!'})
        if len(attrs['action2'].phrases) <= attrs['phrase2']:
            raise exceptions.ValidationError({'phrase2': 'Index is too big!'})
        return value

    def create(self, validated_data):
        try:
            return ActionAnomaly.objects.get(**validated_data)
        except ActionAnomaly.DoesNotExist:
            return super(ActionAnomalySerializer, self).create(validated_data)

    class Meta:
        model = ActionAnomaly
        fields = ('id', 'action1', 'action2', 'phrase1', 'phrase2')
