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

province_dict = dict(zip(province_city_dict.keys(), [1]*len(province_city_dict.keys())))
print(province_dict)

# maptype='china' 只显示全国直辖市和省级
map = Map(init_opts=opts.InitOpts(width='1200px', height='800px'))
map.set_global_opts(
    title_opts=opts.TitleOpts(title="个人足迹地图"),
    visualmap_opts=opts.VisualMapOpts(max_=1, is_piecewise=True,
                                      pieces=[
                                        {"max": 1, "min": 1, "label": "去过", "color": "#4EA397"},
                                        {"max": 0, "min": 0, "label": "未去过", "color": "#FFFFFF"},
                                        ])  #最大数据范围，分段
                                     )
map.add("个人足迹地图", data_pair=province_dict.items(), maptype="china", is_roam=True)
map.render('全国.html')