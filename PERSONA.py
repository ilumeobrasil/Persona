
# coding: utf-8

# <h1 style='color:#ef9709'>PERSONAS - SÉRIE HISTÓRICA</h1>

# <h4 style='color:blue'>Última atualização: 13/09/2018</h4>

# <h2>1. Preparação</h2>

# Primeiro é necessário importar as bibliotecas:

# In[1]:


import numpy as np
import pandas as pd


# Cria-se as variáveis para no futuro criar os "txt" finais, que serão importados no SQL Server:

# In[3]:


# Mudar para 1 quando for gerar as bases

OPT_GERAR_VW_BASE = 0
OPT_GERAR_VW_BASE_METRICAS = 1
OPT_GERAR_VW_COMP = 0


# Cria-se uma variável que será usada para o caminho da pasta raíz do projeto; um atalho para buscar os próximos arquivos:

# In[4]:


# Se houver acentuação incorrerá em erro
PATH_R = r'C:\Users\Kevin Nakasaki\Documents\KEVIN\DT_PROJETOS\PERSONA - SERIE HISTORICA\Importacao\SERIE'
PATH_W = r'C:\Users\Kevin Nakasaki\Documents\KEVIN\DT_PROJETOS\PERSONA - SERIE HISTORICA\Importacao'
PATH_FL = r'C:\Users\Kevin Nakasaki\Documents\KEVIN\DT_PROJETOS\PERSONA - SERIE HISTORICA\Importacao\22'


# ---

# <h2>2. Início de tratamento da BASE</h2>

# Lê o "txt" SERIE_HISTORICA_v2 e o aloca na variável "df":

# In[5]:


# Se houver acentuação incorrerá em erro
df = pd.read_csv(PATH_R + '\SERIE_HISTORICA_v2.txt', sep='\t', encoding= 'ISO-8859-1')


# ---

# <h2 style='color:red'>3. Append do último flight</h2>

# Junta o último flight à série histórica:

# <h4 style='color:blue'>Data: 13/09/2018 - Flight 22</h4>

# In[6]:


fl = pd.read_csv(PATH_FL + '\BASE_FL22.txt', sep='\t', encoding= 'ISO-8859-1')


# In[7]:


#<h3 style='color:black'>3.1. JOIN BASE E NUVEM</h3>


# In[8]:


#df_nuv = pd.read_csv(PATH_FL + '\AUX_NUVEM_FL22.txt', sep='\t', encoding= 'ISO-8859-1')
#df_nuv['CELEBRIDADE'] = df_nuv['Celeb']

# Exceção para excluir a coluna 'ID' do DataFrame auxiliar da nuvem, isto porque o 'ID' deste DF é o 'ID' de inquiridos
# e não o mesmo 'ID' utilizado na base da 'série histórica'
#try:
#    df_nuv = df_nuv[pd.Series(['Nuvem', 'CELEBRIDADE', 'IP'])]
#    del df_nuv['ID', 'Celeb', 'IP']
#except:
#    pass


# In[9]:


#df_nuv = df_nuv.reset_index(drop=True).set_index(['IP', 'CELEBRIDADE'])
#fl = fl.reset_index(drop=True).set_index(['IP', 'CELEBRIDADE'])

#fl = fl.join(df_nuv, on=['IP', 'CELEBRIDADE'], how='inner')


# In[10]:


# Exceção para inserir a coluna 'ID' no dataframe para fazer o join com a base da 'série histórica'.
# Além disso, iguala a coluna 'OPINIAO' com 'Nuvem' e depois exclui a coluna 'Nuvem'

try:
    fl.insert(0, 'ID', range(0, len(fl)))
#    fl['OPINIAO'] = fl['Nuvem']
#    fl = fl[pd.Series(['ID', 'FLIGHT', 'ESTADO', 'IDADE', 'ESTADO_CIVIL', 'TEM_FILHOS', 'RENDA',
#       'ESCOLARIDADE', 'SEXO', 'AWARENESS', 'NOME', 'OPINIAO',
#       'LEMBRANCA_DE_MARCA', 'GOSTO_MUITO', 'ME_IDENTIFICO', 'TENHO_RESPEITO',
#       'PRESTO_ATENCAO', 'CONFIO', 'MUITO_BOM_NAQUILO_QUE_FAZ', 'INTELIGENTE',
#       'DETERMINADO', 'HONESTO', 'ENGRAÇADO', 'LINDO', 'SEDUTOR', 'DO_POVO',
#       'CARA_DO_BRASIL', 'INOVADOR', 'GOSTA_DE_DESAFIOS',
#       'TENHO_VISTO_NA_MIDIA', 'BOA_PARA_PROPAGANDA',
#       'COMPRARIA_PRODUTOS_QUE_ANUNCIASSE',
#       'BOA_PARA_PROPAGANDA_PROJETOS_SOCIAIS',
#       'ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE',
#       'INDICARIA_PARA_AMIGOS_MARCAS',
#       'COMENTARIA_COM_AMIGOS_PROJETOS_SOCIAIS_QUE_ANUNCIASSE'])]
#
#    del fl['Nuvem']
except:
    pass

