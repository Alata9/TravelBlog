from django.contrib.auth.models import User
from django.db import models


from .utilities import get_timestamp_path

#  рубрика
class Rubric(models.Model):
    name = models.CharField(max_length=225, db_index=True, unique=True, verbose_name='Name')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Order')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT,
                                     null=True, blank=True, verbose_name='Super_rubric')


#  надрубрика
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    object = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Sub_rubric'
        verbose_name_plural = 'Sub_rubrics'


#  подрубрика
class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    object = SubRubricManager()

    def __str__(self):
        return '%s: %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Sub_rubric'
        verbose_name_plural = 'Sub_rubrics'


#  дополнительные иллюстрации
class AdditionalImage(models.Model):
    bb = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='The note')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'


#  объявление
class Article(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Rubric')
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Show?')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Image')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']