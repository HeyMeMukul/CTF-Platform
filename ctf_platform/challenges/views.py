from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect , get_object_or_404

from .models import Challenge, Submission
from challenges.forms import CustomUserCreationForm , CustomAuthenticationForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required



from django.contrib.auth import get_user_model
User = get_user_model()



def home(request):
    if request.user.is_authenticated:
        # Get the challenges the user has solved
        solved_challenges = Challenge.objects.filter(submission__user=request.user, submission__is_correct=True)
        challenges_solved = solved_challenges.count()

        # Calculate the user's total score (sum of points from solved challenges)
        total_score = Submission.objects.filter(user=request.user, is_correct=True).aggregate(
            total_score=Sum('challenge__points')
        )['total_score'] or 0  # Default to 0 if no score exists

        # Calculate the user's rank based on total score compared to other users
        leaderboard_data = (
            Submission.objects
            .filter(is_correct=True)
            .values('user')
            .annotate(total_score=Sum('challenge__points'))
            .order_by('-total_score')
        )

        # Rank the user
        user_rank = None
        for idx, entry in enumerate(leaderboard_data, start=1):
            if entry['user'] == request.user.id:
                user_rank = idx
                break

        # If the user is not found in the leaderboard, assign a default rank
        if user_rank is None:
            user_rank = len(leaderboard_data) + 1  # If the user is not in the leaderboard, they will be ranked last

        context = {
            'user': request.user,
            'challenges_solved': challenges_solved,
            'total_score': total_score,
            'user_rank': user_rank,
            'solved_challenges': solved_challenges,
        }
    else:
        context = {
            'user': request.user,
            'challenges_solved': 0,
            'total_score': 0,
            'user_rank': None,
            'solved_challenges': None,
        }

    return render(request, 'profile.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to a home page or dashboard after login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  

@login_required
def dashboard(request):
    challenges = Challenge.objects.filter(is_active=True)
    
    # Annotate each challenge with 'is_solved' by checking if the user has a correct submission
    for challenge in challenges:
        challenge.is_solved = Submission.objects.filter(
            user=request.user, challenge=challenge, is_correct=True
        ).exists()

    return render(request, 'dashboard.html', {'challenges': challenges})


@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
    # Annotate whether the user has solved the challenge
    challenge.is_solved = Submission.objects.filter(
        user=request.user, challenge=challenge, is_correct=True
    ).exists()

    return render(request, 'challenge_detail.html', {'challenge': challenge})

@login_required
def submit_flag(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    # Check if the user has already submitted a flag for this challenge
    existing_submission = Submission.objects.filter(user=request.user, challenge=challenge).first()

    if existing_submission and existing_submission.is_correct:
        # If the user has already submitted a correct flag, redirect to an error page or show a message
        return redirect('submission_error')  # Define this view to show the error message
  
    
    if request.method == 'POST':
        # Get the submitted flag from the form
        submitted_flag = request.POST.get('submitted_flag')

        # Ensure that the submitted flag is provided and not empty
        if not submitted_flag:
            return render(request, 'submit_flag.html', {'challenge': challenge, 'error': 'Flag cannot be empty.'})

        # Check if the submitted flag matches the correct one
        is_correct = submitted_flag == challenge.flag 

        # Create and save the new submission
        submission = Submission.objects.create(
            user=request.user,
            challenge=challenge,
            submitted_flag=submitted_flag,
            is_correct=is_correct
        )

        # Redirect to a success page or leaderboard, depending on correctness
        if is_correct:
            return redirect('submission_success')  # Define this view to show success
        elif is_correct == False:
            return redirect('submission_fail')  
        else:
            return redirect('submission_error')
        
    # For GET requests, render the form to submit the flag
    return render(request, 'submit_flag.html', {'challenge': challenge})

from django.db.models import Sum
import random

@login_required

def leaderboard(request):
    users = User.objects.filter(role='participant')  # Filter participants if role is defined
    timestamps = Submission.objects.order_by().values_list('timestamp', flat=True).distinct()
    labels = sorted([timestamp.strftime('%Y-%m-%d') for timestamp in timestamps])

    # Prepare data for the score progression chart
    datasets = []
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']  # Colors for users

    for user in users:
        user_scores = []
        cumulative_score = 0

        for timestamp in timestamps:
            # Calculate score up to each timestamp
            score = Submission.objects.filter(
                user=user,
                timestamp__lte=timestamp,
                is_correct=True
            ).aggregate(total_score=Sum('challenge__points'))['total_score'] or 0

            # Append the cumulative score at each timestamp
            user_scores.append(score)
        
        datasets.append({
            'label': user.username,
            'data': user_scores,
            'borderColor': random.choice(colors),
            'fill': False,
        })

    # Calculate current leaderboard scores for table
    leaderboard_data = (
        Submission.objects
        .filter(is_correct=True)
        .values('user')
        .annotate(total_score=Sum('challenge__points'))
        .order_by('-total_score')
    )

    user_dict = {user.id: user for user in users}
    leaderboard_data = [
        {
            'user': user_dict.get(entry['user'], None),
            'total_score': entry['total_score']
        }
        for entry in leaderboard_data
    ]
    # Calculate user's rank
    user_rank = None
    if request.user.is_authenticated:
        user_score = (
            Submission.objects
            .filter(user=request.user, is_correct=True)
            .aggregate(total_score=Sum('challenge__points'))['total_score'] or 0
        )
        leaderboard_scores = [entry['total_score'] for entry in leaderboard_data]
        user_rank = sorted(leaderboard_scores, reverse=True).index(user_score) + 1

    user_scores = []
    if request.user.is_authenticated:
        for timestamp in timestamps:
            score = Submission.objects.filter(
                user=request.user,
                timestamp__lte=timestamp,
                is_correct=True
            ).aggregate(total_score=Sum('challenge__points'))['total_score'] or 0
            user_scores.append(score)    

     # Fetch solved challenges for the user
    solved_challenges = []
    if request.user.is_authenticated:
        solved_challenges = (
            Submission.objects
            .filter(user=request.user, is_correct=True)
            .select_related('challenge')
            .values_list('challenge__title', 'challenge__points')
        )
        

    context = {
        'labels': labels,
        'datasets': datasets,
        'leaderboard': leaderboard_data,
        'user_rank': user_rank,
        'user_scores': user_scores,
        'solved_challenges': solved_challenges,

    }

    return render(request, 'leaderboard.html', context)

@login_required
def submission_error(request):
    return render(request, 'submission_error.html')

@login_required
def submission_success(request):
    return render(request, 'submission_success.html')

@login_required
def submission_fail(request):
    return render(request, 'submission_fail.html')

