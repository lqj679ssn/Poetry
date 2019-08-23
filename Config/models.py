from django.db import models
import pypinyin
from SmartDjango import ErrorCenter, SmartModel, Packing, E


class ConfigError(ErrorCenter):
    CREATE_CONFIG = E("更新配置错误", hc=500)
    CONFIG_NOT_FOUND = E("不存在的配置", hc=404)


ConfigError.register()


class Config(SmartModel):
    MAX_L = {
        'key': 100,
        'value': 255,
    }

    key = models.CharField(
        max_length=MAX_L['key'],
        unique=True,
    )

    value = models.CharField(
        max_length=MAX_L['value'],
    )

    @classmethod
    @Packing.pack
    def get_config_by_key(cls, key):
        ret = cls.validator(locals())
        if not ret.ok:
            return ret

        try:
            o_config = cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            return ConfigError.CONFIG_NOT_FOUND

        return o_config

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            ret = cls.get_config_by_key(key)
            if not ret.ok:
                return default
            return ret.body.value
        except Exception as err:
            return default

    @classmethod
    @Packing.pack
    def update_value(cls, key, value):
        ret = cls.validator(locals())
        if not ret.ok:
            return ret

        ret = cls.get_config_by_key(key)
        if ret.ok:
            o_config = ret.body
            o_config.value = value
            o_config.save()
        else:
            try:
                o_config = cls(
                    key=key,
                    value=value,
                )
                o_config.save()
            except Exception as err:
                return ConfigError.CREATE_CONFIG


class ConfigInstance:
    JWT_ENCODE_ALGO = 'jwt-encode-algo'
    PROJECT_SECRET_KEY = 'project-secret-key'

    HOST = 'host'
    QITIAN_APP_ID = 'qt-app-id'
    QITIAN_APP_SECRET = 'qt-app-secret'


CI = ConfigInstance
