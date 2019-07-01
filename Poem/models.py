import datetime

from SmartDjango import SmartModel, ErrorCenter, E, Packing, Param
from django.db import models
from django.db.models import Q


class PoemError(ErrorCenter):
    POEM_NOT_FOUND = E("不存在的诗歌")
    CREATE_POEM = E("发布诗歌失败")


PoemError.register()


class Poem(SmartModel):
    MAX_L = {
        'title': 100,
    }

    title = models.CharField(
        verbose_name='诗名',
        max_length=MAX_L['title'],
    )

    content = models.TextField(
        verbose_name='正文',
    )

    create_time = models.DateTimeField(
        verbose_name='发布时间',
    )

    @classmethod
    @Packing.pack
    def create(cls, title, content):
        crt_time = datetime.datetime.now()

        try:
            poem = cls(
                title=title,
                content=content,
                create_time=crt_time,
            )
            poem.save()
        except Exception as err:
            return PoemError.CREATE_POEM
        return poem

    @classmethod
    @Packing.pack
    def get_by_id(cls, poem_id):
        try:
            poem = cls.objects.get(pk=poem_id)
        except cls.DoesNotExist:
            return PoemError.POEM_NOT_FOUND
        return poem

    @staticmethod
    def _search_keyword(v):
        return Q(title__contains=v) | Q(content__contains=v)

    def _readable_id(self):
        return self.pk

    def _readable_create_time(self):
        return self.create_time.timestamp()

    def d_create(self):
        return self.dictor(['id'])

    def d_list(self):
        return self.dictor(['id', 'title', 'create_time'])

    def d(self):
        return self.dictor(['title', 'content', 'create_time'])


PM_TITLE, PM_CONTENT = Param.from_fields(Poem.get_fields(['title', 'content']))
