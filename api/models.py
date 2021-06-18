from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    email = models.EmailField()

    class Meta:
        db_table = "patient"


class BodyPart(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "body_part"
        ordering = ['name']

    def __str__(self):
        return self.name


class Type(models.Model):
    '''
    Notes: README.md -> # about the app_names and table_names
        the table name "type" it does not give enough
        information when the db is displayed in a db software.
    '''
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "type"
        ordering = ['name']

    def __str__(self):
        return self.name


class Study(models.Model):
    URGENCIES = (('LOW', 'Low'), ('MID', 'Mid'), ('HIGH', 'High'))
    urgency_level = models.CharField(
        max_length=5,
        choices=URGENCIES)
    body_part = models.ForeignKey(
        BodyPart,
        related_name='studies',
        on_delete=models.RESTRICT)
    description = models.TextField()
    type = models.ForeignKey(
        Type,
        related_name='studies',
        on_delete=models.RESTRICT)
    patient = models.ForeignKey(
        Patient,
        related_name='studies',
        on_delete=models.RESTRICT)

    class Meta:
        db_table = "study"
