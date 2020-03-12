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
        elif '个人售汇' in context or '个人结汇' in context:
            if record.status == '支出':
                category = '外汇卖出'
            else:
                category = '外汇买入'
            return '内部转账', category, ''

        elif 'ATM取款' in context:
            return '内部转账', '取现', ''
        elif '花呗' in context:
            return '支出', '还债', '花呗'
        elif '网转' in context:
            status = '支出'
            category = '还债'
            subcategory = '信用卡'
            return status, category, subcategory
        elif '还款' in context:
            status = '支出'
            category = '还债'
            subcategory = '信用卡'
            return status, category, subcategory
        elif '信用卡' in context and '还款' in context:
            status = '支出'
            category = '还债'
            subcategory = '信用卡'
            return status, category, subcategory
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

        return category, subcategory
