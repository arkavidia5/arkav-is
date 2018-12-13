from rest_framework import serializers

from arkav_is_api.quiz.models import QuizAttempt, Question, AttemptAnswer, QuestionSelection

class QuestionSelectionSerializer(serializers.ModelSerializer):
    key_display = serializers.CharField(source='get_key_display')
    class Meta:
        model = QuestionSelection
        fields = ['key_display','key', 'value']
class QuestionSerializer(serializers.ModelSerializer):
    selections = QuestionSelectionSerializer(many=True)
    class Meta:
        model = Question
        fields = ['identifier', 'description', 'selections']

class AttemptAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    class Meta:
        model = AttemptAnswer
        fields = ['question', 'answer']

class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = AttemptAnswerSerializer(many=True)
    class Meta:
        model = QuizAttempt
        fields = ['quiz', 'user','start_time', 'finish_time', 'answers']
class QuickSaveRequestSerializer(serializers.Serializer):
    identifier = serializers.UUIDField()
    answer = serializers.CharField(max_length=1)
