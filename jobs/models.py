from django.db import models
from account.models import Account
from main.models import Category, Type, Tag, Region, Company


class Jobs(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=228)
    location = models.ForeignKey(Region, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ManyToManyField(Type)
    price = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    jobs = models.OneToOneField(Jobs, on_delete=models.CASCADE)

    def __str__(self):
        return self.author


class ApplyJob(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    jobs = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    rezume = models.FileField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rezume


