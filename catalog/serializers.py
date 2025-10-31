from rest_framework import serializers
from .models import Source, Organization, Theme, Dataset


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all())
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    themes = serializers.PrimaryKeyRelatedField(many=True, queryset=Theme.objects.all())

    class Meta:
        model = Dataset
        fields = '__all__'