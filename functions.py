import pandas as pd
from tabulate import tabulate

###-----------------------------------
### Import txt into pandas dataframe
###-----------------------------------

def obtain_matrix(path,list="default"):

    read_file = pd.read_csv (path, delimiter = '\t')
    read_file.to_csv ('./Tables/CSV/temporal.csv', index=False, sep = ';')

    df = pd.read_csv ('./Tables/CSV/temporal.csv', sep = ';') 
    df = df.drop(df.columns[df.shape[1]-1], axis=1)


    if list=="default":

        objects =[]
        for i in range(0,df.shape[0]):
            objects.append('Obj '+ str(i+1))
    elif len(list)!=df.shape[0]:
        print("Not enough objects in the input list")
    else:
        objects=list


    #Insertamos el nombre de los objetos por cada fila
    df.index=objects

    #Volvemos a convertir el dataframe en archivo .csv
    df.to_csv('./Tables/CSV/CleanContext.csv', index=False, sep=';')

    return df


#### NOTA: ESTAS FUNCIONES SIRVEN CON EL DATAFRAME CUYOS ÍNDICES SON LOS NOMBRES DE LOS OBJETOS.


#Función auxiliar que al introducir una lista, devuelve 1 si solo esta compuesta por 1. En otro caso devuelve 0.
def list_to_01(list):

    if set(list)=={1}:
        sol=1
    else:
        sol=0

    return sol


###-----------------------------------
### Extension and intension
###-----------------------------------


#Función que calcula la derivación de un subconjunto de atributos.
def extension(df,atrib_list):

    #Obtiene la lista de todos los objetos
    list_objs=df.index.tolist()

    #Obtiene una lista formadas por las filas de 0 y 1.
    values=df[atrib_list].values.tolist()

    #Transfa en 1 las listas compuestas únicamente por 1, y en 0 el resto.
    list_01=[list_to_01(x) for x in values]

    #Calcula los índices de los 1 de la lista anterior, que se corresponderan con el índice de la lista de objetos.
    indexes=[]

    for i in range(0,len(list_01)):
        if list_01[i]==1:
            indexes.append(i)

    #Extrae de la lista de objetos aquellos que tengan algún índice de la lista indexes.
    sol=[list_objs[i] for i in indexes]

    if not atrib_list:
        sol=list_objs

    return sol

#Función que calcula la derivación de un subconjunto de objetos.
def intension(df,objs_list):

    #Traspone y usa la función de extensión, ya que es equivalente.
    df2=df.T
    sol=extension(df2,objs_list)

    return sol

###-----------------------------------
### Gamma and Mu functions
###-----------------------------------


def gamma(df,b):

    sol=(extension(df,(intension(df,[b]))),intension(df,[b]))

    return sol

def mu(df,a):

    sol=(extension(df,[a]),intension(df,(extension(df,[a]))))

    return sol

def Inf_irreductible_set(df):

    list_atribs=df.columns.tolist
    #[mu(x) for x in list_atribs if set(extension[x]) != [set(extension[a]) for a in list_atribs if  ]]

    return




###-----------------------------------
### ALGORITHM AND RELATED FUNCTIONS 
###-----------------------------------

def algorithm(df):

    A=df.columns.tolist()
    B=df.index.tolist()

    list_ext=[[a,extension(df,[a])] for a in A]

    list_ext_sorted=sorted(list_ext,key=lambda x: len(x[1]),reverse=True)


    sol=[]


    # FIRST ROW (B)

    #Optimized search of an atribute whose extension is equal to B 
    #(it looks into the list sorted, if an extension of an attribute is not B, it does not look further)

    control=True
    i=0
    temp_list=[]

    while control and i<len(list_ext_sorted):
        pair=list_ext_sorted[i]
        if pair[1]==B:
            temp_list.append(pair[0])
        else:
            control=False
        i=i+1
        
        a=temp_list

    sol.append([a,B,None])


    # NEXT ROWS

    #If there is some attributes whose extension is B, we want to drop them from the list.
    if temp_list:
        if len(a)==len(A):
            list_ext_sorted=[]
        else:
            list_ext_sorted=list_ext_sorted[len(a):]

    #We take the attribute and its extension from the sorted filtered list one by one. 
    for i in range(0,len(list_ext_sorted)):

        element=list_ext_sorted[i]

        attribute=element[0]
        att_extension=element[1]

        #Check if att_extension is equal to a subset of objects that's already in the table.
        check_not_equal=True
        for j in range(0,len(sol)):
            if equal_list(att_extension,sol[j][1]):
                sol[j][0]=sol[j][0]+[attribute]
                check_not_equal=False

        #If it was not equal to any subset of objects, add the pair to the table
        #and add all the new intersections.

        if check_not_equal:
            
            index_att=len(sol)
            sol.append([[attribute],att_extension,None])

            objects_in_table=[sorted(x[1]) for x in sol]
            all_intersections=[[intersection(att_extension,x),[index_att,objects_in_table.index(x)]] for x in objects_in_table]

            new_intersections=list_no_repeat_1([x for x in all_intersections if sorted(x[0]) not in objects_in_table])

            if new_intersections:
                for n in range(0,len(new_intersections)):
                    sol.append([[],new_intersections[n][0],new_intersections[n][1]])

    return sol



