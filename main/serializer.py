from rest_framework import serializers
from .models import Category, State, Region, Type, Tag, Company, Contact


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class MiniStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'title')


class MiniRegionSerializer(serializers.ModelSerializer):
    state = MiniStateSerializer(read_only=True)

    class Meta:
        model = Region
        fields = ('id', 'title', 'state')
        

class StateSerializer(serializers.ModelSerializer):
    region = MiniRegionSerializer(read_only=True, many=True)

    class Meta:
        model = State
        fields = ('id', 'title', 'region')
        

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('id', 'state', 'title')
        extra_kwargs = {
            'state': {'read_only': True}
        }
        
    def create(self, validated_data):
        state_id = self.context['state_id']
        instance = Region.objects.create(state_id=state_id, **validated_data)
        instance.save()
        return instance


class CompanyGETSerializer(serializers.ModelSerializer):
    region = MiniRegionSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'region', 'title')


class CompanyPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'region', 'title')

    # def create(self, validated_data):
    #     region_id = self.context['region_id']
    #     instance = Company.objects.create(region_id=region_id, **validated_data)
    #     return instance


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'title')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')

