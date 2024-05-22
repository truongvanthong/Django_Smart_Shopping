import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from products.models import Sentiment

def plot_sentiment(product_id, company_id):
    aspects = ['Pin', 'Tổng quan', 'Dịch vụ CSKH', 'Những khía cạnh khác']
    sentiments = ['Xấu', 'Bình thường', 'Tốt']

    sentiment = Sentiment.objects.filter(product_id=product_id, company_id=company_id)[0]

    if sentiment:
        sentiments_ratio = []
        if sentiment.s_pin:
            sentiments_ratio.append(eval(re.sub(r'\s+', ',', sentiment.s_pin)))
        else:
            sentiments_ratio.append([0, 0, 0])
        
        if sentiment.s_general:
            sentiments_ratio.append(eval(re.sub(r'\s+', ',', sentiment.s_general)))
        else:
            sentiments_ratio.append([0, 0, 0])
        
        if sentiment.s_service:
            sentiments_ratio.append(eval(re.sub(r'\s+', ',', sentiment.s_service)))
        else:
            sentiments_ratio.append([0, 0, 0])
        
        if sentiment.s_others:
            sentiments_ratio.append(eval(re.sub(r'\s+', ',', sentiment.s_others)))
        else:
            sentiments_ratio.append([0, 0, 0])
    else:
        # Handle the case when sentiment object does not exist
        sentiments_ratio = [[0, 0, 0] for _ in range(4)]
    
        # Tạo subplot với loại 'pie' và khoảng trống
    fig = make_subplots(rows=2, cols=2, subplot_titles=aspects, specs=[[{'type':'pie'}, {'type':'pie'}],[{'type':'pie'}, {'type':'pie'}]], horizontal_spacing=0.05, vertical_spacing=0.2)

    # Vẽ biểu đồ pie cho mỗi khía cạnh
    for i, aspect in enumerate(aspects):
        row = 1 if i < 2 else 2
        col = i % 2 + 1
        labels = sentiments
        values = [sentiments_ratio[i][2], sentiments_ratio[i][1], sentiments_ratio[i][0]] 
        
        # Tạo biểu đồ pie và thêm vào subplot tương ứng
        fig.add_trace(go.Pie(labels=labels, values=values, name=aspect), row=row, col=col)


    # Cài đặt layout
    fig.update_layout(
        title=f'<b>Cảm xúc trung bình của <span style="color:#FF5733">{sentiment.product.product_name}</span> trên <span style="color:#ff8a3c">{sentiment.company_id.company_name}</span></b>',
        width=600,
        height=350,
        title_x=0.5
    )
    return fig

