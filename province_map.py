# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020/5/31 10:01 上午
# 绘制个人足迹地图：省市范围
import yaml
from pyecharts.charts import Map
from pyecharts import options as opts

# 省和直辖市下面的市
with open("travel_config.yml", 'r', encoding='utf-8') as ymlfile:
    province_city_dict = yaml.safe_load(ymlfile)


for province, cities in province_city_dict.items():

    map = Map(init_opts=opts.InitOpts(width='1200px', height='800px'))
    map.set_global_opts(
        title_opts=opts.TitleOpts(title="个人足迹地图-%s" % province),
        visualmap_opts=opts.VisualMapOpts(max_=1, is_piecewise=True,
                                          pieces=[
                                            {"max": 1, "min": 1, "label": "去过", "color": "#4EA397"},
                                            {"max": 0, "min": 0, "label": "未去过", "color": "#FFFFFF"},
                                            ])  #最大数据范围，分段
                                         )
    city_dict = dict(zip(cities, [1]*len(cities)))
    map.add("个人足迹地图-%s" % province, data_pair=city_dict.items(), maptype=province, is_roam=True)
    map.render('./provinces/%s.html' % province)
    print("生成个人足迹地图-%s 成功" % province)