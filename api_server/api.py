from collections import OrderedDict
from random import randint
import time

from flask import Flask
from faker import Faker


app = Flask(__name__)

# list of locales to user
# if not explicitly provided first one is used
locales = OrderedDict([
    ('ru_RU', 1),
    ('en_US', 2),
])
fake = Faker(locales)


def random_sleep(x=0, y=200):
    time.sleep(randint(x, y) * 0.001)

def create_user_obj(username=None):
    if not username:
        username = fake['en_US'].first_name().lower()

    return {
        'username': username,
        'email': fake.email(),
        'full_name': fake.name(),
        'address': fake.address(),
        'ip': fake.ipv4(network=False, address_class=None, private=None),
        'user_agent': fake.user_agent()
    }


@app.route('/api/user/<username>', methods=['GET'])
def get_user_by_username(username):
    random_sleep()
    user = create_user_obj(username)
    return user
    
@app.route('/api/users', methods=['GET'])
def get_users():
    random_sleep()
    user_list = [create_user_obj() for user in range(5)]  # number of users in list
    return {'users': user_list}
