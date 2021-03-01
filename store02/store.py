from flask import Flask, redirect, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def index():
    with open('lulu.csv', 'r') as f:
        data = [dict(item) for item in csv.DictReader(f)]

        try:
            page = int(request.args.get('page'))
        except:
            page = 0

        items_per_page = 16

        index_from = 0

        if range(page - 1):
            index_from += items_per_page

        index_to = index_from + items_per_page

        # Debugging pages
        # print('page:', page)
        # print('per page:', items_per_page)
        # print('from:', index_from)
        # print('to:', index_to)

        total_pages = range(int(len(data) / items_per_page))

    return render_template('index.html', data=data[index_from: index_to], total_pages=total_pages, str=str)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)