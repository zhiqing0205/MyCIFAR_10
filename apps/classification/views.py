import os
import time

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from MyCIFAR_10 import settings
from MyCIFAR_10.settings import BASE_DIR
from apps.classification.models import ClassificationRecord
from utils.test import *


def save_images(file):
    file_name = ''
    if file:
        dir = os.path.join(os.path.join(BASE_DIR, 'media'), 'classification', 'images')

        lt = time.localtime()
        st = str(time.strftime("%Y-%m-%d_%H%M%S", lt))
        # 格式化时间
        file_name = '%s-%s.%s' % (file.name.split('.')[0], st, file.name.split('.')[1])

        destination = open(os.path.join(dir, file_name), 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    if file_name == '':
        return ''
    return os.path.join('classification', 'images', file_name)


@require_POST
def upload_img_to_classify(request):
    file = request.FILES.get("file", None)
    print(file)
    path = ''
    if file:
        path = save_images(file)

    name = path

    img_path = os.path.join(os.path.join(BASE_DIR, 'media'), path)

    print(img_path)

    result, probability, probability_list, = classify(img_path)
    probability = round(float(probability) * 100, 2)
    probability_list = [round(float(i) * 100, 2) for i in probability_list]
    ClassificationRecord.objects.create(result=result, probability=probability, probability_list=probability_list, image=path)

    return JsonResponse({"data": {'imgUrl': settings.MEDIA_URL + path, 'result': result, 'probability': probability, 'probability_list': probability_list}})


def classifyRecords(request):
    records = ClassificationRecord.objects.exclude(image='').order_by('-time')
    print(records[0].to_dict())
    return JsonResponse({"data": [ record.to_dict() for record in records]})