#Shows the result of the algorithm.
def show_algorithm(df):

    pd.set_option("display.max_columns", None)

    list=algorithm(df)

    rows=[tuple(x) for x in list]

    table=pd.DataFrame(rows,columns=['ATTRIBUTES','OBJECTS','INTERSECTIONS'])

    print(tabulate(table, headers='keys',tablefmt='grid',stralign='center',numalign='center'))


    return


###-----------------------------------
### OBTAIN FULL CONCEPTS
###-----------------------------------

# Funtion to obtain all concepts

def construct_concepts(df):

    # Aplies the algorithm
    list_alg=algorithm(df)

    sol= [[x[1],intension(df,x[1]),x[2]] for x in list_alg]

    return sol

def show_concepts(df):

    pd.set_option("display.max_columns", None)

    list=construct_concepts(df)

    rows=[tuple(x[0:2]) for x in list]

    table=pd.DataFrame(rows,columns=['OBJECTS','ATTRIBUTES'])

    print(tabulate(table, headers='keys',tablefmt='grid',stralign='center',numalign='center'))

    return




###-----------------------------------
### ATTRIBUTE CLASIFICATION
###-----------------------------------

def clasify_att(df):

    # Algorithm to obtain concepts
    concepts=algorithm(df)

    # Filtration of rows which first element (Atts) is not void.
    concepts_filtered=[x for x in concepts if x[0]]

    # Check if a concept is obtained by intersections
    att_I=[x[0] for x in concepts_filtered if x[2]!=None]
    I=list_no_repeat(sum(att_I,[]))

    # Check if a concept is not obtained by intersections and the list of attributes has only 1 element.
    att_K=[x[0] for x in concepts_filtered if x[2]==None and len(x[0])==1]
    K=list_no_repeat(sum(att_K,[]))

    # Check if a concept is not obtained by intersections and the list of attributes has more than 1 element.
    att_C=[x[0] for x in concepts_filtered if x[2]==None and len(x[0])!=1]
    C=list_no_repeat(sum(att_C,[]))

    return [K,C,I]

def show_att_clasification(df):

    list=clasify_att(df)

    data={'Absolutely Necessary': [list[0]],
          'Relatively Necessary': [list[1]],
          'Unnecessary': [list[2]]}

    pd.set_option("display.max_columns", None)
    
    table=pd.DataFrame(data)
    table.index=['ATTRIBUTES']

    print(tabulate(table, headers='keys',tablefmt='grid',stralign='center',numalign='center'))

    return


###-----------------------------------
### MEET IRREDUCIBLE
###-----------------------------------

def meet_irreducible(df):

    list_objs=df.index.tolist()
    concepts=construct_concepts(df)
    M_f=[x[0:2] for x in concepts if x[2]==None and not equal_list(x[0],list_objs)]

    return M_f

def show_Mf(df):

    list=meet_irreducible(df)

    rows=[tuple(x) for x in list]

    table=pd.DataFrame(rows,columns=['OBJECTS','ATTRIBUTES'])

    print(tabulate(table, headers='keys',tablefmt='grid',stralign='center',numalign='center'))

    return

###-------------------------------------------
### OBJECT CLASIFICATION AND JOIN IRREDUCIBLE
###-------------------------------------------

def clasify_obj(df):

    sol=clasify_att(df.T)

    return sol

def show_obj_clasification(df):

    list=clasify_obj(df)

    data={'Absolutely Necessary': [list[0]],
          'Relatively Necessary': [list[1]],
          'Unnecessary': [list[2]]}

    pd.set_option("display.max_columns", None)
    
    table=pd.DataFrame(data)
    table.index=['OBJECTS']

    print(tabulate(table, headers='keys',tablefmt='grid',stralign='center',numalign='center'))

    return

def join_irreducible(df):

    sol=meet_irreducible(df.T)

    return sol

def show_Jf(df):

    list=join_irreducible(df)

    rows=[tuple(x) for x in list]

    table=pd.DataFrame(rows,columns=['ATTRIBUTES','OBJECTS'])

    table=table[['OBJECTS','ATTRIBUTES']]


    print(tabulate(table, headers='keys',tablefmt='grid',stralign='center',numalign='center'))

    return

###-----------------------------------
### Implications
###-----------------------------------

def satisfies(T,C,D):
    sol=False
    if not equal_list(intersection(C,T),C):
        sol=True
    if equal_list(intersection(D,T),D):
        sol=True
    return sol

def set_satisfies(list_T,C,D):
    
    sol=True
    for i in range(0,len(list_T)):
        if not satisfies(list_T[i],C,D):
            sol=False
    return sol

def valid(df,C,D):

    C2=intension(df,extension(df,C))
    sol=False
    if equal_list(intersection(D,C2),D):
        sol=True

    return sol























###-----------------------------------
### List operations
###-----------------------------------

def equal_list(list1,list2):
    return set(list1)==set(list2)

def intersection(list1,list2):
    return list(set(list1) & set(list2))

def union(list1,list2):
    return list(set(list1) | set(list2))

def minus(list1,list2):
    return list(set(list1) - set(list2))

def list_no_repeat(list):
    sol=[]
    [sol.append(x) for x in list if x not in sol]
    return sol

def list_no_repeat_1(list):

    sol=[]
    checked=[]
    for i in range(0,len(list)):
        rep=list[i][0]
        if rep not in checked:
            checked.append(rep)
            sol.append(list[i])


    return sol




