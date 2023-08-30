from flask import Flask, render_template, request, flash, redirect, url_for
from settings import*
from sql_queries import WebShopDB

app = Flask(__name__)
db = WebShopDB()
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")
def index():
    categoris: db.get_categori()
    items = db.get_all_items()
    return render_template("index.html", items = items, categoris = categoris ) 

@app.route("/item/<item_id>")
def item(item_id):
    item = db.get_item(item_id)
    return render_template("item.html", item = item, categoris = categoris )

@app.route("/order/<item_id>", methods = ["GET", "POST"])
def order(item_id):
    categoris = db.get_categori()
    item = db.get_item(item_id)
    if request.method == 'POST':
        try:
            db.add_order(item[0], 
                        request.form["name"], 
                        request.form["phone"],
                        request.form["email"], 
                        request.form["city"],
                        request.form["address"],
                        item[5])
            flash("Додано замавлення!", "alert-light")
            return redirect(url_for('index'))
        except:
            flash("Помилка помилка!!!!!", "alert-danger")
    return render_template("order.html", item = item, categoris = categoris ) 

@app.route("/category/<id>")
def category(id):
    categoris = db.get_categori()
    items = db.get_category_items(id)
    return render_template("category.html", items = items, categoris = categoris ) 

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True) # Запускаємо веб-сервер з цього файлу


