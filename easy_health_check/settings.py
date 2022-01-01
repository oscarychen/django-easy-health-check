from django.conf import settings
from django.test.signals import setting_changed

USER_SETTINGS = getattr(settings, "DJANGO_EASY_HEALTH_CHECK", None)

DEFAULTS = {
    "PATH": "/healthcheck/",
    "RETURN_STATUS_CODE": 200,
    "RETURN_BYTE_DATA": "",
    "RETURN_HEADERS": None
}


class HealthCheckSettings:
    def __init__(self, user_settings=None, defaults=None):
        self._user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "DJANGO_EASY_HEALTH_CHECK", {})
        return self._user_settings

    def __getattr__(self, attr):

        # check the setting is accepted
        if attr not in self.defaults:
            raise AttributeError(f"Invalid DJANGO_EASY_HEALTH_CHECK setting: {attr}")

        # get from user settings or default value
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


health_check_settings = HealthCheckSettings(USER_SETTINGS, DEFAULTS)


def reload_health_check_settings(*args, **kwargs):
    print("Reloading health check settings")
    setting = kwargs["setting"]
    if setting == "DJANGO_EASY_HEALTH_CHECK":
        health_check_settings.reload()


setting_changed.connect(reload_health_check_settings)
