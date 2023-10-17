from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    create_at = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    blog_text = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    RATE_CHOICES = (
        (5, "excellent"),
        (4, "vey good"),
        (3, "good"),
        (2, "not bad"),
        (1, "bad"),

    )
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
