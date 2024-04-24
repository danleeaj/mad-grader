from django.db import models

# Create your models here.

class Response(models.Model):
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    content = models.TextField()
    time_requested = models.DateTimeField()
    time_taken = models.DateTimeField()

class Round(models.Model):
    responses = models.ManyToManyField(Response)
    evaluation_error_flag = models.BooleanField(default=False)
    consensus_error_flag = models.BooleanField(default=False)

class Debate(models.Model):
    rubric_component = models.TextField()
    student_response = models.TextField()
    context = models.TextField(null=True, blank=True)
    rounds = models.ManyToManyField(Round)
    flagged = models.BooleanField(default=False)