from flask import render_template, request, redirect, url_for, session, flash
from config import app
import database

@app.route("/")
def home():
    products = database.get_all_products()
    return render_template("home.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        existing_user = database.get_user_by_username(username)
        
        if existing_user:
            flash("Nome de usuário já existe")
            return redirect(url_for('register'))
            
        database.create_user(username, password)
        flash("Cadastro feito! Entre.")
        return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = database.get_user_by_username(username)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
            
        flash("Credenciais inválidas")
        return redirect(url_for('login'))
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template("cart.html", cart=cart, total=total)

@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = database.get_product_by_id(product_id)
    cart = session.get("cart", {})
    pid = str(product_id)
    
    current_quantity = cart.get(pid, {}).get('quantity', 0)
    
    if current_quantity < product['stock']:
        if pid in cart:
            cart[pid]['quantity'] += 1
        else:
            cart[pid] = {
                'title': product['title'],
                'price': float(product['price']),
                'quantity': 1,
                'max_stock': product['stock']
            }
        session["cart"] = cart
    else:
        flash("Sem estoque suficiente para esse produto!")
        
    return redirect(url_for('home'))

@app.route("/cart/update/<int:product_id>/<action>")
def update_cart(product_id, action):
    cart = session.get("cart", {})
    pid = str(product_id)
    
    if pid in cart:
        if action == "increase" and cart[pid]['quantity'] < cart[pid]['max_stock']:
            cart[pid]['quantity'] += 1
        elif action == "decrease" and cart[pid]['quantity'] > 1:
            cart[pid]['quantity'] -= 1
            
    session["cart"] = cart
    return redirect(url_for('view_cart'))

@app.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)
    
    if pid in cart:
        cart.pop(pid)
        
    session["cart"] = cart
    return redirect(url_for('view_cart'))

@app.route("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for('view_cart'))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for('home'))
        
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    if request.method == "POST":
        database.register_order(session['user_id'], cart, total)
        session.pop("cart", None)
        return redirect(url_for('history'))
        
    return render_template("checkout.html", total=total)

@app.route("/history")
def history():
    print(session)
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    orders = database.get_user_orders(session['user_id'])
    return render_template("history.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)