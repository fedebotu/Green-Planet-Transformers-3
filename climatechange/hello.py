from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

@app.route("/getweather")
def getweather():
    return render_template("form.html", messages=messages)

@app.route("/weatherresults")
def displayweatherresults():
    return render_template("weatherresults.html", messages=messages)



@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        ##content = request.form['content']

        if not title:
            flash('Title is required!')
       ## elif not content:
         ##   flash('Content is required!')
        else:
            messages.append({'title': title}) ##, 'content': content})
            return redirect(url_for('displayweatherresults'))

    return render_template('create.html')


    
if __name__ == "__main__":
    app.run(debug=True)