fl = fl.reset_index(drop=True)

# Verifica se a substituição em 'OPINIAO' funcionou corretamente.
#with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
#    print(fl[fl['OPINIAO'].notna()].head())


# In[11]:


#fl.rename(columns={'level_0': 'IP', 'level_1': 'CELEBRIDADE'}, inplace=True)
fl.columns


# In[12]:


# Verifica a quantidade de colunas do dataframe
len(fl.columns)


# <h3 style='color:red'>Merge das tabelas auxiliares tratadas no DF de Base</h3>

# In[13]:


df_nuvem_hist = pd.read_csv(PATH_R + '\AUXNUVEM_1.txt', sep='\t', encoding= 'ISO-8859-1')
df_marcas_hist = pd.read_csv(PATH_R + '\AUXMARCAS_1.txt', sep='\t', encoding= 'ISO-8859-1')


# In[14]:


df = df.merge(df_nuvem_hist, how='left', on='ID')
df = df.merge(df_marcas_hist, how='left', on='ID')


# In[15]:


df['OPINIAO'] = df['PALAVRAS']
df['LEMBRANCA_DE_MARCA'] = df['LEMB_MARCAS']


# <h3 style='color:black'>3.2. APPEND</h3>

# O bloco de código abaixo junta a base da "série histórica" atual, com o último flight citado:

# In[16]:


df = df.append(fl, ignore_index=True, sort=False)
df["ID"] = (df.index)+1


# ---

# <h2 style='color:black'>4. Manipulação do DF de base e criação de funções</h2>

# Exceção para verificar se existem todas as colunas no DataFrame e deletar a coluna 'IP'.
# Se retornar um erro, o bloco de código passa sem executar nada:

# In[17]:


try:
    df = df[pd.Series(['CELEBRIDADE', 'ID', 'FLIGHT', 'ESTADO', 'IDADE', 'ESTADO_CIVIL',
       'TEM_FILHOS', 'RENDA', 'ESCOLARIDADE', 'SEXO', 'AWARENESS', 'NOME',
       'OPINIAO', 'LEMBRANCA_DE_MARCA', 'GOSTO_MUITO', 'ME_IDENTIFICO',
       'TENHO_RESPEITO', 'PRESTO_ATENCAO', 'CONFIO',
       'MUITO_BOM_NAQUILO_QUE_FAZ', 'INTELIGENTE', 'DETERMINADO', 'HONESTO',
       'ENGRAÇADO', 'LINDO', 'SEDUTOR', 'DO_POVO', 'CARA_DO_BRASIL',
       'INOVADOR', 'GOSTA_DE_DESAFIOS', 'TENHO_VISTO_NA_MIDIA',
       'BOA_PARA_PROPAGANDA', 'COMPRARIA_PRODUTOS_QUE_ANUNCIASSE',
       'BOA_PARA_PROPAGANDA_PROJETOS_SOCIAIS',
       'ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE',
       'INDICARIA_PARA_AMIGOS_MARCAS',
       'COMENTARIA_COM_AMIGOS_PROJETOS_SOCIAIS_QUE_ANUNCIASSE'])]

    del df['IP', 'PALAVRAS', 'LEMB_MARCAS']
except:
    pass


# Cria um item no DataFrame 'df' chamado 'IX' e o configura para ser igual ao 'ID'. Em seguida o configura para ser o índice do dicionário:

# In[18]:


df["IX"] = df["ID"]
df = df.set_index("IX")


# Define a função 'loadDF' que têm três argumentos:
# - file = nome do arquivo
# - enc = tipo de codificação (por padrão é 'utf-8')
# - sep = tipo do separador dos valores no arquivo (por padrão é ',')
# 
# A função lê o arquivo (precisa ser "txt") e o aloca na variável em que for chamado:

# In[19]:


def loadDF(file, enc="UTF-8", sep=','): return pd.read_csv(PATH_R + r'\{0}.txt'.format(file), encoding=enc, sep=sep)

#def loadDF(file): return pd.read_csv(r'/Users/damorim/Documents/Notebooks/{0}.txt'.format(file), encoding="UTF-8", sep=",")


# Define a função 'writeDF' que têm quatro argumentos:
# - dfr = nome do DataFrame ('df' alguma coisa) que é definido nesse script
# - file = nome do arquivo "txt" em que o DataFrame vai ser escrito
# - enc = tipo de codificação (por padrão é 'utf-8')
# - sep = tipo do separador dos valores no arquivo (por padrão é ',')
# 
# A função escreve o DataFrame criado no python em um arquivo "txt":

# In[20]:


def writeDF(dfr, file, enc="UTF-8", sep=','): return dfr.to_csv(PATH_W + r'\{0}.txt'.format(file), header=True, encoding=enc, sep=",", float_format="%.3f")


