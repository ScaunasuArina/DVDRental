from werkzeug.security import generate_password_hash

users = {
    'basic_user': generate_password_hash('basic_password')
}