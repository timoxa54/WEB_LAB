from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, name, surname, address, phone, email, password):
        self.name = name
        self.surname = surname
        self.address = address
        self.phone = phone
        self.email = email
        self.password_hash = generate_password_hash(password)


# Получить всех пользователей
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'address': user.address,
            'phone': user.phone,
            'email': user.email
        }
        user_list.append(user_data)
    return jsonify(user_list)


# Получить пользователя по ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'address': user.address,
            'phone': user.phone,
            'email': user.email
        }
        return jsonify(user_data)
    else:
        return 'Пользователь не найден'


@app.route('/reg', methods=['POST'])
def create_user():
    name = request.form.get('name')
    surname = request.form.get('surname')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('password-confirm')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return 'Пользователь с таким адресом электронной почты уже существует'

    # Проверка совпадения паролей
    if password != confirm_password:
        return 'Пароли не совпадают'

    # Создание нового пользователя
    user = User(name=name, surname=surname, address=address, phone=phone, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return 'Пользователь успешно создан'


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        # Вход выполнен успешно
        session['user'] = {
            'name': user.name,
            'email': user.email,
            'surname': user.surname,
        }
        return redirect(url_for('personal_account'))
    else:
        return 'Неверный адрес электронной почты или пароль'


@app.route('/personal-account')
def account_info():
    # Проверка наличия данных пользователя в сессии
    if 'user' in session:
        user_data = session['user']
        return render_template('personal-account.html', user=user_data)
    else:
        return 'Пользователь не авторизован'



# Обновить пользователя
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        name = request.form.get('name')
        surname = request.form.get('surname')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')

        user.name = name
        user.surname = surname
        user.address = address
        user.phone = phone
        user.email = email

        db.session.commit()

        return 'Пользователь успешно обновлен'
    else:
        return 'Пользователь не найден'


# Удалить пользователя
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

        return 'Пользователь успешно удален'
    else:
        return 'Пользователь не найден'


@app.route('/')
def home():
    return render_template('registration.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Выводим данные в терминал
        print('Имя:', name)
        print('Фамилия:', surname)
        print('Адрес доставки:', address)
        print('Номер телефона:', phone)
        print('Эл. Почта:', email)

        session['message'] = 'Данные успешно получены'

    # Получаем сообщение из сессии
    message = session.get('message', '')

    return render_template('registration.html', message=message)


@app.route('/personal-account')
def personal_account():
    # Проверка наличия данных пользователя в сессии
    if 'user' in session:
        user_data = session['user']
        return render_template('personal-account.html', user=user_data)
    else:
        return 'Пользователь не авторизован'




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
