from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from math import floor
from . models import Product
from . import db

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('home.html', user = current_user)

@views.route('/produits')
@login_required
def produits():
    search = request.args.get('search')

    if search:
        products = Product.query.filter_by(wilaya=search).all()
    else:
        products = Product.query.all()

    return render_template("produits.html", products=products)

@views.route('/produit')
@login_required
def produit():
    id = request.args.get('id')
    product = Product.query.filter_by(id=id).first()
    autosuffisance=floor(product.production_qte / product.consommation_qte * 100)
    return render_template("produit.html", product=product, autosuffisance=autosuffisance)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'GET':
        products = Product.query.all()
        return render_template("admin.html", products=products)
    elif request.method == 'POST': 
        toDelete = request.form.get('toDelete')

        print('delete', toDelete)
        if (toDelete):
            Product.query.filter_by(id=toDelete).delete()
            db.session.commit()
            return redirect(url_for('views.admin'))
        else:
            name = request.form.get('name')
            type = request.form.get('type')
            category = request.form.get('category')
            wilaya = request.form.get('wilaya')
            production_qte = request.form.get('production_qte')
            consommation_qte = request.form.get('consommation_qte')
            new_product = Product(name = name, type = type, category = category, wilaya = wilaya, production_qte = production_qte, consommation_qte = consommation_qte)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('views.admin'))
