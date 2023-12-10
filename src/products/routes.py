from flask import redirect , render_template , url_for , flash , request, session , g
from src import db , app , photos
from .models import Brand , Category , Addproduct
import secrets
from .forms import Addproducts


@app.route('/addbrand', methods = ['GET', 'POST'])
def addbrand():
    if not g.logged_in:
        flash('please login first', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added' , 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands= 'brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if not g.logged_in:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    updatebrand = Brand.query.get_or_404(request.args.get('id'))
    brand = request.form.get('brand')

    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/addcategory', methods = ['GET', 'POST'])
def addcat():
    if request.method == 'POST':
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The category {getbrand} was added' , 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    
    return render_template('products/addbrand.html', brands= 'brands')


@app.route('/updatecat/<int:id>', methods = ['GET', 'POST'])
def updatecategory():
    if not g.logged_in:
        flash('please login first', 'danger')
    updatecat = Category.query.get_or_404(id)
    Category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = Category
        flash(f'The category has been added' , 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html',  title='update category page', updatecat= updatecat)



@app.route('/addproduct', methods = ['GET', 'POST'])
def Addproduct():
    
    brands = Brand.query.all()
    Categories = Category.query.all()
    form = Addproducts(request.form)
    
    if not g.logged_in:
        flash('please login first', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        discription = form.discription.data
        brand = request.form.get('brand')
        Category = request.form.get('category')
        image_1 = photos.save(request.files.get('images_1'), name=secrets.token_hex(16)+",")
        image_2 = photos.save(request.files.get('images_2'), name=secrets.token_hex(16)+",")
        image_3 = photos.save(request.files.get('images_3'), name=secrets.token_hex(16)+",")
        addpro = Addproduct(name=name, price=price ,  discount=discount , stock=stock , colors=colors , discription = discription , brand_id = brand ,Category_id = Category , image_1 = image_1 , image_2 = image_2 , image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} was added' , 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title="Add product Page", form=form , brands = brands , Categories = Categories)


