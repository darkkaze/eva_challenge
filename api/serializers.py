from rest_framework import serializers

from .models import BodyPart, Patient, Study, Type


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'birth_date':
                {'help_text': 'iso format'}
        }


class StudySerializer(serializers.ModelSerializer):
    '''
    Study serializer

    notes:
        without the explicit body_part and type.
        the representation going to return the object id,
        but is more useful return the object.name

        undocumented trick:
        Explicit extra fields can correspond to any property or callable on the model.
        During the representation it going to return the str of object
        django-rest-framework.org/api-guide/serializers/#specifying-fields-explicitly

        fix the post/update:
        for saving works properly  the trick is override the validation_**
        and return the object for the user input value
    '''
    body_part = serializers.ChoiceField(choices=[])
    type = serializers.ChoiceField(choices=[])

    class Meta:
        model = Study
        fields = '__all__'

    def validate_body_part(self, value) -> BodyPart:
        """
        Check that value is in body_part catalog.
        """
        print('validate', value)
        if obj := BodyPart.objects.filter(name=value).first():
            return obj
        raise serializers.ValidationError(
            f"{value} is not in body parts catalog")

    def validate_type(self, value) -> Type:
        """
        Check that value is in type catalog
        """
        if obj := Type.objects.filter(name=value).first():
            return obj
        raise serializers.ValidationError(
            f"{value} is not in types catalog")

    def __init__(self, *args, **kwargs):
        '''
        Notes:
            lazy load of body_parts and types catalogs
            this is for show the catalog in the /api-docs/ page
        '''
        super().__init__(*args, **kwargs)
        body_parts = BodyPart.objects.all().values_list('name', flat=True)
        types = Type.objects.all().values_list('name', flat=True)
        self.fields['body_part'].choices = body_parts
        self.fields['type'].choices = types
        self.fields['body_part'].help_text = str([item for item in body_parts])
        self.fields['type'].help_text = str([item for item in types])
        self.fields['urgency_level'].help_text = str(
            [item[0] for item in Study.URGENCIES])


class StudyUpdateSerializer(StudySerializer):

    class Meta:
        model = Study
        exclude = ['patient']
