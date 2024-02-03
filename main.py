import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PyPDF2
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def gerar_tagcloud_pagina(arquivo_pdf_path, pagina=None):
    # Define stop words em português e adiciona termos específicos
    stopwords_pt = set(stopwords.words('portuguese')) | {'nº', 'lei', 'art', 'ltda', '1º','projeto', 's'}
    
    # Abre um arquivo PDF existente
    with open(arquivo_pdf_path, 'rb') as arquivo_pdf:
        leitor = PyPDF2.PdfReader(arquivo_pdf)
        texto = ""
        
        # Decide se processa uma página específica ou todo o documento
        if pagina is not None:
            pagina_obj = leitor.pages[pagina - 1]  # As páginas são indexadas a partir de 0
            texto = pagina_obj.extract_text().lower()
        else:
            for pagina_obj in leitor.pages:
                texto += pagina_obj.extract_text().lower() + " "
    
    # Processa o texto para remover stop words e termos específicos
    palavras = texto.split()
    texto_filtrado = ' '.join([palavra for palavra in palavras if palavra not in stopwords_pt])
    
    # Gera uma imagem de tag cloud com o texto filtrado
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_filtrado)
    
    # Exibe a imagem gerada
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
    # Corrige a criação do nome do arquivo de saída
    nome_arquivo_saida = 'tagcloud_pagina_{}.png'.format(pagina if pagina is not None else 'completo')
    wordcloud.to_file(nome_arquivo_saida)

# Chama a função sem especificar a página, processa todo o PDF
gerar_tagcloud_pagina('dados/2024_02_01_ASSINADO_do1.pdf')
