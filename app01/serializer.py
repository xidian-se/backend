from rest_framework import serializers

class OwnerListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
