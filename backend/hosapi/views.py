from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Hospuser
from .models import Subject
from .models import Cancertype
from .models import Sample
from rest_framework.renderers import JSONRenderer
from hosapi.serializers import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import json
from rest_framework import permissions

import logging

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def authenticate_user(request, format=None):
	username = request.data['username']
	password = request.data['password']
	user = authenticate(username=username, password=password)
	logging.warn(user)
	logging.warn(request)
	if not user:
		return HttpResponse(status=403)

	token = Token.objects.get(user=user)
	user = Hospuser.objects.get(username=user.username)
	if not user:
		return HttpResponse(status=404)

	return JSONResponse({ 'username': username, 'token': token.key, 'role': user.role })

@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def signup(request, format=None):
	firstname = request.data['firstname']
	lastname = request.data['lastname']
	email = request.data['email']
	password = request.data['password']
	confirmpassword = request.data['confirmpassword']
	username = request.data['username']

	logging.warn(request.data)

	if confirmpassword != password:
		return HttpResponse('the password should match', status=400)

	try:
		user = User.objects.get(username=username)
		return HttpResponse('username already exists', status=403) # user already exists
	except User.DoesNotExist: #To create both django user and hospuser
		user = User.objects.create_user(username=username, password=password, email=email)
		b = Hospuser.objects.create(first_name=firstname, last_name=lastname, email=email, username=username)	
        
	return HttpResponse(status=200)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def hospuser_data(request, username):
	# user = Hospuser.objects.get(username=request.user.username)
	# if username != request.user.username and user.role != 'admin':
	# 	return HttpResponse(status=403)

	user = Hospuser.objects.get(username=username) # name of the username thaht I want more information
	hospuserSerialize = HospuserSerializer(user).data

	return JSONResponse(hospuserSerialize)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def hospusers_data_all(request):
	user = Hospuser.objects.get(username=request.user.username)
	if not user:
		return HttpResponse(status=404)
	if user.role != 'Admin':
		return HttpResponse(status=403)

	users = Hospuser.objects.all()

	logging.warn(users)
	hospuserSerializer = HospuserSerializer(users, many=True)

	result = {
		'hospusers_data': hospuserSerializer.data,
		'roles': Hospuser._meta.get_field('role').choices
	}

	return JSONResponse(result)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_hospuser(request):
	logging.warn('update user')
	request_user = request.user
	request_hospusers_data_all = request.data

	user = Hospuser.objects.get(username=request.user.username)

	logging.warn(request_hospusers_data_all)
	for hospuser_data in request_hospusers_data_all:
		user = Hospuser.objects.get(username=hospuser_data['username'])
		hospuserSerializer = HospuserSerializer(user, hospuser_data)
		if not hospuserSerializer.is_valid():
			return Response(hospuserSerializer.errors)
		hospuserSerializer.save()

	return HttpResponse(status=200)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_profile(request):
	logging.warn('update user')

	request_user = request.user
	hospuser_data = request.data


	user = Hospuser.objects.get(username=hospuser_data['username'])
	hospuser_data['role'] = user.role
	hospuserSerializer = HospuserSerializer(user, hospuser_data)
	if not hospuserSerializer.is_valid():
		return Response(hospuserSerializer.errors)
	hospuserSerializer.save()
	logging.warn(hospuserSerializer.data)

	return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createsubject(request, format=None):
	subjectcode = request.data['subjectcode']
	bloodtype = request.data['bloodtype']

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Subject editor']:
		return HttpResponse(status=403)

	# from time import gmtime, strftime
	# request.data['date'] = strftime("%Y-%m-%d", gmtime())

	d = {'blood_type':bloodtype, 'created_id': 'hqee', 'subject_code': subjectcode, 'create_date': request.data['date'] }

	logging.warn(request.user)

	# a = Address.objects.create(country=country, city=city, street=street, postalcode=postalcode)
	subjectSerializer = SubjectSerializer(data=d)
	if not subjectSerializer.is_valid():
		return Response(subjectSerializer.errors, status=404)

	a = subjectSerializer.save()
	created_id = subjectcode + '-' + request.data['date'][0:4] + '-' + str(a.id)
	logging.warn(created_id)
	a.created_id = created_id
	a.save()

	user.save()
     
	return HttpResponse(status=200)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_subjects(request, format=None):

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Subject editor']:
		return HttpResponse(status=403)

	subjects = Subject.objects.all()
	subjectSerializer = SubjectSerializer(subjects, many=True)

	result = {
		'subjects_data': subjectSerializer.data,
	}

	return JSONResponse(result)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_subjects(request):

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Subject editor']:
		return HttpResponse(status=403)

	logging.warn('update user')
	request_user = request.user
	subject_data = request.data
	id_ob = subject_data['id']
	subject_data['created_id'] = subject_data['subject_code'] + '-' + subject_data['create_date'][0:4] + '-' + str(id_ob)
	subject = Subject.objects.get(id=int(id_ob))
	subjectSerializer = SubjectSerializer(subject, subject_data)
	if not subjectSerializer.is_valid():
		return Response(subjectSerializer.errors)
	subjectSerializer.save()
	logging.warn(subject)
	return HttpResponse(status=200)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_subjects(request):

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Subject editor']:
		return HttpResponse(status=403)
		
	logging.warn('update user')
	request_user = request.user
	# subject_data = request.data
	# id_ob = subject_data['id']
	subject = Subject.objects.get(id=int(request.data['id']))
	subject.delete()
	return HttpResponse({"message":"subject deleted"},status=200)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createsample(request, format=None):
	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Sample editor']:
		return HttpResponse(status=403)

	cancertype = request.data['cancertype']
	subject_id = request.data['subject_id']

	ct = Cancertype.objects.filter(name__in=cancertype)
	if not ct:
		return HttpResponse(status=404)
	logging.warn(ct)
	
	d = {'cancer': CancertypeSerializer(ct, many=True).data, 'subject': subject_id }

	sampleSerializer = SampleSerializer(data=d)
	if not sampleSerializer.is_valid():
		return Response(sampleSerializer.errors, status=400)

	a = sampleSerializer.save()

	user.save()

	return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_samples(request, format=None):

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Sample editor']:
		return HttpResponse(status=403)
	
	samples = Sample.objects.all()
	sampleSerializer = SampleSerializer(samples, many=True)

	result = {
		'samples_data': sampleSerializer.data,
	}

	return JSONResponse(result)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_samples(request):

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Sample editor']:
		return HttpResponse(status=403)

	logging.warn(request.data)
	request_user = request.user
	sample_data = request.data
	id_ob = sample_data['id']
	sample = Sample.objects.get(id=int(id_ob))
	sampleSerializer = SampleSerializer(sample, sample_data)
	if not sampleSerializer.is_valid():
		return Response(sampleSerializer.errors)
	sampleSerializer.save()
	logging.warn(sample)
	return HttpResponse(status=200)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_samples(request):

	user = Hospuser.objects.get(username=request.user.username)

	if not user:
		return HttpResponse(status=404)
	if user.role not in ['Admin', 'Sample editor']:
		return HttpResponse(status=403)

	logging.warn('update user')
	request_user = request.user
	# subject_data = request.data
	# id_ob = subject_data['id']
	sample = Sample.objects.get(id=int(request.data['id']))
	sample.delete()
	return HttpResponse({"message":"sample deleted"},status=200)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_subjects_id(request, format=None):
	subjects = Subject.objects.all()
	subjectidSerializer = SubjectIdSerializer(subjects, many=True)

	result = {
		'subjects_id_data': subjectidSerializer.data,
	}

	return JSONResponse(result)