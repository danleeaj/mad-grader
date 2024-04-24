from rest_framework import serializers
from .models import Response, Round, Debate

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('type', 'model', 'content', 'time_requested')

class RoundSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True)
    class Meta:
        model = Round
        fields = ('responses', 'evaluation_error_flag', 'consensus_error_flag')

class DebateSerializer(serializers.ModelSerializer):
    rounds = RoundSerializer(many=True)
    class Meta:
        model = Debate
        fields = ('rubric_component', 'student_response', 'context', 'rounds', 'flagged') 