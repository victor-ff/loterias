# -*- coding: utf-8 -*-

import time
import json
import requests
import urlloterias as urll
from bson.json_util import dumps as dps
from pymongo import MongoClient as mc


def Requisicao(bConcurso, numConcurso):
    try:
        if (bConcurso == "readDB"):
            _colecoes = Connection()
            _resultadoDB = json.loads(
                dps(_colecoes.find().sort('concurso', -1).limit(1))[1:-1])
            return _resultadoDB
        elif ((bConcurso == True) or (bConcurso == False)):
            _urlRequisicao = URL()
            if (bConcurso == False):
                _url = "{}{}{}".format(_urlRequisicao['Route'],
                                       _urlRequisicao['TimeStamp'], str(int(time.time())))
            elif (bConcurso == True):
                _url = "{}{}{}{}{}".format(_urlRequisicao['Route'],
                                           _urlRequisicao['TimeStamp'], str(
                                               int(time.time())),
                                           _urlRequisicao['Contest'], str(numConcurso))
            _resultadoJson = requests.get(_url).json()
            return _resultadoJson
        else:
            print("""
            Verificar o item passado no objeto 'concurso'!
            """)
    except Exception as e:
        print(e)
        exit()


def URL():
    _strRota = urll.url_megasena
    _strTimeStamp = urll.url_timestamp
    _strConcurso = urll.url_contest
    _urlParcial = {'Route': _strRota,
                   'TimeStamp': _strTimeStamp, 'Contest': _strConcurso}
    return _urlParcial


def Connection():
    _client = mc('localhost', 27017)
    _dataBase = _client['Loterias']
    _collections = _dataBase['Contests']
    return _collections


def InsertDB(collections, resultJson):
    _jsonConcurso = collections.insert_one(resultJson)
    return _jsonConcurso.inserted_id


def Loop(FC, LC):
    if (LC < FC):
        loop = True
    else:
        loop = False
    return loop


def PrintConcursos():
    return ("""
    Ultimo concurso no site:    {}
    Ultimo concurso no banco:   {}
    """
            .format(_concursoSite, _concursoDB))


# Faz a busca no site do utlimo concurso realizado.
_concursoSite = Requisicao(False, 0)['concurso']
# Faz a busca no banco do ultimo concurso inserido.
_concursoDB = Requisicao("readDB", 0)['concurso']
_strPrintConcurso = PrintConcursos()

print(_strPrintConcurso)

while(Loop(_concursoSite, _concursoDB)):

    _numConcurso = _concursoDB + 1
    _concursoDB = _numConcurso
    # Faz a busca no site com o numero do concurso.
    _jsonConcurso = Requisicao(True, _numConcurso)
    #_insertDB = InsertDB(Connection(), _jsonConcurso)  '''removido para teste'''

    print("Buscado no site o concurso {}, ID: {}".format(_numConcurso, _insertDB))

    time.sleep(1)  # segundo a cada requisição.

print("Dados atualizados!")
