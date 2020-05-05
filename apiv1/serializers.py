from django.core.validators import RegexValidator

from rest_framework import serializers
from mbti.models import Mbti

class MbtiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mbti
        fields = ['content']
        # exclude = ['created_at']
        extra_kwargs = {
            'content' : {
                'write_only' : True,
                'validators' : [
                    RegexValidator(
                        r'^[a-zA-Z0-9\s\n!-/:-@¥[-`{-~]+$', message="This field only allows English"
                    )
                ]
            }
        }