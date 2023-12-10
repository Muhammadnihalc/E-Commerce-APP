from flask import redirect , render_template , url_for , flash , request, session
from src import db , app , photos
from .models import Brand , Category , Addproduct
import secrets
from .forms import Addproducts


@app.route('/addbrand', methods = ['GET', 'POST'])
def addbrand():
    if 'email' not in session:
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


@app.route('/updatebrand', methods=['GET', 'POST'])
def updatebrand():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    updatebrand = Brand.query.get_or_404(request.args.get('id'))

    if request.method == 'POST':
        brand_name = request.form.get('brand')
        updatebrand.name = brand_name
        flash(f'The brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/updatebrand.html', title='Update Brand', updatebrand=updatebrand)


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
    if 'email' not in session:
        flash('please login first', 'danger')
    updatecat = Category.query.get_or_404(id)
    Category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = Category
        flash(f'The brand has been added' , 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',  title='update brand page',updatebrandbrand= updatecat)



@app.route('/addproduct', methods = ['GET', 'POST'])
def Addproduct():
    
    brands = Brand.query.all()
    Categories = Category.query.all()
    form = Addproducts(request.form)
    
    if 'email' not in session:
        flash('please login first', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        photos.save(request.files.get('images_1'), name=secrets.token_hex(16)+",")
        photos.save(request.files.get('images_2'), name=secrets.token_hex(16)+",")
        photos.save(request.files.get('images_3'), name=secrets.token_hex(16)+",")
    return render_template('products/addproduct.html', title="Add product Page", form=form , brands = brands , Categories = Categories)


