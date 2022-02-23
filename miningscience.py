from Bio import Entrez, SeqIO 
import pandas as pd
import re,csv,itertools
import numpy as np
#IMPORTACION DEl miningscience
import miningscience as msc

def download_pubmed(keyword):

    Entrez.email = 'alexandra.sarmiento@est.ikiam.edu.ec'  #se puede usar cualquier correo 
    results = Entrez.read(Entrez.esearch(db='pubmed',retmax=190 ,retmode='xml',term=keyword))
    return results

def mining_pubs(tipo):
    list1= []
    list2 = []
    var_contador = 0
    
    results = download_pubmed('Ecuador genomics[Title/Abstract]')
    ids_docs = ','.join(results['IdList'])     
    Entrez.email = 'alexandra.sarmiento@est.ikiam.edu.ec'    
    handle = Entrez.efetch(db='pubmed',rettype='medline',retmode='text',id=ids_docs)
    docs_id = handle.read()   
    
    if(tipo == "AU"):
        columna1 = re.findall(r'PMID-.(.+)|AU  - (.+[A-Z-a-z])', docs_id)
        columna2 = re.findall(r'DP  -.(.+[A-Z-a-z-0-9])', docs_id)
        nombre_dataset = ['Pmid','NrAutor'] 
        contenedor1 = list()        
        for x in columna1:
            contenedor1.append((x[0],''))  if x[0]!='' else contenedor1.append(('',x[1]))
        for vam in contenedor1:
            if(vam[0] !=''):
                list1.append(vam[0])                 
                if(var_contador != 0):
                    list2.append(var_contador)
                    var_contador = 0
                else:
                    None
            else:
                var_contador += 1                 
        dataset = list(zip(list1,list2))        
    elif(tipo == "AD"):
        columna1 = re.findall(r'PL  -.(.+[A-Z-a-z-0-9])|(AU)  -|', docs_id)
        columna2 = re.findall(r'DP  -.(.+[A-Z-a-z-0-9])', docs_id)
        nombre_dataset = ['Country','NrAutor'] 
        contenedor1 = list()        
        for primer in columna1:
            #Generado de lista para los articulos encontrados 
            if(primer[0]!=''):
                contenedor1.append((primer[0],''))
            elif(primer[1]!=''):
                contenedor1.append(('',primer[1]))
            else:
                None                
        for vam in contenedor1:
            if(vam[0] !=''):
                list1.append(vam[0])                 
                if(var_contador != 0):
                    list2.append(var_contador)
                    var_contador = 0
                else:
                    None
            else:
                var_contador += 1
        else:
            None
        dataset = list(zip(list1,list2))       
    elif(tipo == "DP"):
        columna1 = re.findall(r'PMID-.(.+\d[A-Z-a-z-0-9])', docs_id)
        columna2 = re.findall(r'DP  -.(.+[A-Z-a-z-0-9])', docs_id)
        nombre_dataset = ['Pmid','DpYear']        
        dataset = list(zip(columna1,columna2))
    results = pd.DataFrame(dataset,columns = nombre_dataset)             
    return results