# ---

# <h2 style='color:black'>5. Tratamento de METADADOS</h2>

# In[21]:


meta = loadDF("METADADOS", enc="UTF-8")
meta["COLUNA2"] = meta["COLUNA"]
meta = meta.set_index("COLUNA2")


# ---

# <h2 style='color:black'>6. Tratamento de FOTOS</h2>

# Define o DataFrame 'df_fotos' utilizando a função 'loadDF' e já configura a coluna 'CELEBRIDADE' como índice:

# In[22]:


df_fotos = loadDF('\FOTOS', enc= 'ISO-8859-1', sep='\t').set_index('CELEBRIDADE')
df_fotos


# ---

# <h2 style='color:black'>7. Tratamento de CATEGORIAS</h2>

# Define o DataFrame 'df_categorias' utilizando a função 'loadDF':

# In[23]:


df_categorias = loadDF('\CATEGORIAS', enc= 'ISO-8859-1', sep='\t')


# ---

# <h2 style='color:black'>8. Arquivo para conferir se todas as CELEBRIDADES estão CATEGORIZADAS</h2>

# In[24]:


VERIF_CATEG = 1
df4 = df.reset_index().set_index('CELEBRIDADE')
df5 = df_categorias.reset_index().set_index('CELEBRIDADE').join(df4)
df6 = df5[ df5['CATEGORIA'].isna()]

print(df6)


# ---

# Atualiza o DataFrame 'df_categorias' resetando o índice do DataFrame. **Por não ter o argumento *drop=True*, o índice antigo se transforma numa nova coluna no DataFrame**.
# 
# Em seguida cria um DataFrame no qual o índice é a coluna 'CELEBRIDADE' e a coluna do DataFrame é a 'CATEGORIA', agrupando tudo através da função *lambda* definida, ao invés do padrão que é *numpy.mean* (**verificar com o Danilo para quê isso foi feito**):

# In[25]:


df_categorias = df_categorias      .reset_index()     .pivot_table(index='CELEBRIDADE' ,columns=['CATEGORIA'], aggfunc=lambda x : x)


# ---

# <h2 style='color:black'>9. Join entre a BASE e FOTOS</h2>

# O código abaixo executa os seguintes passos:
# 1. Reseta o índice do DataFrame 'df' (que puxou o arquivo 'SERIE_HISTORICA_v2')
# 2. Configura como novo índice a coluna 'CELEBRIDADE'
# 3. Junta o 'df' com 'df_fotos' utilizando os seus índices (de ambos são a coluna 'CELEBRIDADE')
# 4. Reseta o índice de 'df' novamente (já que já foi utilizado para o *join*)
# 5. Configura novamente o índice para a coluna 'IX'

# In[26]:


df = df.reset_index().set_index('CELEBRIDADE').join(df_fotos).reset_index().set_index('IX')


# A função *option_context()* é utilizada para permitir que todas as colunas sejam mostradas no *print()*, para conferir se o *join* foi realizado corretamente.
# 
# A função *head()* retorna, por padrão, as primeiras 5 linhas do DataFrame para verificar os tipos de dados que o DataFrame contém.

# In[27]:


# Verificação de print() sem o option_context()
print(df.head())


# In[28]:


with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
    print(df.head())


# ---

# In[29]:


#<h2 style='color:black'>10. Arquivo para conferir se todas as CELEBRIDADES têm FOTOS</h2>
#
#VERIF_FOTOS = 1
#df3 = df[ df["FOTO_P"].isna() ]
#print(df3["CELEBRIDADE"].unique(), "Coluna FOTO_P")
#df3 = df[ df["FOTO_M"].isna() ]
#print(df3["CELEBRIDADE"].unique(), "Coluna FOTO_M")
#df3 = df[ df["FOTO_G"].isna() ]
#print(df3["CELEBRIDADE"].unique(), "Coluna FOTO_G")
#
#if VERIF_FOTOS == 1:
#    writeDF(df3, 'VERIF_FOTOS')
#    print("Arquivo exportado")


# ---

# <h2 style='color:black'>11. Conferência de possíveis problemas na BASE</h2>

# In[ ]:


# with pd.option_context('display.max_rows', None, 'display.max_columns', 10):
    # print(pd.Series(df["CELEBRIDADE"].unique()))
    # print(pd.Series(df["FLIGHT"].unique()))
    # print(pd.Series(df["ESTADO"].unique()))
    # print(pd.Series(sorted(df["IDADE"].unique())))
    # print(pd.Series(sorted(df["ESTADO_CIVIL"].unique())))
    # print(pd.Series(sorted(df["TEM_FILHOS"].unique())))
    # print(pd.Series(sorted(df["RENDA"].unique())))
    # print(pd.Series(sorted(df["ESCOLARIDADE"].unique())))
    # print(pd.Series(sorted(df["SEXO"].unique())))
    # print(pd.Series(sorted(df["AWARENESS"].unique())))


