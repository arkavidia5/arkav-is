from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from arkav_is_api.quiz.models import Quiz, QuizAttempt
from arkav_is_api.quiz.serializers import QuizAttemptSerializer, QuickSaveRequestSerializer


class QuizAttemptView(views.APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, quiz_slug, format=None):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        attempt = QuizAttempt.objects.filter(quiz=quiz, user=request.user).order_by('-start_time').first()

        return Response(data=QuizAttemptSerializer(attempt).data)

class QuizSaveView(views.APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, quiz_slug, format=None):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        attempt = QuizAttempt.objects.filter(quiz=quiz, user=request.user).order_by('-start_time').first()
        serialized = QuickSaveRequestSerializer(data= request.data, many=True)
        for item in serialized.validated_data:
            attemptanswer = attempt.answers.filter(question__identifier=item['identifier']).first()
            attemptanswer.answer = item['answer']
            attemptanswer.save()
        attempt.finish()
        return Response(status = 200)



class QuizQuickSaveView(views.APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, quiz_slug, format=None):
        quiz = Quiz.objects.filter(slug=quiz_slug).first()
        attempt = QuizAttempt.objects.filter(quiz=quiz, user=request.user).order_by('-start_time').first()
        if attempt.finish_time:
            return Response(status=403)
        serialized = QuickSaveRequestSerializer(data= request.data)
        if serialized.is_valid():
            attemptanswer = attempt.answers.filter(question__identifier=serialized.validated_data['identifier']).first()
            attemptanswer.answer = serialized.validated_data['answer']
            attemptanswer.save()
            return Response(status=200)
        else:
            return Response(status=400)