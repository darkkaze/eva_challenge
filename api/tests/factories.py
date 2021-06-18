import factory
from api.models import BodyPart, Patient, Study, Type
from factory.django import DjangoModelFactory

# from faker import Faker


class PatientFactory(DjangoModelFactory):
    class Meta:
        model = Patient

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date')
    email = factory.Faker('email')


class StudyFactory(DjangoModelFactory):
    class Meta:
        model = Study

    patient = factory.Iterator(Patient.objects.all())
    urgency_level = factory.Iterator(Study.URGENCIES)
    body_part = factory.Iterator(BodyPart.objects.all())
    description = factory.Faker('text')
    type = factory.Iterator(Type.objects.all())
