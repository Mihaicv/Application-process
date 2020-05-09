from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import random

import database_common


@database_common.connection_handler
def get_mentors(cursor: RealDictCursor) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE last_name
        LIKE %s
        ORDER BY first_name"""
    name_last=last_name
    cursor.execute(query,(name_last,))
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_city(cursor: RealDictCursor, city: str) -> list:
    query = f"""
        SELECT first_name, last_name, city
        FROM mentor
        WHERE city='{city}'
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_applicant_data_by_name(cursor: RealDictCursor, applicant_n: str) -> list:
    query=f"""
        SELECT first_name, last_name, phone_number
        FROM applicant
        WHERE first_name='{applicant_n}' OR last_name='{applicant_n}'
        ORDER BY first_name"""
    name_ap=applicant_n
    cursor.execute(query,(name_ap,))
    return cursor.fetchall()

@database_common.connection_handler
def get_applicant_data_by_email_ending(cursor: RealDictCursor, email_ending: str) -> list:
    query="""
        SELECT first_name, last_name, phone_number
        FROM applicant
        WHERE email
        LIKE %s
        ORDER BY first_name"""
    name_ap="%"+email_ending
    cursor.execute(query,(name_ap,))
    return cursor.fetchall()

@database_common.connection_handler
def get_applicants(cursor: RealDictCursor) -> list:
    query = """
            SELECT first_name, last_name, phone_number,email,application_code
            FROM applicant"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def show_applicant(cursor: RealDictCursor, application_code: int) -> list:
    query = f"""
            SELECT *
            FROM applicant
            WHERE application_code='{application_code}'
            ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def update_phone(cursor: RealDictCursor, update_phone: str,application_code:str) -> list:
    query = """
            UPDATE applicant
            SET phone_number= %(update_phone)s
            WHERE application_code= %(application_code)s
            """
    data={'update_phone':update_phone, 'application_code':application_code}
    cursor.execute(query,data)
    update_query="""
        SELECT * 
        FROM applicant
        WHERE application_code =%s
        """
    new_phone=application_code
    cursor.execute(update_query,(new_phone,))
    return cursor.fetchall()

@database_common.connection_handler
def delete_applicant(cursor: RealDictCursor,application_code:str) -> list:
    query="""
        DELETE FROM applicant
        WHERE application_code=%(application_code)s
        """
    data={'application_code':application_code}
    cursor.execute(query, data)
    update_query = """
            SELECT * 
            FROM applicant
            WHERE application_code =%s
            """
    delete = application_code
    cursor.execute(update_query, (delete,))
    return cursor.fetchall()

@database_common.connection_handler
def delete_by_mail(cursor: RealDictCursor,del_by_end_mail:str) -> list:

    query="""
        DELETE FROM applicant
        WHERE email
        LIKE %s
        """
    delete_applicant_by_mail="%"+del_by_end_mail
    cursor.execute(query,(delete_applicant_by_mail,))
    update_query="""
        SELECT *
        FROM applicant
        """
    cursor.execute(update_query)
    return cursor.fetchall()

@database_common.connection_handler
def generate_code(cursor: RealDictCursor):
    lst_application_code=[]
    for applicant in get_applicants():
            lst_application_code.append(int(applicant['application_code']))
            print(lst_application_code)
    empty_list=0
    while empty_list==0:
        code=random.randint(0,9999)
        if code not in lst_application_code:
            empty_list+=code
        return code

@database_common.connection_handler
def get_id(cursor: RealDictCursor)-> list:
    query="""
        SELECT MAX(id)
        FROM applicant
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def add_applicant(cursor: RealDictCursor,first_name:str, last_name:str,phone_number:str,email:str, application_code:str) -> list:
    query="""
        INSERT INTO applicant(first_name,last_name,phone_number,email,application_code) VALUES (%s,%s,%s,%s,%s)
        """
    data=first_name,last_name,phone_number,email,application_code
    cursor.execute(query, data)
    update_query = """
            SELECT *
            FROM applicant
            """
    cursor.execute(update_query)
    return cursor.fetchall()




   








