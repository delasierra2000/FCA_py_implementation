import pandas as pd

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



def obtain_concepts(df):

    A=df.columns.tolist()
    B=df.index.tolist()

    list_ext=[(a,extension(df,[a])) for a in A]

    list_ext_sorted=sorted(list_ext,key=lambda x: len(x[1]),reverse=True)


    sol=[]

    #First Row (B)

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

    sol.append((a,B))

    #If there is some attributes whose extension is B, we wont to drop them from the list.
    if temp_list:
        if len(a)==len(A):
            list_ext_sorted=[]
        else:
            list_ext_sorted=list_ext_sorted[len(a):]

    print(list_ext_sorted)

    while list_ext_sorted:

        element=list_ext_sorted[0]
        element_objects=element[1]

        control=True
        i=0
        while control:
            if equal_list(sol[i][1],element_objects):

                sol[i]=(sol[i][0]+[element[0]],sol[i][1])


                control=False

            i=i+1

            if i==len(sol) and control:
                control=False
                sol.append(([element[0]],element_objects))

                list_intersections=[]
                current_objects=[]
                for j in range(0,len(sol)):

                    current_objects.append(sol[j][1])
                    list_intersections.append(intersection(element_objects,sol[j][1]))
                    
                    list_intersections_filtered=[]

                    for w in range(0,len(list_intersections)):
                        inter=list_intersections[w]
                        control=True
                        for z in range(0,len(current_objects)):
                            if equal_list(inter,current_objects(z)):
                                control=False
                        if control:
                            list_intersections_filtered.append(inter)
                for i in range(0,list_intersections_filtered):
                    sol.append(([],list_intersections_filtered[i]))
                        



        list_ext_sorted.pop(0)







    

    return sol


def equal_list(list1,list2):
    return set(list1)==set(list2)

def intersection(list1,list2):
    return list(set(list1) & set(list2))

def union(list1,list2):
    return list(set(list1) | set(list2))



df=obtain_matrix('./Tables/test1.txt',['Carpa','Escatofagus','Sargo','Dorada','Anguila'])


print(obtain_concepts(df))


