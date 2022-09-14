import psycopg2


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='foodtrucks',
                            #user=os.environ['DB_USERNAME'],
                            #password=os.environ['DB_PASSWORD']
                            user='postgres',
                            password='arent123')
    return conn


def get_trucks_locations(x, y):
    data_keys = ['longitude', 'latitude', 'applicant']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select {data_keys} from trucks where ST_DWithin( POINT({x}, {y})::GEOMETRY,trucks.location::geometry, 0.03);'.format(x=x,y=y, data_keys = ", ".join(data_keys)))
    data = cur.fetchall()
    data = [dict(zip(data_keys, values)) for values in data]
    cur.close()
    conn.close()
    return data

def add_user(user, password, email, salt):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO accounts (username, password, email, salt) VALUES (\'{user}\', \'{password}\', \'{email}\', \'{salt}\');'.format(user=user, password=password, email=email, salt=salt))
    conn.commit()
    cur.close()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from accounts where username = \'{user}\';'.format(user=username))
    account = cur.fetchall()
    cur.close()
    conn.close()
    return account