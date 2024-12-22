# CTF Platform

A fully functional Capture The Flag (CTF) platform designed for hosting cybersecurity challenges. This platform provides an engaging environment for players, a leaderboard for tracking scores, and an admin interface for managing challenges.

## Features

### Player Features
- **User Registration and Login**: Players can create accounts and log in to participate.
- **Challenge Solving**: Players can view and solve challenges by submitting flags.
- **Leaderboard**: A dynamic leaderboard displays players' rankings based on their scores.

### Admin Features
- **Challenge Management**: Admins can create, edit, and delete challenges through an intuitive admin portal.
- **Category and Difficulty Levels**: Challenges can be categorized and assigned difficulty levels.
- **Leaderboard Management**: Admins can view and monitor leaderboard activity.

### Platform Features
- **Responsive Design**: The platform is optimized for use on desktop and mobile devices.
- **Secure Flag Submission**: Prevents unauthorized access and ensures data integrity.
- **Real-time Updates**: Automatically updates the leaderboard as players solve challenges.

## Tech Stack
- **Backend**: Django Framework
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Database**: SQLite (or any Django-compatible database)
- **Deployment**: Heroku (or any cloud-based hosting platform)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HeyMeMukul/CTF-Platform
   cd ctf-platform
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000` in your browser to access the platform.

6. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account for accessing the admin portal.

## Usage

### For Players
1. Register and log in to the platform.
2. Browse available challenges and solve them by submitting the correct flags.
3. Track your progress on the leaderboard.

### For Admins
1. Log in to the admin portal using your superuser credentials.
2. Create and manage challenges, including setting their difficulty, category, and flag.
3. Monitor the leaderboard and player activity.

## Deployment

To deploy the platform to Heroku:
1. **Install Heroku CLI** and log in:
   ```bash
   heroku login
   ```

2. **Create a Heroku App**:
   ```bash
   heroku create your-app-name
   ```

3. **Push the Code to Heroku**:
   ```bash
   git push heroku main
   ```

4. **Run Migrations on Heroku**:
   ```bash
   heroku run python manage.py migrate
   ```

5. **Collect Static Files**:
   ```bash
   heroku run python manage.py collectstatic
   ```

6. **Access Your App**:
   Visit `https://your-app-name.herokuapp.com`.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.



### Contact
If you have any questions or feedback, feel free to reach out via [memukuljoshi@gmail.com].
