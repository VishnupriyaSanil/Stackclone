from django.db import models

# Create your models here.
from email.policy import default
from django.db import models
from django.db.models import Count

# Create your models here.
from django.contrib.auth.models import User


class Questions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    @property
    def fetch_answers(self):
        answers=self.answers_set.all().annotate(up_count=Count("up_vote")).order_by("-up_count")
        return answers

    def _str_(self):
        return self.question


class Answers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    up_vote=models.ManyToManyField(User,related_name="upvotes")
    created_date=models.DateField(auto_now_add=True)


    def _str_(self):
        return self.answer