# Cria a *Series* 'df2' como sendo o resultado do *subset* (no SQL = SELECT) de todos os Estados com valores maiores que 27.
# 
# Em seguida printa o *subset* do *Series* 'df2' puxando todos os valores distintos na coluna 'FLIGHT' (no SQL = SELECT DISTINCT FLIGHT FROM df2):

# In[ ]:


# FLIGHT 18 TÁ CAGADO, fizeram alguma bosta na coluna de Estado. Tem que esperar o Gui arrumar
df2 = df[ df["ESTADO"] > 27 ]
print(df2["FLIGHT"].unique())


# A função *isnull()* (também conhecida como *isna()*) retorna 'True' para cada valor nulo na coluna. Foi utilizado para buscar por valores nulos no DataFrame (aparentemente esperava-se que tudo estivesse preenchido).

# In[ ]:


# FLIGHT 9 TÁ CAGADO, fizeram alguma bosta nas colunas de perfil demográfico, pois estão vazias
df2 =  df [ pd.isnull(df["IDADE"]) ]
print(df2["FLIGHT"].unique())
df2 =  df [ pd.isnull(df["ESTADO_CIVIL"]) ]
print(df2["FLIGHT"].unique())
df2 =  df [ pd.isnull(df["TEM_FILHOS"]) ]
print(df2["FLIGHT"].unique())
df2 =  df [ pd.isnull(df["RENDA"]) ]
print(df2["FLIGHT"].unique())
df2 =  df [ pd.isnull(df["ESCOLARIDADE"]) ]
print(df2["FLIGHT"].unique())
df2 =  df [ pd.isnull(df["SEXO"]) ]
print(df2["FLIGHT"].unique())


# Faz a mesma verificação por valores nulos só que dessa vez criando uma cópia do resultado e o associando em 'df2':

# In[ ]:


# FLIGHTS 8, 11, 12 possuem a coluna de 'AWARENESS' vazio
df2 =  df [ pd.isnull(df["AWARENESS"]) ].copy()


# Printa as quantidades de celebridades em 'df2' agrupando pela coluna 'FLIGHT':

# In[ ]:


print(df2.groupby("FLIGHT")["CELEBRIDADE"].count() )


# Cria a variável 'ls_cols' e associa a ela uma lista criada a partir da coluna 'AWARENESS':

# In[ ]:


ls_cols = list(["AWARENESS"])


# Adiciona o conteúdo das listas 'ls_cols' e a lista gerada a partir de 'pd.Series(df.columns)[13:-3]', criando uma única lista em 'ls_cols'.
# 
# O item *.columns* faz com que sejam "puxados" somente os *labels* das colunas que no caso são as escalas:

# In[ ]:


ls_cols.extend(pd.Series(df.columns)[13:-3])


# Cria um DataFrame com a *Series* da lista 'ls_cols':

# In[ ]:


df2 = df [ pd.Series(ls_cols) ]


# Printa um sumário com as principais estatísticas excluindo-se os valores *NaN*:

# In[ ]:


print(df2.describe())


# In[ ]:


# As escalas ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE e INDICARIA_PARA_AMIGOS_MARCAS não foram respondidas no flight 8


# **Legenda de AWARENESS na tabela: 1 - Sei; 2 - Não Sei**
# 
# Busca no DataFrame 'df' quais são as CELEBRIDADES que são conhecidas e que os respondentes preencheram no campo 'GOSTO_MUITO'.

# In[ ]:


df2 = df[ df["AWARENESS"] == 1 &  pd.notnull( df["GOSTO_MUITO"]) ]


# Cria uma *Series* dos *labels* do DataFrame 'df2' para verificar o DataFrame contém todas as colunas necessárias:

# In[ ]:


print(pd.Series(df2.columns))


# Busca por colunas que possuem valores nulos e seus respectivos 'FLIGHTS':

# In[ ]:


