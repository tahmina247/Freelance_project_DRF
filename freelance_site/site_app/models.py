from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)
    ROLE_CHOICES = (
        ("admin", "admin"),
        ("client", "client"),
        ("freelancer", "freelancer"),
    )
    role = models.CharField(max_length=24, choices=ROLE_CHOICES)
    bio = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    social_links = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.username}, {self.role}'


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category_name}'


class Project(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    budget = models.PositiveIntegerField(default=0)
    deadline = models.DateField()
    STATUS_CHOICES = (
        ('open', 'open'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    category = models.ForeignKey(Category, related_name='projects', on_delete=models.CASCADE)
    skills_required = models.TextField(null=True, blank=True)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects_client')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.category}, {self.client}'


class Offer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_offer')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='freelance_offers')
    message = models.CharField(max_length=500)
    proposed_budget = models.PositiveIntegerField(default=0)
    proposed_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project}, {self.freelancer}'


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_review')
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviewer')
    target = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='target')
    star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviewer}, {self.project}, {self.star}'




