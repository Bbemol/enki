FLASK_ENV=development
FLASK_APP=src/entrypoints/flask_app
DEBUG=True
SECRET_KEY=changeme
DATABASE_URI=postgresql://postgres:pg-password@postgres:5432/enki-dev

#### TWILIO
TWILIO_ACCOUNT_SID=aski-it
TWILIO_AUTH_TOKEN=ask-it

#### Not used for now
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=redis://redis

SIG_API_URL=http://docker.for.mac.localhost:8083
SIG_API_KEY=ffef5b1a-d4bd-4b08-9b75-c7ab4f9aa14b

KEYCLOAK_BASE_URL=http://keycloak:8080/auth/
KEYCLOAK_REALM=enki
KEYCLOAK_USERNAME=admin
KEYCLOAK_PASSWORD=Pa55w0rd

# Emails
EMAIL_HOST=smtp.online.net
EMAIL_PORT=465
EMAIL_USER=no-reply@enki-crise.fr
EMAIL_PASSWORD=ask-it

ENKI_FRONT_URL=http://localhost:1337