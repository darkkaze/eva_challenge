import logging

from api.models import BodyPart, Study, Type
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .factories import PatientFactory, StudyFactory

logger = logging.getLogger('debug')
faker = Faker()
User = get_user_model()


def _study_to_dict(study: Study) -> dict:
    data = {
        'patient': study.patient.id,
        'urgency_level': study.urgency_level[0],
        'body_part': study.body_part.name,
        'description': study.description,
        'type': study.type.name
    }
    return data


class StudyTests(APITestCase):

    def setUp(self):
        User.objects.create(username='test',
                            is_superuser=True,
                            is_staff=True,
                            is_active=True)
        token = Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.patient1 = PatientFactory()
        self.patient2 = PatientFactory()
        self.study1 = StudyFactory(patient=self.patient1)
        self.study2 = StudyFactory(patient=self.patient2)
        self.study3 = StudyFactory(patient=self.patient1)
        self.study4 = StudyFactory(patient=self.patient2)

    def test_create_study(self):
        """
        Ensure api create a new study.
        """
        study = StudyFactory.stub(patient=self.patient1)
        url = reverse(
            'study_list_create', kwargs={'patient_pk': self.patient1.id})
        data = _study_to_dict(study)
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['patient'], study.patient.id)

    def test_get_studies(self):
        """
        Ensure api return a list of studies
        """
        url = reverse(
            'study_list_create',  kwargs={'patient_pk': self.patient1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 2)

    def test_get_study(self):
        """
        Ensure api return a study
        """
        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.study1.id)

    def test_partial_update_study(self):
        """
        Ensure api do a partial update a study
        """

        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        data = {
            'body_part': BodyPart.objects.exclude(
                name=self.study1.body_part.name).first().name,
            'type': Type.objects.exclude(
                name=self.study1.type.name).first().name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['body_part'], data['body_part'], response.data)
        self.assertEqual(response.data['type'], data['type'])

    def test_update_study(self):
        """
        Ensure api update a study
        """

        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        data = _study_to_dict(self.study1)
        data.update({
            'body_part': BodyPart.objects.exclude(
                name=self.study1.body_part.name).first().name,
            'type': Type.objects.exclude(
                name=self.study1.type.name).first().name})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['body_part'], data['body_part'], response.data)
        self.assertEqual(response.data['type'], data['type'])

    def test_delete_study(self):
        """
        Ensure api delete a study
        """
        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data)


class StudyNoCredentialsTests(APITestCase):

    def setUp(self):
        self.patient1 = PatientFactory()
        self.patient2 = PatientFactory()
        self.study1 = StudyFactory(patient=self.patient1)
        self.study2 = StudyFactory(patient=self.patient2)
        self.study3 = StudyFactory(patient=self.patient1)
        self.study4 = StudyFactory(patient=self.patient2)

    def test_create_study(self):
        """
        Unauthorized api create a new study.
        """
        study = StudyFactory.stub(patient=self.patient1)
        url = reverse(
            'study_list_create', kwargs={'patient_pk': self.patient1.id})
        data = _study_to_dict(study)
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_get_studies(self):
        """
        Unauthorized api return a list of studies
        """
        url = reverse(
            'study_list_create',  kwargs={'patient_pk': self.patient1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_get_study(self):
        """
        Unauthorized api return a study
        """
        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_partial_update_study(self):
        """
        Unauthorized api do a partial update a study
        """

        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        data = {
            'body_part': BodyPart.objects.exclude(
                name=self.study1.body_part.name).first().name,
            'type': Type.objects.exclude(
                name=self.study1.type.name).first().name}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_update_study(self):
        """
        Unauthorized api update a study
        """

        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        data = _study_to_dict(self.study1)
        data.update({
            'body_part': BodyPart.objects.exclude(
                name=self.study1.body_part.name).first().name,
            'type': Type.objects.exclude(
                name=self.study1.type.name).first().name})
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_delete_study(self):
        """
        Ensure api delete a study
        """
        url = reverse(
            'study_get_update_delete',
            kwargs={'patient_pk': self.patient1.id, 'pk': self.study1.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
