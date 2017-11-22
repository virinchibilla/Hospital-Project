from rest_framework import serializers
from .models import *

import logging

class HospuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospuser
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def update(self, instance, validated_data):
        instance.role = validated_data.pop('role')

        instance.save()
        return instance

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ( 'id', 'subject_code', 'created_id', 'blood_type', 'create_date')

class SubjectIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ( 'id', 'created_id')

class CancertypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancertype
        fields = ( 'name', )

class SampleSerializer(serializers.ModelSerializer):
    cancer = CancertypeSerializer(many=True)
    created_id = serializers.SerializerMethodField('get_the_create_id')
    class Meta:
        model = Sample
        fields = ( 'id', 'subject', 'cancer', 'created_id')

    def get_the_create_id(self, model):
        return Subject.objects.get(id=model.subject_id).created_id

    def create(self, validated_data):
        cancer = validated_data.pop('cancer')
        sample = Sample(subject=validated_data.pop('subject'), **validated_data)
        sample.save()
        for c in cancer:
            c = Cancertype.objects.get(name=c['name'])
            sample.cancer.add(c)

        return sample


 