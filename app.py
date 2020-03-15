import os
from datetime import datetime

from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename, redirect
from Models import create_table

from App import api

app = Flask(__name__)


def to_table(data: dict):
    status = []
    for k, v in data.items():
        item = {'name': k, 'balance': v}
        status.append(item)
    columns = [
        {
            "field": "name",  # which is the field's name of data key
            "title": "名称",  # display as the table header's name
            "sortable": False,
        },
        {
            "field": "balance",
            "title": "金额 (元)",
            "sortable": False,
        },
    ]

    return status, columns


@app.route("/barChart/year=<year>&month=<month>")
def get_bar_chart(year, month):
    year = int(year)
    month = int(month)
    c = api.draw_balance_bar_in_month(year, month)
    return c.dump_options()


@app.route("/PieChart/Category/year=<year>&month=<month>")
def get_category_pie(year, month):
    year = int(year)
    month = int(month)
    c = api.draw_pie_per_month(year, month)
    return c.dump_options()


@app.route("/barChart/year=<year>")
def get_annual_bar(year):
    year = int(year)
    c = api.draw_balance_bar_per_month(year=year)
    return c.dump_options()


@app.route("/PieChart/year=<year>")
def get_annual_pie(year):
    year = int(year)
    c = api.draw_pie_per_year(year=year)
    return c.dump_options()


@app.route('/barChart/annual_statistics')
def get_annual_statistics_bar():
    # bar = draw_annual_comparison()
    bar = api.draw_balance_bar_per_year()
    return bar.dump_options()


@app.route('/lineChart/annual_statistics')
def get_annual_statistics_line():
    # line = draw_annual_balance()
    line = api.draw_surplus_line_per_year()
    return line.dump_options()


@app.route("/category_statistics/year=<year>&month=<month>")
def get_category(year, month):
    name = 'select_month'
    year = int(year)
    month = int(month)

    charts = [url_for('get_category_pie', year=year, month=month)]
    # return render_template("category.html", chart_url=url_for('get_category_pie', year=t.year, month=t.month), )

    status, columns = to_table(api.account_status_per_month(year, month, prefix="{}/{}月".format(year, month)))
    return render_template("category.html", charts=charts, num=len(charts), name=name, data=status, columns=columns)


@app.route("/")
@app.route("/index")
def index():
    t = api.FinancialDateTime.current_financial_month()

    status, columns = to_table(api.account_status_per_month(t.year, t.month))

    return render_template("index.html", chart_url=url_for('get_current_month_bar'), data=status, columns=columns,
                           usage_chart=url_for("get_month_usage"))


@app.route("/current_usage")
def get_month_usage():
    t = api.FinancialDateTime.current_financial_month()
    c = api.draw_month_usage(t.year, t.month)
    return c.dump_options()


@app.route("/current_month")
def get_current_month_bar():
    t = api.FinancialDateTime.current_financial_month()
    c = api.draw_balance_bar_in_month(t.year, t.month)
    return c.dump_options()


@app.route('/load_file', methods=['GET', 'POST'])
def load_file():
    msg = ""
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            msg = api.read_csv(file_path)
            return render_template("load_file_result.html", msg=msg)
    else:
        return render_template("load_file.html")


@app.route("/details", methods=['GET', 'POST'])
def details():
    name = 'select_month'
    if request.method == 'GET':
        t = api.FinancialDateTime.current_financial_month()
    else:
        month = request.form.get(name)
        try:
            t: datetime = datetime.strptime(month, '%Y-%m')
        except ValueError:
            t = datetime.now()

    return redirect(url_for('get_details', year=t.year, month=t.month))


@app.route("/details/year=<year>&month=<month>")
def get_details(year, month):
    name = 'select_month'
    year = int(year)
    month = int(month)
    data, columns = api.get_balance_details_in_month(year, month)

    return render_template("details.html",
                           chart_url=url_for('get_bar_chart', year=year, month=month),
                           data=data, columns=columns, name=name)


@app.route("/category_statistics", methods=['GET', 'POST'])
def category_statistics():
    name = 'select_month'
    if request.method == 'GET':
        t = api.FinancialDateTime.current_financial_month()
    else:
        month = request.form.get(name)
        try:
            t: datetime = datetime.strptime(month, '%Y-%m')
        except ValueError:
            t = datetime.now()

    return redirect(url_for('get_category', year=t.year, month=t.month))


# 理财页面
@app.route("/invest/barChart/year=<year>&month=<month>")
def get_invest_bar_chart(year, month):
    year = int(year)
    month = int(month)
    c = api.draw_investment_bar_in_month(year, month)
    return c.dump_options()


@app.route("/invest/year=<year>&month=<month>")
def get_invest(year, month):
    name = 'select_month'
    year = int(year)
    month = int(month)

    return render_template("invest.html",
                           chart_url=url_for('get_invest_bar_chart', year=year, month=month),
                           name=name)


@app.route("/invest", methods=['GET', 'POST'])
def invest():
    name = 'select_month'
    if request.method == 'GET':
        t = api.FinancialDateTime.current_financial_month()
    else:
        month = request.form.get(name)
        try:
            t: datetime = datetime.strptime(month, '%Y-%m')
        except ValueError:
            t = datetime.now()

    return redirect(url_for('get_invest', year=t.year, month=t.month))


# 年度
@app.route('/annual/year=<year>')
def annual_with_year(year):
    name = 'select_year'
    year = int(year)

    status, columns = to_table(api.account_status_per_year(year, prefix="{}年".format(year)))
    return render_template("annual.html", name=name,
                           chart_url=url_for('get_annual_bar', year=year),
                           pie_url=url_for('get_annual_pie', year=year),
                           data=status, columns=columns
                           )


@app.route('/annual', methods=['GET', 'POST'])
def annual():
    name = 'select_year'
    if request.method == 'GET':
        t = datetime.now()
    else:
        year = request.form.get(name)
        try:
            t: datetime = datetime.strptime(year, '%Y')
        except ValueError:
            t = datetime.now()
    return redirect(url_for('annual_with_year', year=t.year))


@app.route("/statistics")
def annual_statistics():
    balance = api.account_surplus_from_start_to_now()
    return render_template("statistics.html",
                           bar_chart_url=url_for('get_annual_statistics_bar'),
                           line_chart_url=url_for('get_annual_statistics_line'),
                           balance=balance)


if __name__ == "__main__":

    create_table()

    # config upload_path for saving account file
    upload_path = os.path.join(os.getcwd(), "Web", "upload_file")
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    app.config['UPLOAD_FOLDER'] = upload_path

    app.run(debug=True)
