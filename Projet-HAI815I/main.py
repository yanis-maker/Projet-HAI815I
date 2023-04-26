import requests
from bs4 import BeautifulSoup
import json as js
import csv
import pandas as pd
from function import *


node1=input(" First node value : ")
node2=input(" Second node value : ")
relation=input(" Relation's name : ")
print("pour chaque approche répondez par : \n'1' pour 'oui' \n'0' pour non  ")
deduction=int(input(" Déduction :  "))
induction=int(input(" Induction : "))
transitivite=int(input(" Transitivité : "))
abduction=int(input(" Abduction : "))


relations=getCode(str(node1))
listNodes, listRelations =parseCSV(relations,'relations.csv')

idNode1=getIdNodeRelation(node1,listNodes)
idNode2=getIdNodeRelation(node2,listNodes)
idRelation=getIdNodeRelation(relation,listRelations)

df=pd.read_csv("relations.csv",sep=';')
listNode2Relation = []
if idNode1!=None and idRelation!=None and idNode2!=None:
  if deduction:
    listNode2Relation=inference(idNode1,idNode2,idRelation,df,listNodes,getRelationsSortante,2,4)
    if (len(listNode2Relation) > 0):
      listNode2Relation.sort(key=sortFunction, reverse=True)
      print("******************"+node1 + " " + relation + " " + node2 + " car par déduction on a (du meilleur au pire)====> **********************")
      for l in listNode2Relation:
        print(
          node1 + " " + str(getNameNode(6, listRelations)) + " " + str(getNameNode(l['node1'], listNodes)) + "  et   " +
          str(getNameNode(l['node1'], listNodes)) + " " + str(
            getNameNode(l['relation'], listRelations)) + " " + node2 + ". Score:" + str(l['w']))
        print("===================")
    else:
      print("*******Par déduction, il n'est pas vrai que : "+node1+" "+relation+" "+node2+"*********")
      print("===========================================================================")

  if induction:
    listNode2Relation=inference(idNode1,idNode2,idRelation,df,listNodes,getRelationsEntrante,1,4)

    if(len(listNode2Relation)>0):
      listNode2Relation.sort(key=sortFunction, reverse=True)
      print("**********************"+node1 + " " + relation + " " + node2 + " car par induction on a (du meilleur au pire)====> ***********************")
      for l in listNode2Relation:
        print(str(getNameNode(l['node1'],listNodes))+" "+str(getNameNode(6,listRelations))+" "+node1+"  et   "+
              str(getNameNode(l['node1'],listNodes))+" "+str(getNameNode(l['relation'],listRelations))+" "+node2+ ". Score:" + str(l['w']))
        print("===================")
    else:
      print("*******Par induction, il n'est pas vrai que : "+node1+" "+relation+" "+node2+"*********")
      print("====================================")

  if transitivite:
    # Récupérer tout les relations de type node1  relation  node
    relationIsa = getRelationsSortante(idNode1, idRelation, df)

    # Récupérer tout les noeud node tel que node1 relation node
    node1IsaNode2 = []
    for r in relationIsa:
      nodePoid=[]
      nodePoid.append(getNameNode(r[2], listNodes))
      nodePoid.append(r[4])
      node1IsaNode2.append(nodePoid)

    listNode2Relation = []
    for node in node1IsaNode2:
      n = getIdNodeRelation(node[0], listNodes)
      code = getCode(node[0])
      if n != None and code != None:
        listNodes1, listRelations1 = parseCSV(code, 'temporaryFile.csv')
        dfTemporary = pd.read_csv("temporaryFile.csv", sep=';')
        os.remove("temporaryFile.csv")

        nodeListSortante = getRelation(n, idNode2, idRelation, dfTemporary)
        if len(nodeListSortante) > 0:
          nodeListSortante[0]['w'] = sqrt(node[1] *nodeListSortante[0]['w'])
          listNode2Relation.append(nodeListSortante[0])

    if (len(listNode2Relation) > 0):
      listNode2Relation.sort(key=sortFunction, reverse=True)
      print("*********************"+node1 + " " + relation + " " + node2 + " car par transitivité on a (du meilleur au pire)====>"+"*********************")
      for l in listNode2Relation:
        print(node1 + " " + str(getNameNode(idRelation, listRelations)) + " " + str(
          getNameNode(l['node1'], listNodes)) + "  et   " +
              str(getNameNode(l['node1'], listNodes)) + " " + str(
          getNameNode(l['relation'], listRelations)) + " " +node2+ ". Score:" + str(l['w']))
        print("===================")
    else:
      print("*******Par transivité, il n'est pas vrai que : "+node1+" "+relation+" "+node2+"*********")
      print("====================================================================")

  if abduction:
    relations1 = getCode(str(node1))
    listNodes1, listRelations1 = parseCSV(relations1, 'relations1.csv')

    relations1 = getCode(str(node2))
    listNodes2, listRelations2 = parseCSV(relations1, 'relations2.csv')

    idNode1 = getIdNodeRelation(node1, listNodes1)
    idNode2 = getIdNodeRelation(node2, listNodes1)

    df1 = pd.read_csv("relations1.csv", sep=';')
    df2 = pd.read_csv("relations2.csv", sep=';')
    # Récupérer tout les relations de type node1  relation  node
    relationNode1 = getAllRelationsSortante(idNode1, df1)
    relationNode2 = getAllRelationsSortante(idNode2, df2)
    listResultats=[]
    for r1 in relationNode1:
      for r2 in relationNode2:
        relation=[]
        if r1['relation']==r2['relation'] and r1['node2']==r2['node2']:
          relation.append(r1)
          relation.append(r2)
        if len(relation)>0:
          listResultats.append(relation)

    listResultats.sort(key=lambda x: (x[0]['w'] + x[1]['w']), reverse=True)
    if (len(listResultats) > 0):
      #listNode2Relation.sort(key=sortFunction, reverse=True)
      print("*****************"+node1 + " " + "r_isa" + " " + node2 + " car par abduction on a (du meilleur au pire)====> **********************")
      for l in listResultats:
        print(node1 + " " + str(getNameNode(l[0]['relation'], listRelations1)) + " " + str(
          getNameNode(l[0]['node2'], listNodes1)) + "  et   " +
              node2 + " " + str(
          getNameNode(l[0]['relation'], listRelations2)) + " " + str(getNameNode(l[0]['node2'], listNodes2)) + ". Score:" + str(l[0]['w']+l[1]['w']))
        print("===================")
    else:
      print("*********Pas d'inférence de type abduction************")
      print("============================================")
else : 
  print(" La relation "+node1+" "+relation+" "+node2+" n'existe pas")
  


