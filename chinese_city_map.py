from pyecharts import options as opts
from pyecharts.charts import Map
import random

city = ["北京", "天津", "保定", "廊坊", "烟台", "青岛", "扬州", "镇江",
        "南京", "无锡", "苏州", "上海", "杭州", "嘉兴", "湖州", "绍兴",
        "宁波", "舟山", "台州", "金华", "武汉", "长沙", "成都", "湛江",
        "海口", "三亚", "黄山", "南昌", "九江"]
data_city = {i: 1 for i in city}
china_city = (
    Map(init_opts=opts.InitOpts(width='1200px', height='800px'))
    .add(
        "",
        data_city.items(),
        "china-cities",
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="个人足迹——地级市"),
        visualmap_opts=opts.VisualMapOpts(
            max_=1, is_piecewise=True,
            pieces=[
                {"max": 1, "min": 1, "label": "去过", "color": "#4EA397"},
                {"max": 0, "min": 0, "label": "未去过", "color": "#FFFFFF"},
            ]
        ),
    )
    .render("个人足迹——地级市.html")
)

with open("个人足迹——地级市.html", "r") as f:
    content = f.read()

content = content.split("</head>")[0]\
          + '<script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/china-cities.js"></script>\n</head>'\
          + content.split("</head>")[1]

with open("个人足迹——地级市.html", "w") as g:
    g.write(content)