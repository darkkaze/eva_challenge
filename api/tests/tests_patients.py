import logging

from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .factories import PatientFactory

logger = logging.getLogger(__name__)
faker = Faker()
User = get_user_model()


class PatientTests(APITestCase):

    def setUp(self):
        User.objects.create(username='test',
                            is_superuser=True,
                            is_staff=True,
                            is_active=True)
        token = Token.objects.get(user__username='test')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.patient1 = PatientFactory()
        self.patient2 = PatientFactory()

    def test_create_patient(self):
        """
        Ensure api create a new patient.
        """
        patient = PatientFactory.stub()
        url = reverse('patient_list_create')
        response = self.client.post(url, patient.__dict__, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['first_name'], patient.first_name)
        self.assertEqual(response.data['last_name'], patient.last_name)
        self.assertEqual(response.data['birth_date'], patient.birth_date)

    def test_get_patients(self):
        """
        Ensure api return a list of patients
        """
        url = reverse('patient_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 2)

    def test_get_patient(self):
        """
        Ensure api return a patients
        """
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['first_name'], self.patient1.first_name)

    def test_partial_update_patient(self):
        """
        Ensure api do a partial update a patient
        """

        first_name = faker.first_name()
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.patch(
            url, {'first_name': first_name}, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['first_name'], first_name)

    def test_update_patient(self):
        """
        Ensure api update a patient
        """

        first_name = faker.first_name()
        data = {
            'first_name': first_name,
            'last_name': self.patient1.last_name,
            'birth_date': self.patient1.birth_date,
            'email': self.patient1.email}
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['first_name'], first_name)

    def test_delete_patient(self):
        """
        Ensure api delete a patient
        """
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data)


class PatientNoCredentialsTests(APITestCase):

    def setUp(self):
        self.patient1 = PatientFactory()
        self.patient2 = PatientFactory()

    def test_create_patient(self):
        """
        Unauthorized api create a new patient.
        """
        patient = PatientFactory.stub()
        url = reverse('patient_list_create')
        response = self.client.post(url, patient.__dict__, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_get_patients(self):
        """
        Unauthorized api return a list of patients
        """
        url = reverse('patient_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_get_patient(self):
        """
        Unauthorized api return a patients
        """
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_partial_update_patient(self):
        """
        Unauthorized api do a partial update a patient
        """

        first_name = faker.first_name()
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.patch(
            url, {'first_name': first_name}, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_update_patient(self):
        """
        Unauthorized api update a patient
        """

        first_name = faker.first_name()
        data = {
            'first_name': first_name,
            'last_name': self.patient1.last_name,
            'birth_date': self.patient1.birth_date,
            'email': self.patient1.email}
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)

    def test_delete_patient(self):
        """
        Unauthorized api delete a patient
        """
        url = reverse(
            'patient_get_update_delete', kwargs={'pk': self.patient1.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
