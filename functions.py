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

    

    
    #[mu(x) for x in list_atribs if set(extension[x]) != [set(extension[a]) for a in list_atribs if  ]]

    return list_ext_sorted



df=obtain_matrix('./Tables/peces.txt',['Carpa','Escatofagus','Sargo','Dorada','Anguila'])


print(obtain_concepts(df))


