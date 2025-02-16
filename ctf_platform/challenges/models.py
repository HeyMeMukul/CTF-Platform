from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('participant', 'Participant'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=11, choices=ROLE_CHOICES, default='participant')  # Corrected max_length to fit the longest choice

    # Prevent reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username


class Challenge(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    TYPE_CHOICES = (
        ('web', 'Web Exploitation'),
        ('crypto', 'Cryptography'),
        ('reverse', 'Reverse Engineering'),
        ('linux', 'Linux'),
        ('Steganography', 'Steganography'),
        ('forensics', 'Forensics'),
        ('misc', 'Miscellaneous'),


    )
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)  # Enforce unique titles
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    points = models.PositiveIntegerField(default=50)
    challenge_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    flag = models.CharField(max_length=100)  # Use flag validation in views or forms
    is_active = models.BooleanField(default=True)
    attach = models.FileField(upload_to='uploads/', blank=True, null = True)
    


    def __str__(self):
        return self.title


from django.core.exceptions import ValidationError

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    submitted_flag = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Check if a correct submission already exists for the user and challenge
        if self.is_correct:
            existing_correct_submission = Submission.objects.filter(
                user=self.user,
                challenge=self.challenge,
                is_correct=True
            ).exists()

            if existing_correct_submission:
                raise ValidationError("You have already made a correct submission for this challenge.")

    def save(self, *args, **kwargs):
        # Run custom validation before saving
        self.clean()

        # Call the original save method to actually save the object
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.challenge.title} - {"Correct" if self.is_correct else "Incorrect"}'
