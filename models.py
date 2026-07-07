from django.db import models
from django.contrib.auth.models import User

class HeartPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.FloatField()
    sex = models.IntegerField()
    cp = models.IntegerField()
    trestbps = models.FloatField()
    chol = models.FloatField()
    fbs = models.IntegerField()
    restecg = models.IntegerField()
    thalach = models.FloatField()
    exang = models.IntegerField()
    oldpeak = models.FloatField()
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()
    prediction = models.CharField(max_length=25)  # "High risk" or "Low risk"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.age} yrs - {self.prediction}"

class PatientUser(User):
    class Meta:
        proxy = True
        verbose_name = "User Detail"
        verbose_name_plural = "User Details"

class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = "Admin Detail"
        verbose_name_plural = "Admin Details"
