from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Fjr',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'March 13, 2021'
    },
    {
        'author': 'Slvn',
        'title': 'Blog post 2',
        'content': 'second post content',
        'date_posted': 'March 14, 2021'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)
