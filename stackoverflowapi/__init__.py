from ._celery import app as celery_app

__all__ = ('celery_app',)

"""
Почему Redis быстрее других БД SQL?
Redis работает на нашей оперативной памяти
"""