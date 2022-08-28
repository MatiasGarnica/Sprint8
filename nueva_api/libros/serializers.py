from rest_framework import serializers

from .models import Libro

from django.contrib.auth.models import User

class LibroSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Libro
        fields = ['title','genre','year','author','created_at','updated_at','owner']

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    libros = serializers.HyperlinkedRelatedField(many=True, view_name='libro-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url','id','username','libros']
