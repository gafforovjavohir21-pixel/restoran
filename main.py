from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'restoran_secret_2024'

users = {}

menu = [
    {"id": 1, "name": "Osh (Palov)", "price": 35000, "category": "Asosiy taomlar", "emoji": "🍚", "desc": "An'anaviy o'zbek palobi, qo'ziqorin va sabzavotlar bilan"},
    {"id": 2, "name": "Lag'mon", "price": 28000, "category": "Asosiy taomlar", "emoji": "🍜", "desc": "Qo'lda tortilgan eritma, go'sht va sabzavotlar bilan"},
    {"id": 3, "name": "Shashlik", "price": 45000, "category": "Grill", "emoji": "🍖", "desc": "Tandirda pishirilgan mol go'shti, limon va ko'k piyoz bilan"},
    {"id": 4, "name": "Somsa", "price": 8000, "category": "Snacklar", "emoji": "🥟", "desc": "Tandir somsasi, go'shtli yoki kartoshkali"},
    {"id": 5, "name": "Mastava", "price": 22000, "category": "Sho'rvalar", "emoji": "🍲", "desc": "Guruchli o'zbek sho'rvasi, go'sht va sabzavotlar bilan"},
    {"id": 6, "name": "Chuchvara", "price": 25000, "category": "Asosiy taomlar", "emoji": "🥘", "desc": "Qaynatilgan yoki qovurilgan, qatiq bilan"},
    {"id": 7, "name": "Non", "price": 5000, "category": "Snacklar", "emoji": "🫓", "desc": "Tandirda pishirilgan issiq non"},
    {"id": 8, "name": "Ko'k choy", "price": 6000, "category": "Ichimliklar", "emoji": "🍵", "desc": "Farg'ona ko'k choyi, chinni piyolada"},
    {"id": 9, "name": "Limonad", "price": 12000, "category": "Ichimliklar", "emoji": "🥤", "desc": "Tabiiy limon va nanadan tayyorlangan sovuq ichimlik"},
]

orders = []

@app.route('/')
def index():
    popular = menu[:4]
    return render_template('index.html', popular=popular)

@app.route('/menu')
def menu_page():
    category = request.args.get('category', 'Barchasi')
    categories = ['Barchasi', 'Asosiy taomlar', 'Grill', 'Sho'rvalar', 'Snacklar', 'Ichimliklar']
    if category == 'Barchasi':
        filtered = menu
    else:
        filtered = [m for m in menu if m['category'] == category]
    return render_template('menu.html', items=filtered, categories=categories, active=category)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        items = request.form['items']
        orders.append({'name': name, 'phone': phone, 'address': address, 'items': items})
        flash(f'Rahmat {name}! Buyurtmangiz qabul qilindi. 30-45 daqiqada yetkazamiz! 🚀', 'success')
        return redirect(url_for('order'))
    return render_template('order.html', menu=menu)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Xabaringiz yuborildi! Tez orada javob beramiz.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            flash(f'Xush kelibsiz, {username}! 🎉', 'success')
            return redirect(url_for('index'))
        flash('Login yoki parol noto\'g\'ri!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if username in users:
            flash('Bu foydalanuvchi nomi band!', 'danger')
        elif password != confirm:
            flash('Parollar mos kelmadi!', 'danger')
        else:
            users[username] = password
            flash('Ro\'yxatdan o\'tdingiz! Endi kiring.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Tizimdan chiqdingiz.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
