app_name      = "noe-backend"
# app_image_url = "074164835766.dkr.ecr.eu-central-1.amazonaws.com/noe-backend"
env_vars = {
  DJANGO_DATABASE_HOST    = "noe-postgres.co7irzuctvdj.eu-central-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT    = "5432"
  DJANGO_DATABASE_USER    = "noe_master"
  DJANGO_DATABASE_NAME    = "noe_db"
  ALLOWED_CORS_HOSTS      = "https://regisztracio.tesztallomas.hu"
  EMAIL_BACKEND           = "django.core.mail.backends.smtp.EmailBackend"
  FRONTEND_URL            = "https://regisztracio.tesztallomas.hu"
  DJANGO_EMAIL_HOST         = "email-smtp.eu-central-1.amazonaws.com"
  DJANGO_EMAIL_PORT         = "587"
  DJANGO_EMAIL_USE_TLS      = "true"
  DJANGO_DEFAULT_FROM_EMAIL = "no-reply@tesztallomas.hu"
}

env_secrets = {
  DJANGO_SECRET_KEY         = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD  = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_database_password"
  EMAIL_VERIFICATION_KEY    = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/email_verification_key"
  DJANGO_EMAIL_HOST_USER     = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-common/backend/aws-ses-smtp-user"
  DJANGO_EMAIL_HOST_PASSWORD = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-common/backend/aws-ses-smtp-password"
}

app_tg_ports = {
  "8000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 1
cooldown_seconds = 3

cw_log_group_name   = "noe-ecs-private-cluster"
cw_log_group_region = "eu-central-1"
