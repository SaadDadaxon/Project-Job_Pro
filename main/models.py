from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=228)

    def __str__(self):
        return self.title


class State(models.Model):
    title = models.CharField(max_length=228)

    def __str__(self):
        return self.title


class Region(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='region')
    title = models.CharField(max_length=228)

    def __str__(self):
        return f"{self.title}/{self.state.title}"


class Type(models.Model):
    title = models.CharField(max_length=228)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=228)

    def __str__(self):
        return self.title


class Company(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=88)

    def __str__(self):
        return self.title


class Contact(models.Model):
    full_name = models.CharField(max_length=228)
    email = models.EmailField(unique=True, db_index=True, max_length=88)
    subject = models.CharField(max_length=228)
    message = models.TextField()

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.email

