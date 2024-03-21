from django.db import models

# Create your models here.

index = [x for x in range(10)]
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


class ClassificationRecord(models.Model):
    """
    A model to store classification results.
    """
    # The image that was classified.
    image = models.ImageField(upload_to='media/classification/images/', verbose_name='图片')
    # The classification result.
    result = models.CharField(max_length=100, verbose_name='分类结果', choices=tuple(zip(index, classes)))
    # The probability of the classification result.
    probability = models.FloatField(verbose_name='概率')
    # The probability of the classification result_list.
    probability_list = models.CharField(verbose_name='概率列表', max_length=300)
    # The time the classification was made.
    time = models.DateTimeField(auto_now_add=True)
    # The user who made the classification.
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # The ip address of the user who made the classification.
    ipaddress = models.GenericIPAddressField(verbose_name='IP地址', default='127.0.0.1')

    def __str__(self):
        return '预测为 {}, 概率为{}'.format(self.result, self.probability)

    def to_dict(self):
        d = dict(zip(classes, self.probability_list[1:-1].split(', ')))
        # 给每个类别加上%
        for k, v in d.items():
            d[k] = '{}%'.format(v)

        return {
            'image': self.image.url if self.image else None,
            'result': self.result,
            'probability': str(self.probability) + '%',
            'probability_list': str(d),
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'ipaddress': self.ipaddress,
        }

    class Meta:
        db_table = 'tb_classification_record'  # 定义模型对应的数据库表名
        verbose_name = verbose_name_plural = '预测分类记录'  # 定义model的别名(后台管理)