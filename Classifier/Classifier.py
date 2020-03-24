"""
    根据账单的“交易对象，产品名称，备注” 对账单进行 分类。
    先简单根据文本内容的关键字进行分类。
    后续考虑使用深度学习进行分类。
"""

#
# 子类名称:关键字列表
#
SUBCATEGORY_KEYWORD_DICT = {
    "工资": ["工资"],
    "外卖": ['饿了么', '美团订单'],
    "食堂": ["食堂"],
    "食材": ['盒马'],
    "水果": ["水果"],
    "饮品": ['星巴克', '咖啡', '奶茶', '奶盖', 'COFFEE', 'coffee '],
    "话费充值": ['话费充值', '手机话费'],
    "电影": ['淘票票', '影城'],
    "充值": ['App Store'],
    "房租": ['房租', '月租金'],
    "物业费": ["物业"],
    "数码": ["数码", "电子", "电"],
    "鞋服": ['优衣库', '男装', '女装', '鞋', '衣', '真皮'],
    "京东": ["京东"],
    "淘宝": ["淘宝"],
    "超市": ["超市", "711", "便利店"],
    "退款": ["退款"],

}

SUBCATEGORY_CLASSIFICATION = {
    "工资": ["工资"],
    "餐饮": ["外卖", "食堂", "食材", "水果", "饮品"],
    "住房": ["房租", "物业费"],
    "购物": ["数码", "鞋服", "超市", "淘宝", "京东"],
    "交通": ["地铁", "火车票", "出租车"],
    "娱乐": ["氪金", "充值", "会员"],
    "通讯": ["话费充值", "网费"],
    "退款": ["退款"],
    "投资": ["投资"],
    "人情": ["红包"],
    "内部转账": ["内部转账"],
}


class Classifier(object):

    @classmethod
    def classify(cls, record):

        context = "{} {} {}".format(record.product_name, record.trader_name, record.remarks)

        if ('财富' in context or '定期' in context or '理财' in context or '基金' in context) and '收益发放' not in context:
            if record.status == '支出':
                return record.status, '投资', ''
            elif record.status == '收入':
                return record.status, '赎回', ''
            else:
                return record.status, record.status, ''
        elif '花呗' in context:
            return '支出', '还债', '花呗'
        else:
            if record.status == '内部转账':
                category = '内部转账'
                subcategory = ''
            else:
                category, subcategory = cls.classify_category(record)

            return record.status, category, subcategory

    @classmethod
    def classify_category(cls, record):
        # category = record.category
        # subcategory = record.subcategory

        if record.category:
            category = record.category
            subcategory = record.subcategory
        else:
            category = '其他'
            subcategory = ''

        context = "{} {} {}".format(record.product_name, record.trader_name, record.remarks)

        for sub, keys in SUBCATEGORY_KEYWORD_DICT.items():
            for key in keys:
                if key in context:
                    subcategory = sub
                    break

        if subcategory:
            for c, l in SUBCATEGORY_CLASSIFICATION.items():
                if subcategory in l:
                    category = c
                    break

        return category, subcategory
