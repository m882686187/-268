# crawler/views.py
from django.http import JsonResponse, HttpResponse
from .dianping_spider import crawl_attractions, save_to_excel


def attractions_view(request):
    url = 'https://www.dianping.com/shanghai/ch35'  # 替换为目标地区的URL
    attractions = crawl_attractions(url)

    # 保存到Excel文件
    save_to_excel(attractions, 'attractions.xlsx')

    # 返回JSON响应
    return JsonResponse(attractions, safe=False)


def download_excel(request):
    url = 'https://www.dianping.com/shanghai/ch35'  # 替换为目标地区的URL
    attractions = crawl_attractions(url)

    # 保存到Excel文件
    filename = 'attractions.xlsx'
    save_to_excel(attractions, filename)

    # 读取Excel文件并返回
    with open(filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
