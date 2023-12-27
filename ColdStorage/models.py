from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    regDate=models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.user.username
class ColdStorage(models.Model):
    title = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    cost = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    creationDate=models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.title
class ApplicationForm(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    storage = models.ForeignKey(ColdStorage, on_delete=models.CASCADE, null=True)
    applicationNumber = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    remark = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    fromDate = models.DateField(null=True)
    toDate = models.DateField(null=True)
    remarkDate = models.DateField(null=True)
    applyDate=models.DateField(auto_now=True,null=True)
    def __str__(self):
        return self.applicationNumber