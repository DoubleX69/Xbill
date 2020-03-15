from .DataModel import *

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie


def draw_category_pie(pie_axis: PieAxis, inner_title="分类报表", outer_title='小类报表', width=2000) -> Pie:
    c = Pie()

    inner_radius = "70%"
    outer_radius = "80%"

    c.add(series_name=inner_title,
          data_pair=pie_axis.inner_data,
          radius=["0%", inner_radius],
          label_opts=opts.LabelOpts(position="inner"),
          )
    c.add(series_name=outer_title,
          radius=[inner_radius, outer_radius],
          data_pair=pie_axis.outer_data,
          label_opts=opts.LabelOpts(position="outside",
                                    formatter="{b}:\n{c}({d}%)",
                                    border_width=1,
                                    border_radius=4,
                                    ),
          )

    c.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"), )
    c.set_series_opts(tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"))

    return c


def draw_usage_pie(payout, budget, title) -> Pie:
    c = Pie()
    c.add(series_name=title,
          data_pair=budget,
          radius=["0%", "30%"],
          label_opts=opts.LabelOpts(position="inner"),
          )
    c.add(series_name=title,
          radius=["30%", "40%"],
          data_pair=payout,
          label_opts=opts.LabelOpts(position="outside",
                                    formatter="{b}:\n{c}({d}%)",
                                    border_width=1,
                                    border_radius=4,
                                    ),
          )

    return c


def draw_balance_bar(balance_axis: BalanceAxis, title="收支统计", markline=None, width=2000) -> Bar:
    bar = Bar()
    bar.add_xaxis(balance_axis.x_axis)

    for name, axis in balance_axis.y_axis.items():
        bar.add_yaxis(name, axis, category_gap="20%", gap="0%")

    bar.set_global_opts(title_opts=opts.TitleOpts(title=title, ),
                        datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100),
                                       opts.DataZoomOpts(type_="inside")],
                        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'))

    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    if markline is not None:
        bar.set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=markline, name='预算')]),
                            )

    return bar


def draw_surplus_line(surplus_axis: SurplusAxis, title='年度结余', width=800) -> Line:
    line = Line()
    line.add_xaxis(surplus_axis.x_date)
    line.add_yaxis("结余", surplus_axis.y_surplus)

    line.set_global_opts(title_opts=opts.TitleOpts(title=title, ), )
    # line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    return line


class BalanceBar(object):

    def __init__(self, balance_axis: BalanceAxis, title="收支统计"):
        self.balance_axis = balance_axis
        self.title = title

    def render(self) -> Bar:
        bar = Bar()
        bar.add_xaxis(self.balance_axis.x_axis)
        bar.add_yaxis("支出", self.balance_axis.y_axis_a, category_gap="20%")
        bar.add_yaxis("收入", self.balance_axis.y_axis_b, category_gap="20%")
        bar.set_global_opts(title_opts=opts.TitleOpts(title=self.title, ),
                            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100),
                                           opts.DataZoomOpts(type_="inside")],
                            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='shadow'))
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        return bar
