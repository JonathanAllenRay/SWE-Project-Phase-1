import json
import psycopg2
import requests
import math
import wikipedia

curr_conflict_id = 0
curr_country_id = 0
###
# Test functions, not core part of module, but useful for reference
###
def get_countries_from_json_demo() : 
    with open('countries.json', errors='ignore') as json_data:    
        data = json.load(json_data)
        for country in data:
            print(country.get("flag"))

def get_countries_from_url() :
    response = requests.get('https://restcountries.eu/rest/v2/all')
    data = response.json()
    for country in data:
        print(country.get("flag"))

def get_news_from_url() :
    response = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=ffeeaaeb16eb4b0b966afe73655743f6')
    data = response.json()
    articles = data.get("articles")
    for art in articles :
        print(art.get("author"))

# https://help.compose.com/docs/postgresql-and-python
def put_data_in_table_demo() :
    conn = psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')
    cur = conn.cursor()
    sql_string = """INSERT INTO practice (names)
        VALUES (%s)"""
    cur.execute(sql_string, ('Mary',))
    conn.commit()
    if conn != None:
        conn.close()

def string_to_id (s):
    if s == None:
        return -1
    if len(s) > 16:
        s = s[:16]
        print(s)
        print(int.from_bytes(s.encode(), 'little'))
    return int.from_bytes(s.encode(), 'little')

def id_to_string (n):
    if s == None:
        return -1
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

def get_wiki_desc(name) :
    description = "No description available."
    try:
        description = wikipedia.WikipediaPage(name).summary
    except:
        pass
    return description
###
# End of Demo region
###

def get_conflicts_from_json(json_file) :
    with open(json_file, errors='ignore') as json_data:    
        data = json.load(json_data)
        return data
    return None    

def get_countries_from_json(json_file) : 
    with open(json_file, errors='ignore') as json_data:    
        data = json.load(json_data)
        return data
    return None

def put_data_in_table(sql_string, conn, data, args_tuple) :
    cur = conn.cursor()
    cur.execute(sql_string, args_tuple)
    conn.commit()

def make_conflict_args_tuple(data) :
    name = data.get("Conflict")
    global curr_conflict_id
    conflict_id = curr_conflict_id
    curr_conflict_id += 1
    deaths = data.get("Cumulative fatalities")
    recent_deaths = data.get("Fatalities in 2018")
    related_countries = data.get("Location").split(", ")
    related_news = [-1]
    year_started = data.get("Start of conflict")
    return (conflict_id, deaths, name, recent_deaths, related_countries, year_started, related_news)

def make_countries_args_tuple(data, conn) :
    name = data.get("name")
    print(name)
    global curr_country_id
    country_id = curr_country_id
    curr_country_id += 1
    region = data.get("region")
    flag = data.get("flag")
    related_conflicts = search_related_conflict(data, conn, name)
    num_ongoing_conflicts = len(related_conflicts)
    if num_ongoing_conflicts <= 0 :
        print('Excluded ' + name + '.')
        return None
    capital = data.get("capital")
    related_charities = [-1]
    year_started = data.get("Start of conflict")
    return (country_id, name, region, num_ongoing_conflicts, capital, related_conflicts, related_charities, flag)

def search_related_conflict(data, conn, name) :
    sql = 'SELECT id FROM conflicts WHERE related_countries && \'{%s}\'::text[]' % (name,)
    cur = conn.cursor()
    conflicts_list = []
    try:
        cur.execute(sql)
        conflicts_list = cur.fetchall()
    except:
        print('No conflicts related to: ' + name)
    return make_int_list(conflicts_list)

def put_conflicts_in_table(json_file) :
    data = get_conflicts_from_json(json_file)
    conn = psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')
    sql_string = """INSERT INTO conflicts (id, deaths, name, recent_deaths, related_countries, year_started, 
        related_news)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    for data_dict in data:
        args = make_conflict_args_tuple(data_dict)
        put_data_in_table(sql_string, conn, data_dict, args)
    if conn != None:
        conn.close()

def put_countries_in_table(json_file) :
    data = get_countries_from_json(json_file)
    sql_string = """INSERT INTO countries (id, name, region, num_ongoing_conflicts, capital, 
        related_conflicts, related_charities, flag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    for data_dict in data:
        # For some unknown reason, only about half the list will have conflicts counted
        # if we do not make a new connection each time. It runs slower, but works fine.
        conn = qconn()
        args = make_countries_args_tuple(data_dict, conn)
        if args != None: 
            put_data_in_table(sql_string, conn, data_dict, args)
            print('Put ' + args[1] + ' into table with conflicts = ' + str(args[3]))
        if conn != None:
            conn.close()

def clear_table (table_to_clear):
    conn = psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')
    cur = conn.cursor()
    sql_string = """DELETE FROM %s""" % (table_to_clear,)
    cur.execute(sql_string)
    conn.commit()
    if conn != None:
        conn.close()

#https://stackoverflow.com/questions/16606357/how-to-make-a-select-with-array-contains-value-clause-in-psql
def demo_sql_1() :
    conn = psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')
    cur = conn.cursor()
    sql_string = 'SELECT * FROM conflicts WHERE related_countries && \'{Democratic Republic of the Congo}\'::text[]'
    cur.execute(sql_string)
    print(cur.fetchone())
    conn.commit()
    if conn != None:
        conn.close()

def demo_sql_2() :
    conn = psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')
    cur = conn.cursor()
    sql_string = 'SELECT * FROM conflicts WHERE related_countries && \'{Democratic Republic of the Congo}\'::text[]'
    cur.execute(sql_string)
    print(cur.fetchone())
    conn.commit()
    if conn != None:
        conn.close()

def demo_sql_3() :
    conn = psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')
    sql = 'SELECT id FROM conflicts WHERE related_countries && \'{%s}\'::text[]' % ('Yemen',)
    cur = conn.cursor()
    conflicts_list = []
    try:
        cur.execute(sql)
        conflicts_list = cur.fetchall()
        make_int_list
    except:
        pass
    result = make_int_list(conflicts_list)
    print(result)

def demo1 () :
    with open('countries.json', errors='ignore') as json_data:    
        data = json.load(json_data)
        for country in data:
            if country.get("name") == "Yemen":
                print("hello!!!")


# Should take in a list of tuples that contain 1 int each
def make_int_list(list_arg) :
    result = []
    for x in list_arg :
        result.append(x[0])
    return result

def qconn() :
    return psycopg2.connect(
        host = 'armedconflicts.citm2bumyzxi.us-east-2.rds.amazonaws.com',
        port = 5432,
        user = 'armedconflicts',
        password = 'dripharder',
        database = 'ArmedConflictsDB')

def put_all_conflicts() : 
    put_conflicts_in_table('conflicts_major.json')
    put_conflicts_in_table('conflicts_semimajor.json')
    put_conflicts_in_table('conflicts_small.json')
    put_conflicts_in_table('conflicts_tiny.json')

def run_main () :
    put_countries_in_table('countries.json')
    #put_all_conflicts()   

#https://stackoverflow.com/questions/31701991/string-of-text-to-unique-integer-method
if __name__ == "__main__":
    clear_table('countries')
    run_main()