# Django-easy-health-check

Django-easy-health-check is a Django package that provides an easy-to-use middleware to allow health check.

## Motivation

Django's ALLOWED_HOSTS setting often would prevent health check from being completed successfully in production. A
common method of getting around this involves making a request to fetch ip address about the instance itself and adding
it to the ALLOWED_HOSTS. This approach often varies depending on deployment platform/environment.

This package provides a simple middleware that allows requests to a specified health check path to be made without
checking against ALLOWED_HOSTS setting. This negates the need to modify ALLOWED_HOSTS setting in runtime, and is
therefore platform-agnostic.

## Quick start

Install using pip:

```
pip install django-easy-health-check
```

Or, install from source:

```commandline
pip install git+https://github.com/oscarychen/django-easy-health-check.git
```

Add the health check middleware to Django settings before `django.middleware.common.CommonMiddleware`:

```python
MIDDLEWARE = [
    ...,
    'easy_health_check.middleware.HealthCheckMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```

By default, the health check url will be available at "example.com/healthcheck/".

## Settings

You can customize and overwrite the default settings by including the following in your project's settings.py:

```python
DJANGO_EASY_HEALTH_CHECK = {
    "PATH": "/healthcheck/",
    "RETURN_STATUS_CODE": 200,
    "RETURN_BYTE_DATA": "",
    "RETURN_HEADERS": None
}
```

In production, you may also want to set the following Django settings:

```python
ALLOWED_HOSTS = ["example.com"]
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [r'^healthcheck/$']
```