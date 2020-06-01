# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020/5/31 9:21 上午
# 绘制个人足迹地图：全国范围
import yaml
from pyecharts.charts import Map
from pyecharts import options as opts

# 省和直辖市
with open("travel_config.yml", 'r', encoding='utf-8') as ymlfile:
    province_city_dict = yaml.safe_load(ymlfile)

province_dict = dict(zip(province_city_dict.keys(), [len(_) for _ in province_city_dict.values()]))
print(province_dict)

# maptype='china' 只显示全国直辖市和省级
# 指定chart_id，便于后续添加JS function
map = Map(init_opts=opts.InitOpts(chart_id="123", width='1200px', height='800px'))
map.set_global_opts(
    title_opts=opts.TitleOpts(title="个人足迹地图"),
    visualmap_opts=opts.VisualMapOpts(max_=20, is_piecewise=True)
)

map.add("个人足迹地图", data_pair=province_dict.items(), maptype="china", is_roam=True)
# 添加JS function
js_func = """
        chart_123.on('click', function (param){
            var selected = param.name;
                if (selected) {
                    switch(selected){
          """

for province, cities in province_city_dict.items():
    js_func += '\t\t\t\t\t\tcase "%s":\n\t\t\t\t\t\t\tlocation.href = "provinces/%s.html";' \
               '\n\t\t\t\t\t\t\tbreak;\n' % (province, province)

js_func += "\t\t\t\t\t\tdefault:\n\t\t\t\t\t\t\tbreak;}}});"
print(js_func)
map.add_js_funcs(js_func)

map.render('全国.html')