print( df2 [ pd.isnull(df2["GOSTO_MUITO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["ME_IDENTIFICO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["TENHO_RESPEITO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["PRESTO_ATENCAO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["CONFIO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["MUITO_BOM_NAQUILO_QUE_FAZ"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["INTELIGENTE"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["DETERMINADO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["HONESTO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["ENGRAÇADO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["LINDO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["SEDUTOR"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["DO_POVO"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["CARA_DO_BRASIL"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["INOVADOR"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["GOSTA_DE_DESAFIOS"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["TENHO_VISTO_NA_MIDIA"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["BOA_PARA_PROPAGANDA"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["COMPRARIA_PRODUTOS_QUE_ANUNCIASSE"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["BOA_PARA_PROPAGANDA_PROJETOS_SOCIAIS"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["INDICARIA_PARA_AMIGOS_MARCAS"]) ]["FLIGHT"].unique() )
print( df2 [ pd.isnull(df2["COMENTARIA_COM_AMIGOS_PROJETOS_SOCIAIS_QUE_ANUNCIASSE"]) ]["FLIGHT"].unique() )

print ("\n\n")


# **Legenda de AWARENESS na tabela: 1 - Sei; 2 - Não Sei**
# 
# Cria uma condição em que é necessário que as colunas sejam nulas e que o 'AWARENESS' seja igual a 1, para printar a quantidade de CELEBRIDADES agrupadas por 'FLIGHT' em que essas condições sejam verdadeiras:

# In[ ]:


df3 = df2[ pd.isnull(df2["ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE"]) & df2["AWARENESS"] == 1  ]
print (df3.groupby('FLIGHT')["CELEBRIDADE"].count())

df3 = df2[ pd.isnull(df2["INDICARIA_PARA_AMIGOS_MARCAS"]) & df2["AWARENESS"] == 1  ]
print (df3.groupby('FLIGHT')["CELEBRIDADE"].count())

print ("\n\n")


# **Verificar com Danilo por que foi feito pelo 'df' e não pelo 'df2' igual aos outros**

# In[ ]:


# FLIGHT 17 possui 1 registro que apesar de ter marcado que conhece o artista, não respondeu nenhuma escala
df2 =  df [ df["AWARENESS"] == 1 & pd.isnull(df["GOSTO_MUITO"]) ]
print(df2.groupby('FLIGHT')['CELEBRIDADE'].count())

print ("\n\n") 

df2 = df[ df["FLIGHT"] == 8 ]
print(df2.groupby("AWARENESS")["CELEBRIDADE"].count() )


# ---

# <h2 style='color:black'>12. Carregamento de 'tabelas auxiliares'</h2>

# In[30]:


df_escolaridade = loadDF('ESCOLARIDADE')
df_estado_civil = loadDF('ESTADOCIVIL')
df_idade = loadDF('IDADE')
df_renda = loadDF('RENDA')
df_uf = loadDF('UF')


# Cria um dicionário para fazer a mesma função que as tabelas auxiliares que são importadas no SQL Server:

# In[31]:


dictAux = {     "ESCOLARIDADE" : df_escolaridade.set_index('COD_ESCOLARIDADE')
              , "ESTADOCIVIL"  : df_estado_civil.set_index('COD_ESTADOCIVIL')
              , "IDADE"        : df_idade.set_index('COD_IDADE')
              , "RENDA"        : df_renda.set_index('COD_RENDA')
              , "UF"           : df_uf.set_index('COD_ESTADO')
          }


# ---

# <h2 style='color:red'>13. Views para o PowerBI</h2>

# <h3 style='color:blue'>13.1. VW_BASE</h3>

# Cria uma cópia do DataFrame 'df' e o nomeia como 'df_base'.
# 
# Em seguida faz os *joins* para buscar as informações do dicionário auxiliar (semelhante a buscar informações das tabelas auxiliares).
# 
# A função *where()* é semelhante à um *if* no excel, em que se determinada condição for satisfeita, executar a primeira opção, caso contrário executar a segunda (*where(condition, True, False)*):

# In[ ]:


df_base = df.copy()

df_base = df_base.set_index('ESCOLARIDADE').join(dictAux["ESCOLARIDADE"])
df_base = df_base.set_index('ESTADO_CIVIL').join(dictAux["ESTADOCIVIL"])
df_base = df_base.set_index('IDADE').join(dictAux["IDADE"])
df_base = df_base.set_index('RENDA').join(dictAux["RENDA"])
df_base = df_base.set_index('ESTADO').join(dictAux["UF"])
df_base["ESCOLARIDADE"] = df["ESCOLARIDADE"]
df_base["ESTADO_CIVIL"] = df["ESTADO_CIVIL"]
df_base["IDADE"] = df["IDADE"]
df_base["RENDA"] = df["RENDA"]
df_base["ESTADO"] = df["ESTADO"]

# Correção realizada: 1 - Masculino ; 2 - Feminino
df_base["SEXO"] = np.where(df["SEXO"] == 1, "Masculino", "Feminino")
df_base["TEM_FILHOS"] = np.where(df["TEM_FILHOS"] == 1, "Sim", "Não")

#with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
    #print( df_base[ pd.isnull(df_base['REGIAO']) ].groupby('FLIGHT')["ID"].count()  )
    #print( sorted(df_base[ df_base["FLIGHT"] == 9 ]["ESTADO"].unique()) ) 

#print(pd.Series(df_base.columns)) 


# Deleta as colunas de 'df_base' que estão com os valores antigos, usados para puxar os valores no *join* e renomeia as colunas que vieram das "tabelas auxiliares" para fazer o papel das colunas deletadas:

# In[ ]:


del df_base["ESTADO"]
del df_base["RENDA"]
del df_base["ESCOLARIDADE"]
del df_base["IDADE"]

df_base.rename( columns ={ 
    "UF_NOME" : "ESTADO" ,
    "RENDA_DESC2": "RENDA",
    "ESCOLARIDADE_DESC2" : "ESCOLARIDADE",
    "ESTADOCIVIL_DESC": "ESTADOCIVIL",
    "IDADE_INT": "IDADE"
}, inplace=True)


# Bloco para gerar o arquivo que será usado na importação no SQL Server.
# 
# Ordena pela coluna 'ID' de forma ascendente e a configura para ser índice (key).
# Em seguida usa a função 'writeDF' para escrever o DataFrame no arquivo "VW_BASE.txt":

# In[ ]:


if OPT_GERAR_VW_BASE == 1:
    df_base = df_base                .sort_values(by=['ID'], ascending=True)                .set_index("ID")

    writeDF(df_base, 'VW_BASE')
        
    print("Arquivo gerado")


# ---

# <h3 style='color:purple'>VW_BASE_METRICAS (passo-a-passo)</h3>

# In[ ]:


#df_awareness = df.copy()
#print(df_awareness.head())


# In[ ]:


#df_awareness['AW'] = np.where( df_awareness['AWARENESS'] == 1, 'S', 'N' )


# In[ ]:


#df_awareness = df_awareness.groupby(['FLIGHT','CELEBRIDADE','AW'], as_index=False).count()
#print(df_awareness.head())


# In[ ]:


#df_awareness = df_awareness[ pd.Series(['CELEBRIDADE','FLIGHT','AW', 'ID']) ].pivot_table('ID',['CELEBRIDADE','FLIGHT'],'AW')
#print(df_awareness.head())


# In[ ]:


#df_awareness['S']


# In[ ]:


#df_awareness["AWARENESS"] = df_awareness['S'] / (df_awareness['S'] + df_awareness['N'])
#print(df_awareness)


# In[ ]:


#df_awareness["AWARENESS_NIVEL"] = np.where( df_awareness['AWARENESS'] >= 0.65, 'Alto', 'Baixo' )
#print(df_awareness)


# In[ ]:


#cols = [
#    'ID',
#    'CELEBRIDADE',
#    'FLIGHT',
#    'GOSTO_MUITO',
#    'ME_IDENTIFICO',
#    'TENHO_RESPEITO',
#    'PRESTO_ATENCAO',
#    'CONFIO',
#    'MUITO_BOM_NAQUILO_QUE_FAZ',
#    'INTELIGENTE',
#    'DETERMINADO',
#    'HONESTO',
#    'ENGRAÇADO',
#    'LINDO',
#    'SEDUTOR',
#    'DO_POVO',
#    'CARA_DO_BRASIL',
#    'INOVADOR',
#    'GOSTA_DE_DESAFIOS',
#    'TENHO_VISTO_NA_MIDIA',
#    'BOA_PARA_PROPAGANDA',
#    'COMPRARIA_PRODUTOS_QUE_ANUNCIASSE',
#    'BOA_PARA_PROPAGANDA_PROJETOS_SOCIAIS',
#    'ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE',
#    'INDICARIA_PARA_AMIGOS_MARCAS',
#    'COMENTARIA_COM_AMIGOS_PROJETOS_SOCIAIS_QUE_ANUNCIASSE',
#]
#
#df_metricas = df.copy()
#print(df_metricas.head())


# In[ ]:


#df_metricas = df_metricas[ pd.Series(cols) ]    \
#    .melt(id_vars=['ID', 'CELEBRIDADE', 'FLIGHT' ],  value_name= 'VALOR', var_name='METRICA')     \
#    .set_index("METRICA")     \
#    .join(meta)


# In[ ]:


#df_metricas["TOP2"] = np.where( df_metricas["VALOR"] >= 6 , 1 , 0 )
#df_metricas["BOT2"] = np.where( (df_metricas["VALOR"] <= 2) & (df_metricas["VALOR"] > 0) , 1 , 0 )
#print(df_metricas.head())


# In[ ]:


#del df_metricas["PERGUNTA"]
#del df_metricas["COLUNA"]


# In[ ]:


#df_metricas = df_metricas     \
#        .set_index(['CELEBRIDADE','FLIGHT'])     \
#        .join(df_awareness)     \
#        .set_index("ID")     \
#        .join( df[ pd.Series([ "FOTO_G" , "FOTO_M" , "FOTO_P", 'CELEBRIDADE', 'FLIGHT' ]) ]  )
#print(df_metricas.head())


# ----------

# <h3 style='color:blue'>13.2. VW_BASE_METRICAS (FULL)</h3>

# In[33]:


df_awareness = df.copy()

df_awareness['AW'] = np.where( df_awareness['AWARENESS'] == 1, 'S', 'N' )
df_awareness = df_awareness.groupby(['FLIGHT','CELEBRIDADE','AW'], as_index=False).count()
df_awareness = df_awareness[ pd.Series(['CELEBRIDADE','FLIGHT','AW', 'ID']) ].pivot_table('ID',['CELEBRIDADE','FLIGHT'],'AW')
df_awareness["AWARENESS"] = df_awareness['S'] / (df_awareness['S'] + df_awareness['N'])
df_awareness["AWARENESS_NIVEL"] = np.where( df_awareness['AWARENESS'] >= 0.65, 'Alto', 'Baixo' )

cols = [
    'ID',
    'CELEBRIDADE',
    'FLIGHT',
    'GOSTO_MUITO',
    'ME_IDENTIFICO',
    'TENHO_RESPEITO',
    'PRESTO_ATENCAO',
    'CONFIO',
    'MUITO_BOM_NAQUILO_QUE_FAZ',
    'INTELIGENTE',
    'DETERMINADO',
    'HONESTO',
    'ENGRAÇADO',
    'LINDO',
    'SEDUTOR',
    'DO_POVO',
    'CARA_DO_BRASIL',
    'INOVADOR',
    'GOSTA_DE_DESAFIOS',
    'TENHO_VISTO_NA_MIDIA',
    'BOA_PARA_PROPAGANDA',
    'COMPRARIA_PRODUTOS_QUE_ANUNCIASSE',
    'BOA_PARA_PROPAGANDA_PROJETOS_SOCIAIS',
    'ME_ENVOLVERIA_COM_PROJETOS_SOCIAIS_QUE_ANUNCIASSE',
    'INDICARIA_PARA_AMIGOS_MARCAS',
    'COMENTARIA_COM_AMIGOS_PROJETOS_SOCIAIS_QUE_ANUNCIASSE',
]

df_metricas = df.copy()

df_metricas = df_metricas[ pd.Series(cols) ]        .melt(id_vars=['ID', 'CELEBRIDADE', 'FLIGHT' ],  value_name= 'VALOR', var_name='METRICA')         .set_index("METRICA")         .join(meta)
    
df_metricas["TOP2"] = np.where( df_metricas["VALOR"] >= 6 , 1 , 0 )
df_metricas["BOT2"] = np.where( (df_metricas["VALOR"] <= 2) & (df_metricas["VALOR"] > 0) , 1 , 0 )

del df_metricas["PERGUNTA"]
del df_metricas["COLUNA"]

df_metricas = df_metricas             .set_index(['CELEBRIDADE','FLIGHT'])             .join(df_awareness)             .set_index("ID")             .join( df[ pd.Series([ "FOTO_G" , "FOTO_M" , "FOTO_P", 'CELEBRIDADE', 'FLIGHT' ]) ]  )

# Criação dos cálculos de positivo geral e negativo geral e merge desses dados no arquivo VW_BASE_METRICAS
df_metr1 = df_metricas.groupby(['CELEBRIDADE', 'FLIGHT', 'S', 'N', 'METRICA']).sum()
df_metr1.head(10)

df_metr1 = df_metr1.reset_index().set_index('CELEBRIDADE')

# Cálculo do positivo por celebridade
df_metr1['POSITIVO_G'] = df_metr1['TOP2']/df_metr1['S']

# Cálculo do negativo por celebridade
df_metr1['NEGATIVO_G'] = df_metr1['BOT2']/df_metr1['S']

df_metr2 = df_metr1[['FLIGHT', 'METRICA', 'POSITIVO_G', 'NEGATIVO_G']]

df_metr2 = df_metr2.groupby(['FLIGHT', 'METRICA']).mean().sort_index(ascending=False)


# In[38]:


# Merge no df_metricas
df_metricas = df_metricas.merge(df_metr2, how='inner', left_on=['FLIGHT', 'METRICA'], right_on=['FLIGHT', 'METRICA'])


# In[41]:


if OPT_GERAR_VW_BASE_METRICAS == 1:
    
    df_metricas = df_metricas.reset_index()    
    df_metricas.rename( columns ={ "index" : "ID"}, inplace=True)    
    df_metricas = df_metricas.set_index("ID")
    writeDF(df_metricas, 'VW_BASE_METRICAS')
    
    print("Arquivo exportado")


# ---

# <h3 style='color:purple'>VW_COMPARATIVO (passo-a-passo)</h3>

# In[ ]:


#df_latest_flight = df.groupby('CELEBRIDADE').max()['FLIGHT'].reset_index().set_index(['CELEBRIDADE','FLIGHT'])
#print(df_latest_flight.head())


# In[ ]:


#df_comp = df_metricas \
#    .join(df['AWARENESS'], rsuffix='_SN')
#print(df_comp.head())


# In[ ]:


#df_count_total = df \
#        .groupby(['FLIGHT','CELEBRIDADE'], as_index=False)['ID'] \
#        .count()
#print(df_count_total.head(10))


# In[ ]:


#df_count_total.rename( columns ={ "ID": "COUNT"}, inplace=True)
#print(df_count_total.head())


# In[ ]:


#df_count_aw = df[ df['AWARENESS']==1 ] \
#        .groupby(['FLIGHT','CELEBRIDADE'], as_index=False)['ID'] \
#        .count()
#print(df_count_aw.head())


# In[ ]:


#df_count_aw.rename( columns ={ "ID": "COUNT"}, inplace=True)
#print(df_count_aw.head())


# In[ ]:


#df_count = df_count_total \
#        .set_index(['FLIGHT','CELEBRIDADE']) \
#        .join(df_count_aw.set_index(['FLIGHT','CELEBRIDADE']), rsuffix='_AW')
#print(df_count.head())


# In[ ]:


#del df_count_total
#del df_count_aw


# In[ ]:


#df_comp = df_comp[ df_comp['AWARENESS_SN'] == 1 ] \
#        .groupby(['FLIGHT','CELEBRIDADE', 'FOTO_M','FOTO_P','FOTO_G','AWARENESS', 'AWARENESS_NIVEL', 'CONSTRUCTO','METRICA'], as_index=False) \
#        .agg({ "TOP2" : "sum", "BOT2" : "sum" })
#print(df_comp.head())


# In[ ]:


#df_comp = df_comp \
#        .reset_index()  \
#        .set_index(['FLIGHT','CELEBRIDADE']) \
#        .join(df_count)
#print(df_comp.head())


# In[ ]:


#df_comp['TOP2'] = df_comp['TOP2'] / df_comp['COUNT_AW']
#df_comp['BOT2'] = df_comp['BOT2'] / df_comp['COUNT_AW']
#print(df_comp['TOP2'].head())
#print(df_comp['BOT2'].head())


# In[ ]:


#df_comp = df_comp \
#    .reset_index() \
#    .set_index(['CELEBRIDADE','FLIGHT']) \
#    .join( df_latest_flight, how='inner' )
#print(df_comp.head())


# In[ ]:


#df_comp = df_comp \
#    .reset_index() \
#    .set_index(['CONSTRUCTO','METRICA'])
#print(df_comp.head())


# In[ ]:


#del df_comp['COUNT']
#del df_comp['COUNT_AW']


# In[ ]:


#df_compf = df_comp.join(df_comp, lsuffix = '_1', rsuffix = '_2')
#print(df_compf.head())


# -----

# <h3 style='color:blue'>13.3. VW_COMPARATIVO (FULL)</h3>

# In[ ]:


# Comparativo pelo último flight (21)
df_latest_flight = df.groupby('CELEBRIDADE').max()['FLIGHT'].reset_index().set_index(['CELEBRIDADE','FLIGHT'])

df_comp = df_metricas     .join(df['AWARENESS'], rsuffix='_SN') 

df_count_total = df         .groupby(['FLIGHT','CELEBRIDADE'], as_index=False)['ID']         .count()
df_count_total.rename( columns ={ "ID": "COUNT"}, inplace=True)    
df_count_aw = df[ df['AWARENESS']==1 ]         .groupby(['FLIGHT','CELEBRIDADE'], as_index=False)['ID']         .count()
df_count_aw.rename( columns ={ "ID": "COUNT"}, inplace=True)    

df_count = df_count_total         .set_index(['FLIGHT','CELEBRIDADE'])         .join(df_count_aw.set_index(['FLIGHT','CELEBRIDADE']), rsuffix='_AW')

del df_count_total
del df_count_aw

df_comp = df_comp[ df_comp['AWARENESS_SN'] == 1 ]         .groupby(['FLIGHT','CELEBRIDADE', 'FOTO_M','FOTO_P','FOTO_G','AWARENESS', 'AWARENESS_NIVEL', 'CONSTRUCTO','METRICA'], as_index=False)         .agg({ "TOP2" : "sum", "BOT2" : "sum" })

df_comp = df_comp         .reset_index()          .set_index(['FLIGHT','CELEBRIDADE'])         .join(df_count)

df_comp['TOP2'] = df_comp['TOP2'] / df_comp['COUNT_AW']
df_comp['BOT2'] = df_comp['BOT2'] / df_comp['COUNT_AW']

df_comp = df_comp     .reset_index()     .set_index(['CELEBRIDADE','FLIGHT'])     .join( df_latest_flight, how='inner' )

df_comp = df_comp     .reset_index()     .set_index(['CONSTRUCTO','METRICA'])

del df_comp['COUNT']
del df_comp['COUNT_AW']

df_compf = df_comp.join(df_comp, lsuffix = '_1', rsuffix = '_2')


# In[ ]:


if OPT_GERAR_VW_COMP == 1:
    
    writeDF(df_compf, 'VW_COMPARATIVO')
    
    print("Arquivo exportado")


# ---

# <h4 style='color:orange'>(Verificação) Pegar somente a quantidade de 'S' de cada 'CELEBRIDADE':</h4>

# In[ ]:


idc = df_awareness.index
print(idc)


# In[ ]:


print(df_awareness.loc[['Alessandra Negrini', '21']])


# ---