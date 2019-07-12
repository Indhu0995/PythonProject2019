import argparse

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm, exc

app = Flask(__name__)

database_file = "sqlite:///products.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Products(db.Model):
    product = db.Column(db.String(80),
                       unique=True,
                       nullable=False,
                       primary_key=True)


def __repr__(self):
    return "<Title : {}>".format(self.title)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        product = Products(product=request.form.get("product"))
        db.session.add(product)
        db.session.commit()
    prods = Products.query.all()
    return render_template("prod.html ", prods=prods)


@app.route("/update", methods=["GET", "POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    productup = Products.query.filter_by(product=oldname).first()
    productup.product = newname
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    product = request.form.get("product")
    productdel = Products.query.filter_by(product=product).first()
    print(productdel)
    db.session.delete(productdel)
    db.session.commit()
    return redirect("/")


def Main():
    parser = argparse.ArgumentParser(description='web app ---> amazon.fr')
    args = parser.parse_args()


if __name__ == '__main__':
    app.run()
