# -*- coding: utf-8 -*-

import socket
import inspector
import MySQLdb as DB


def do(docs):
    HOST = '58.229.105.83'
    PORT = 5656

    diction = make_dic()
    docs = inspector.inspector(docs, "seg")

    words = docs.split()
    tmp = []
    msg = str(1)
    for word in words:
        try:
            if diction[word]:
                tmp.append(int(diction[word]))

        except:
            pass

    returnee = sorted(set(tmp))

    for element in returnee:
        plus = " %s:1" % element
        msg += plus

    doc = msg + "!"

    doc = doc.strip()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(doc)
    data = client.recv(1024)
    client.close()

    return data


def make_dic():
    tmp = {}

    connect = None
    try:
        connect = DB.connect(host="61.43.139.115", user="jaeyoung", db="jaeyoung", passwd="asdfasdf", charset="utf8")
        cursor = connect.cursor()
        query = """
            select * from tistory_word
        """
        cursor.execute(query)
        words = cursor.fetchall()

        for word in words:
            tmp[word[1]] = word[0]

    except connect:
        pass

    finally:
        if connect:
            connect.close()

    return tmp