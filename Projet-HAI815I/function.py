from math import sqrt

import requests
from bs4 import BeautifulSoup
import json as js
import csv
import pandas as pd
import os
from urllib.parse import quote
def getCode(node1):
    url = 'http://jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + node1 + '&rel='
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    if(soup.find("code")!=None):
        return (soup.find("code").get_text()).splitlines()
    else:
        return None


def getIdNodeRelation(nameNR, liste):
    for id, name in liste:
        if name == nameNR:
            return id;


def getNameNode(idN, liste):
    for id, name in liste:
        if str(idN) == id:
            return name;


def getSortanteOrEntrante(idNode, idRelation, df):
    listSortantes = []
    listEntrante = []
    for index, row in df.iterrows():
        if int(row['node1']) == int(idNode) and int(row['relation']) == int(idRelation) and row['w'] > 0:
            listSortantes.append(row)
        if int(row['node2']) == int(idNode) and int(row['relation']) == int(idRelation) and row['w'] > 0:
            listEntrante.append(row)
    return listSortantes, listEntrante

def getAllRelationsSortante(idNode, df):
    list = []
    for index, row in df.iterrows():
        if int(row['node1']) == int(idNode) and not int(row['relation']) == 6 and row['w'] > 0:
            list.append(row)
    return list
def getRelationsSortante(idNode, idRelation, df):
    list = []
    for index, row in df.iterrows():
        if int(row['node1']) == int(idNode) and int(row['relation']) == int(idRelation) and row['w'] > 0:
            list.append(row)
    return list

def getRelationsEntrante(idNode, idRelation, df):
    list = []
    for index, row in df.iterrows():
        if int(row['node2']) == int(idNode) and int(row['relation']) == int(idRelation) and row['w'] > 0:
            list.append(row)
    return list


def getRelation(idNode1, idNode2, idRelation, df):
    list = []
    for index, row in df.iterrows():
        if int(row['node1']) == int(idNode1) and int(row['relation']) == int(idRelation) and row['w'] > 0 and int(row['node2']) == int(idNode2):
            list.append(row)
    return list


def parseCSV(relations, fileCSV):
    listNodes = []
    listRelations = []
    relationSortante = False
    with open(fileCSV, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['rid', 'node1', 'node2', 'relation', 'w', "type"])

        for r in relations:
            # Si la ligne commence par 'r;' : une relation
            if r.startswith('//') and "relations sortantes" in r:
                relationSortante = True
            elif r.startswith('//') and "relations entrantes" in r:
                relationSortante = False
            elif r.startswith('r;'):
                r = r[2:]
                if relationSortante:
                    r += ";sortante"
                else:
                    r += ";entrante"
                row = r.strip().split(';')
                writer.writerow(row)
            # Si la ligne commence par 'e;' : nom des noeuds relation
            elif r.startswith('e;'):
                elements = r.split(";")
                idTerme = elements[1]
                nomTerme = elements[2].strip("'")
                l = [idTerme, nomTerme]
                listNodes.append(l)
            # Si la ligne commence par 'rt;' : noms des relation
            elif r.startswith('rt;'):
                elements = r.split(";")
                idTerme = elements[1]
                nomTerme = elements[2].strip("'")
                l = [idTerme, nomTerme]
                listRelations.append(l)
    return listNodes, listRelations

def sortFunction(elem):
    return elem['w']
def inference(idNode1,idNode2,idRelation,df,listNodes,function,index1,index2):
    listNode2Relation = []
    # Récupérer tout les relations de type node1  r_isa node
    relationIsa = function(idNode1, 6, df)

    # Récupérer tout les noeud node tel que node1 r_isa node
    node1IsaNode2 = []
    for r in relationIsa:
        nodePoid = []
        nodePoid.append(getNameNode(r[index1], listNodes))
        nodePoid.append(r[index2])
        node1IsaNode2.append(nodePoid)

    # Récupérer toutes les relations tel que node relation node2
    # Le problème c'est que je dois faire des requêtes pour chaque noeud contenu dans node1IsaNode2

    for node in node1IsaNode2:
        n = getIdNodeRelation(node[0], listNodes)
        code = getCode(node[0])
        if n != None and code != None:
            listNodes1, listRelations1 = parseCSV(code, 'temporaryFile.csv')
            dfTemporary = pd.read_csv("temporaryFile.csv", sep=';')
            os.remove("temporaryFile.csv")

            nodeListSortante = getRelation(n, idNode2, idRelation, dfTemporary)
            if len(nodeListSortante) > 0:
                nodeListSortante[0]['w'] = sqrt(node[1] * nodeListSortante[0]['w'])
                listNode2Relation.append(nodeListSortante[0])

    return listNode2Relation



