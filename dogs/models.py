from django.db import models

from users.models import NULLABLE

class Category (models.Model):
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='descriptions')

    def __str__(self):
            return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    name = models.CharField(max_length=250, verbose_name='dog_name')
    # category = models.CharField(max_length=100, verbose_name='breed')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='image')
    birth_date = models.DateField(**NULLABLE, verbose_name='birth_date')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'dog' # понятное человеку имя модели
        verbose_name_plural = 'dogs' # понятное человеку имя множественное число
        # abstaract = True # Данная модель станет абстракным базовым классом
        # app_label = 'dogs' # если модель определена за пределами app., то момжно таким образом ее к нему отнести
        # ordering =  [-1] # Изменение порядка полей модели
        # proxy = True # модель будет рассматривться как проки модель
        # permessions = [] # добавляются группы пользователей которые могут изменять сущность данной модели
        # db_table = 'doggies' # перезаписть ия таблицы в БД
        # get_latest_by = 'birth_date' # Возвращает последний объект по порядку возрастания (самая молодая собака)
