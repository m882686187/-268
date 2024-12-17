
import matplotlib
import logging
import json
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 显示负号

from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@api_view(['POST'])
def BarChart(request):
    file = request.FILES.get('file')
    x_axis = request.POST.get('x_axis')
    y_axis = request.POST.get('y_axis')
    y_data_processing = request.POST.get('y_data_processing', 'all')  # 获取 Y 轴数据处理方式
    custom_number = request.POST.get('custom_number', 1)  # 获取自定义数量，默认值为 1

    if not file or not x_axis or not y_axis:
        return JsonResponse({'error': '文件或列名未提供'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 读取数据
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return JsonResponse({'error': '不支持的文件类型'}, status=400)

            if x_axis not in df.columns or y_axis not in df.columns:
                return JsonResponse({'error': '选择的列名不存在'}, status=400)

            # 处理 Y 轴数据
            if y_data_processing == 'top':
                df = df.groupby(x_axis)[y_axis].sum().nlargest(int(custom_number))
            elif y_data_processing == 'bottom':
                df = df.groupby(x_axis)[y_axis].sum().nsmallest(int(custom_number))
            else:  # 'all'
                df = df.groupby(x_axis)[y_axis].sum()

            plt.figure(figsize=(10, 6))
            df.plot(kind='bar')
            plt.title(f'{y_axis} 按 {x_axis} 分组的柱状图')
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)

            # 确保图表保存到 media
            chart_path = os.path.join(settings.MEDIA_ROOT, 'chart.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"Chart saved at: {chart_path}")  # 打印文件路径

            chart_url = f"{request.scheme}://{request.get_host()}/media/chart.png"
            return JsonResponse({'chart_url': chart_url})

        except Exception as e:
            return JsonResponse({'error': f'数据处理错误: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'文件保存错误: {str(e)}'}, status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@api_view(['POST'])
def LineChart(request):
    file = request.FILES.get('file')
    x_axis = request.POST.get('x_axis')
    y_axis = request.POST.get('y_axis')
    y_data_processing = request.POST.get('y_data_processing', 'all')
    custom_number = request.POST.get('custom_number', 1)

    if not file or not x_axis or not y_axis:
        return JsonResponse({'error': '文件或列名未提供'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 读取数据
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return JsonResponse({'error': '不支持的文件类型'}, status=400)

            if x_axis not in df.columns or y_axis not in df.columns:
                return JsonResponse({'error': '选择的列名不存在'}, status=400)

            # 处理 Y 轴数据
            if y_data_processing == 'top':
                df = df.groupby(x_axis)[y_axis].sum().nlargest(int(custom_number))
            elif y_data_processing == 'bottom':
                df = df.groupby(x_axis)[y_axis].sum().nsmallest(int(custom_number))
            else:
                df = df.groupby(x_axis)[y_axis].sum()

            plt.figure(figsize=(12, 6))  # 调整图表大小
            ax = df.plot(kind='line')
            plt.title(f'{y_axis} 按 {x_axis} 分组的折线图', fontsize=14)
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel(y_axis, fontsize=12)

            # 设置 X 轴刻度和标签
            ax.set_xticks(range(0, len(df.index), 2))  # 只显示每隔一个标签
            ax.set_xticklabels(df.index[::2], rotation=45, fontsize=10)  # 设置 X 轴标签旋转和字体大小

            plt.tight_layout()  # 自动调整布局

            chart_path = os.path.join(settings.MEDIA_ROOT, 'line_chart.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"Line chart saved at: {chart_path}")

            chart_url = f"{request.scheme}://{request.get_host()}/media/line_chart.png"
            return JsonResponse({'chart_url': chart_url})

        except Exception as e:
            return JsonResponse({'error': f'数据处理错误: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'文件保存错误: {str(e)}'}, status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)






logger = logging.getLogger(__name__)

@api_view(['POST'])
def PieChart(request):
    file = request.FILES.get('file')
    category_column = request.POST.get('category_column')  # 获取单个分类列
    value_column = request.POST.get('value_column')
    num_options = request.POST.get('num_options')  # 获取用户选择的显示数量
    display_option = request.POST.get('display_option')  # 获取显示选项（前N项、后N项或全部）

    # 检查必需的参数
    if not file or not category_column or not value_column or not num_options:
        return JsonResponse({'error': '文件或列名未提供'}, status=400)

    # 确保 num_options 是整数
    try:
        num_options = int(num_options)
    except ValueError:
        return JsonResponse({'error': 'num_options 必须是一个整数'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)

    try:
        # 保存上传的文件
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 读取数据
        if file.name.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return JsonResponse({'error': '不支持的文件类型'}, status=400)

        # 检查列名是否存在
        if category_column not in df.columns:
            return JsonResponse({'error': f'列名 {category_column} 不存在'}, status=400)

        if value_column not in df.columns:
            return JsonResponse({'error': '选择的数值列不存在'}, status=400)

        # 处理数据，按分类列进行分组并求和
        pie_data = df.groupby(category_column)[value_column].sum()

        # 根据显示选项过滤数据
        if display_option == 'top':
            pie_data = pie_data.nlargest(num_options)  # 获取前N项
        elif display_option == 'bottom':
            pie_data = pie_data.nsmallest(num_options)  # 获取后N项
        elif display_option == 'all':
            pass  # 不做任何过滤
        else:
            return JsonResponse({'error': '无效的显示选项'}, status=400)

        # 检查饼图数据是否为空
        if pie_data.empty:
            return JsonResponse({'error': '饼图数据为空，请检查输入数据'}, status=400)

        # 绘制饼图
        plt.figure(figsize=(8, 8))

        # 自定义显示数值和百分比的函数
        def func(pct, allval):
            absolute = int(round(pct / 100. * sum(allval)))
            return f'{absolute} ({pct:.1f}%)'

        # 绘制饼图，确保传递标签
        wedges, texts, autotexts = plt.pie(
            pie_data,
            labels=pie_data.index,  # 使用分类列的名称作为标签
            autopct=lambda pct: func(pct, pie_data),
            startangle=90,
            colors=plt.cm.Paired.colors,
            wedgeprops=dict(edgecolor='w')
        )

        plt.setp(autotexts, size=10, weight="bold", color="white")  # 设置数值文本的样式
        plt.title(f'{value_column} 按 {category_column} 的饼图')
        plt.ylabel('')  # 不显示 Y 轴标签

        # 保存图表到 media
        chart_path = os.path.join(settings.MEDIA_ROOT, 'pie_chart.png')
        plt.savefig(chart_path)
        plt.close()

        # 构造图表的 URL
        chart_url = f"{request.scheme}://{request.get_host()}/media/pie_chart.png"
        return JsonResponse({'chart_url': chart_url})

    except pd.errors.EmptyDataError:
        return JsonResponse({'error': '上传的文件为空'}, status=400)
    except pd.errors.ParserError:
        return JsonResponse({'error': '解析文件时出错'}, status=400)
    except Exception as e:
        logger.error(f"数据处理错误: {str(e)}")
        return JsonResponse({'error': f'数据处理错误: {str(e)}'}, status=500)

    finally:
        # 清理上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)



@api_view(['POST'])
def BoxChart(request):
    print("Request data:", json.dumps(request.POST))  # 打印 POST 数据
    print("Files:", request.FILES)  # 打印上传的文件

    file = request.FILES.get('file')
    x_axis = request.POST.get('x_axis')
    y_axis = request.POST.get('y_axis')

    if not file or not y_axis:
        return JsonResponse({'error': '文件或 Y 轴列名未提供'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return JsonResponse({'error': '不支持的文件类型'}, status=400)

            print("DataFrame columns:", df.columns)  # 打印 DataFrame 的列名

            if y_axis not in df.columns:
                return JsonResponse({'error': f'选择的 Y 轴列名不存在: {y_axis}'}, status=400)

            plt.figure(figsize=(12, 6))
            ax = df.boxplot(column=y_axis, by=x_axis, grid=False)
            plt.title(f'{y_axis} 按 {x_axis} 分组的箱线图', fontsize=14)
            plt.suptitle('')
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel(y_axis, fontsize=12)
            plt.tight_layout()

            chart_path = os.path.join(settings.MEDIA_ROOT, 'box_chart.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"Box chart saved at: {chart_path}")

            chart_url = f"{request.scheme}://{request.get_host()}/media/box_chart.png"
            return JsonResponse({'chart_url': chart_url})

        except Exception as e:
            return JsonResponse({'error': f'数据处理错误: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'文件保存错误: {str(e)}'}, status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@api_view(['POST'])
def ScatterPlot(request):
    print("Request data:", json.dumps(request.POST))  # 打印 POST 数据
    print("Files:", request.FILES)  # 打印上传的文件

    file = request.FILES.get('file')
    x_axis = request.POST.get('x_axis')
    y_axis = request.POST.get('y_axis')
    y_data_processing = request.POST.get('y_data_processing')
    custom_number = request.POST.get('custom_number', 10)  # 默认值为 10

    if not file or not x_axis or not y_axis:
        return JsonResponse({'error': '文件、X 轴列名或 Y 轴列名未提供'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    try:
        # 保存上传的文件
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            # 读取文件内容
            if file.name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return JsonResponse({'error': '不支持的文件类型'}, status=400)

            print("DataFrame columns:", df.columns)  # 打印 DataFrame 的列名

            # 检查列名
            if x_axis not in df.columns or y_axis not in df.columns:
                return JsonResponse({'error': f'选择的列名不存在: {x_axis} 或 {y_axis}'}, status=400)

            # 处理 Y 轴数据
            if y_data_processing == "top":
                df = df.nlargest(int(custom_number), y_axis)
            elif y_data_processing == "bottom":
                df = df.nsmallest(int(custom_number), y_axis)

            # 绘制散点图
            plt.figure(figsize=(12, 6))
            plt.scatter(df[x_axis], df[y_axis], alpha=0.5)
            plt.title(f'{y_axis} vs {x_axis} 散点图', fontsize=14)
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel(y_axis, fontsize=12)
            plt.grid(True)
            plt.tight_layout()

            chart_path = os.path.join(settings.MEDIA_ROOT, 'scatter_plot.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"Scatter plot saved at: {chart_path}")

            chart_url = f"{request.scheme}://{request.get_host()}/media/scatter_plot.png"
            return JsonResponse({'chart_url': chart_url})

        except Exception as e:
            return JsonResponse({'error': f'数据处理错误: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'文件保存错误: {str(e)}'}, status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)




@api_view(['POST'])
def RadarChart(request):
    file = request.FILES.get('file')
    selected_column = request.POST.get('selected_column')
    selected_element = request.POST.get('selected_element')

    if not file or not selected_column or not selected_element:
        return JsonResponse({'error': '文件、分析列或分析元素未提供'}, status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    try:
        # 保存上传的文件
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            # 读取文件内容
            if file.name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return JsonResponse({'error': '不支持的文件类型'}, status=400)

            # 检查列名
            if selected_column not in df.columns:
                return JsonResponse({'error': f'选择的列名不存在: {selected_column}'}, status=400)

            # 获取分析元素的值
            if selected_element not in df[selected_column].values:
                return JsonResponse({'error': f'选择的分析元素不存在: {selected_element}'}, status=400)

            # 筛选出与选定元素相同的行
            selected_row = df[df[selected_column] == selected_element]

            # 选择数值列
            numeric_df = selected_row.select_dtypes(include=['number'])

            if numeric_df.empty:
                return JsonResponse({'error': f'所选分析元素没有数值数据: {selected_element}'}, status=400)

            # 获取数值和类别
            values = numeric_df.values.flatten().tolist()
            categories = numeric_df.columns.tolist()

            # 计算角度
            angles = [n / float(len(categories)) * 2 * 3.141592653589793 for n in range(len(categories))]
            values += values[:1]  # 闭合雷达图
            angles += angles[:1]   # 闭合雷达图

            # 绘制雷达图
            plt.figure(figsize=(6, 6), dpi=120)
            ax = plt.subplot(111, polar=True)
            ax.set_theta_offset(3.141592653589793 / 2)
            ax.set_theta_direction(-1)

            plt.xticks(angles[:-1], categories)
            ax.plot(angles, values, linewidth=2, linestyle='solid')
            ax.fill(angles, values, 'b', alpha=0.1)

            chart_path = os.path.join(settings.MEDIA_ROOT, 'radar_chart.png')
            plt.savefig(chart_path)
            plt.close()

            chart_url = f"{request.scheme}://{request.get_host()}/media/radar_chart.png"
            return JsonResponse({'chart_url': chart_url})

        except Exception as e:
            return JsonResponse({'error': f'数据处理错误: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'文件保存错误: {str(e)}'}, status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

