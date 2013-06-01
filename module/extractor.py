# -*- coding: utf-8 -*-

from math import log
import psycopg2cffi as DB
import config
import operator
import data
import inspector
import HTMLParser
import chardet


def extract(Document):
    return main(Document)


def main(Document, Answers=None):
    TotalDocuments = config.TotalDocuments
    number = config.MaxNumber
    # if Answers:
    #     number = len(Answers)

    Document = filters(Document)
    KeywordList, KeywordListUnique = setKeywordList(Document)
    Ranking = takeRank(KeywordList, KeywordListUnique, TotalDocuments)

    KeywordSet = getItemFromRank(Ranking, KeywordListUnique, number)

    # for a in KeywordSet:
    #     print a[0], a[1], a[2]

    return KeywordSet


def getItemFromRank(Ranking, KeywordListUnique, n=5):
    TopBottom = sorted(Ranking.iteritems(), key=operator.itemgetter(1))
    TopBottom.reverse()

    Filter_NN = []

    for a in TopBottom:
        if "NN" in KeywordListUnique[a[0]][1]:
            Filter_NN.append((KeywordListUnique[a[0]][0], KeywordListUnique[a[0]][1], a[1]))

    if n > len(Filter_NN):
        return Filter_NN[:len(Filter_NN)]
    else:
        return Filter_NN[:n]


def takeRank(KeywordList, KeywordListUnique, TotalDocuments):
    rank = {}
    connect = None
    try:
        connect = DB.connect(host=config.host, user=config.user, password=config.password, database=config.database)
        cursor = connect.cursor()

        totalWordCount = float(len(KeywordList))
        compare = list(KeywordList)

        for idx, Keyword in enumerate(KeywordListUnique):
            realm = 0.0
            tmp = 1.0
            while True:
                if Keyword in compare:
                    tmp += 1
                    if tmp > realm:
                        realm = tmp
                    compare.remove(Keyword)
                else:
                    break
            TF = tmp / totalWordCount
            containDocs = 1.0
            try:
                cursor.execute("select * from %s where keyword = E'{%s}' "
                               "and morpheme = E'{%s}';" % (config.table, Keyword[0], Keyword[1]))
                temp = cursor.fetchone()
                if isinstance(temp, tuple):
                    containDocs = temp[1] + 1.0
                else:
                    containDocs = 1.0

            except:
                pass

            IDF = log(TotalDocuments / containDocs)
            rank[idx] = TF * IDF

    except:
        pass

    finally:
        if connect:
            connect.close()

    return rank


def filters(Document):
    Document = Document.replace("\r", "").replace("\n", "")
    Document = unEscape(Document)
    Document = Document.replace(",", "").replace("\"", "").replace("'", "").replace("{", "").replace("}", "")
    return Document


def unEscape(var):
    hp = HTMLParser.HTMLParser()
    ue = hp.unescape

    return ue(var)


def setKeywordList(document):
    SampleSpace = []

    morphemes = inspector.inspector(document)

    # segmentation depth
    segments = morphemes.split(" ")
    for segment in segments:

        # compose depth
        composes = segment.split("+")
        for wordSet in composes:

            # word depth
            words = wordSet.split("/")
            try:
                SampleSpace.append((words[0], words[1]))
            except:
                pass

    SampleSpaceUnique = list(set(SampleSpace))

    return SampleSpace, SampleSpaceUnique


if __name__ == "__main__":
    Answers = data.Keywords[15]
    Document = data.Document[15]
    main(Document, Answers)