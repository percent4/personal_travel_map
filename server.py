# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020/6/2 9:44 下午
import os

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from pyecharts.charts import Map
from pyecharts import options as opts
from pypinyin import lazy_pinyin

define("port", default=8100, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class MapHandler(tornado.web.RequestHandler):
    def post(self):
        provinces = "上海 云南 内蒙古 北京 台湾 吉林 四川 天津 宁夏 安徽 山东 山西 广东 广西 新疆 江苏 江西 河北 河南 浙江 海南 湖北" \
                    " 湖南 澳门 甘肃 福建 西藏 贵州 辽宁 重庆 陕西 青海 香港 黑龙江"
        pinyin_dict = {province: "".join(lazy_pinyin(province)) for province in provinces.split()}
        pinyin_dict["陕西"] = "shaanxi"

        # 获取参数
        province_dict = {}
        for k, v in pinyin_dict.items():
            cities = self.get_arguments(v)
            if cities:
                province_dict[k] = cities

        print(province_dict)

        # 绘制全国地图
        # 指定chart_id，便于后续添加JS function
        map = Map(init_opts=opts.InitOpts(chart_id="123", width='1200px', height='700px'))
        map.set_global_opts(
            title_opts=opts.TitleOpts(title="个人足迹地图"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical"),
            visualmap_opts=opts.VisualMapOpts(max_=20, is_piecewise=True)
        )

        map.add("个人足迹地图", data_pair={k: len(v) for k, v in province_dict.items()}.items(), maptype="china",
                is_roam=True)
        # 添加JS function
        js_func = """
                chart_123.on('click', function (param){
                    var selected = param.name;
                        if (selected) {
                            switch(selected){
                  """

        for province, cities in province_dict.items():
            js_func += '\t\t\t\t\t\tcase "%s":\n\t\t\t\t\t\t\tlocation.href = "./provinces?province=%s";' \
                       '\n\t\t\t\t\t\t\tbreak;\n' % (province, province)

        js_func += "\t\t\t\t\t\tdefault:\n\t\t\t\t\t\t\tbreak;}}});"
        map.add_js_funcs(js_func)

        print("生成个人足迹地图-全国 成功")
        map.render('./templates/全国.html')

        # 绘制每个省的地图
        for province, cities in province_dict.items():
            map = Map(init_opts=opts.InitOpts(width='1200px', height='700px'))
            map.set_global_opts(
                title_opts=opts.TitleOpts(title="个人足迹地图-%s" % province),
                toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical"),
                visualmap_opts=opts.VisualMapOpts(max_=1, is_piecewise=True,
                                                  pieces=[
                                                      {"max": 1, "min": 1, "label": "去过", "color": "#4EA397"},
                                                      {"max": 0, "min": 0, "label": "未去过", "color": "#FFFFFF"},
                                                  ])  # 最大数据范围，分段
            )
            city_dict = dict(zip(cities, [1] * len(cities)))
            map.add("个人足迹地图-%s" % province, data_pair=city_dict.items(), maptype=province, is_roam=True)
            map.render('./templates/provinces/%s.html' % province)
            print("生成个人足迹地图-%s 成功" % province)

        self.render("全国.html")


class ProvinceHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./provinces/%s.html" % self.get_argument("province"))


def main():
    if not os.path.exists("./templates/provinces"):
        os.mkdir("templates/provinces")
        # os.system("mkdir -p ./templates/provinces")
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            handlers=[(r'/index', IndexHandler),
                      (r'/map', MapHandler),
                      (r'/provinces', ProvinceHandler)
                      ],
            template_path=os.path.join(os.path.dirname(__file__), "templates")
          )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


main()