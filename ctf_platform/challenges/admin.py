from django.contrib import admin
from .models import User, Challenge, Submission

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'points','challenge_type','attach' ,'is_active')
    list_filter = ('difficulty', 'challenge_type', 'is_active')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'is_correct', 'timestamp')
    list_filter = ('is_correct', 'timestamp')
