Clone the project from the master branch:


git clone https://github.com/menOtabek/authentication_task.git
cd to project
Checkout the development branch and update it:


git checkout development
git pull origin development
Create and activate a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate     # for macOS/Linux
venv\Scripts\activate        # for Windows
Install the required packages:


pip install -r requirements.txt
Copy the example environment file and configure it:


cp .env_example .env
Open .env and fill in the necessary environment variables like SECRET_KEY, database settings, Telegram bot token, etc.

Run migrations:

python manage.py makemigrations
python manage.py migrate
Start the development server:
python manage.py runserver

To register a user, send a POST request to /api/v1/auth/register/ with the phone number.
After registering, the OTP code will be sent to the Telegram channel:
Link to channel: https://t.me/+QqnlguB8X-QyZjZi

Use the received OTP to verify the phone number by sending a POST request to /api/v1/auth/verify/ with the phone number and OTP code.

After verification, login by sending a POST request to /api/v1/auth/login/ with the phone number and OTP code.

Access and refresh tokens will be returned on successful login.

To view the list of users via /api/v1/users/, the logged-in user must have an admin role.

No authentication is required for the following endpoints:
/api/v1/auth/register/, /api/v1/auth/verify/, /api/v1/auth/login/.

All OTP codes are sent via Telegram channel instead of SMS.
