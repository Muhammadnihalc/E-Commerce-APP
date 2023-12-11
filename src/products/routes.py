from flask import redirect , render_template , url_for , flash , request, session , g , current_app
from src import db , app , photos
from .models import Brand , Category , Addproduct
import secrets , os
from .forms import Addproducts 


@app.route('/')
def home():
    page = request.args.get('page',1,type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page , per_page = 4)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html' , products=products , brands=brands , categories=categories)

@app.route('/product/<int:id>')
def single_page():
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/single_page.html' , product=product , brands=brands , categories=categories)



@app.route('/brand/<int:id>')
def get_brand():
    
    page = request.args.get('page',1,type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter(brand=get_b).paginate(page=page , per_page = 4)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html' , brand=brand , brands=brands , categories=categories , get_b=get_b)



@app.route('/categories/<int:id>')
def get_category():
    page = request.args.get('page',1,type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_prod= Addproduct.query.filter_by(category= get_cat).paginate(page=page , per_page = 4)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/index.html' , get_prod=get_prod , categories=categories, brands=brands , get_cat=get_cat)



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


@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(request.args.get('id'))
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'your brand {brand.name} has been deleted', 'success')
        return redirect(url_for('admin'))
    
    flash(f'your brand {brand.name} cannot be deleted', 'success')
    return redirect(url_for('admin'))   


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


@app.route('/deletecategory/<int:id>', methods=['GET', 'POST'])
def deletecategory(id):
    category = Category.query.get_or_404(request.args.get('id'))
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'your brand {category.name} has been deleted', 'success')
        return redirect(url_for('admin'))
    
    flash(f'your category {category.name} cannot be deleted', 'success')
    return redirect(url_for('admin'))  



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


@app.route('/updateproduct/<int:id>', methods = ['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    Categories = Categories.query.all()
    product = Addproduct.query.get_or_404(id)
    Category = request.form.get('category')
    brand = request.form.get('brand')
    form = Addproduct(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.color = form.color.data
        product.discription = form.discription.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('images_1'), name=secrets.token_hex(16)+",")
            except:
                product.image_1 = photos.save(request.files.get('images_1'), name=secrets.token_hex(16)+",")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('images_2'), name=secrets.token_hex(16)+",")
            except:
                product.image_2 = photos.save(request.files.get('images_2'), name=secrets.token_hex(16)+",")


        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('images_3'), name=secrets.token_hex(16)+",")
            except:
                product.image_3 = photos.save(request.files.get('images_3'), name=secrets.token_hex(16)+",")


        db.session.commit()
        flash(f'The product has been updated' , 'success')

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.discription.data = product.discription

    return render_template('products/updateproduct.html', title="Add product Page", form=form , brands = brands , Categories = Categories , product = product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =='POST':
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image_3))
            except Exception as e:
                print(e)


        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted' , 'success')
        return redirect(url_for('admin'))

    flash(f'The product cannot be deleted' , 'success')
    return redirect(url_for('admin'))

