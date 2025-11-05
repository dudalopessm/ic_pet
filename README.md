# Análise de Comentários de Vídeos do YouTube utilizando Redes Textuais

## Contextualização

Este projeto investiga diferentes estratégias de modelagem de redes textuais aplicadas a comentários de vídeos do YouTube, com foco em mineração de opinião e análise exploratória. A literatura apresenta lacunas quanto ao impacto comparativo das diferentes abordagens de modelagem na qualidade das análises resultantes.

## Objetivos

### Objetivo Geral
Explorar técnicas de representação de redes textuais de forma comparativa, avaliando qual modelagem oferece melhor desempenho para tarefas específicas de análise.

### Objetivos Específicos
- Coletar e organizar corpus de comentários do YouTube com diversidade temática e temporal
- Implementar diferentes técnicas de modelagem de redes textuais (variando unidade de análise, tipo de aresta e janela de contexto)
- Aplicar métricas de análise de redes (centralidade, modularidade, densidade)
- Avaliar desempenho em tarefas de mineração de opinião
- Conduzir análises exploratórias para identificação de comunidades léxicas e padrões discursivos
- Comparar resultados e elaborar diretrizes metodológicas

## Metodologia

### Técnicas de Modelagem
- **Unidades de análise**: palavras vs sentenças
- **Tipos de aresta**: co-ocorrência, dependência sintática, distância lexical

### Tarefas de Avaliação
- Mineração de opinião (polaridade, subjetividade)
- Análise exploratória (comunidades léxicas, padrões discursivos)

---

## Coleta e Pré-processamento dos Dados

### Seleção do Corpus

Inicialmente, identificou-se a necessidade de um conjunto de dados volumoso para evidenciar a polarização de opiniões na rede textual. Após busca por temas polêmicos no YouTube, o vídeo "‹ CORTANDO O BOTÃO DO YOUTUBE ›" do youtuber Aruan Felix foi considerado: publicado há 9 anos, possui 29 milhões de visualizações e 582331 comentários. Apesar de representar um tema marcante, a recuperação completa dos comentários mostrou-se inviável devido às limitações da cota diária da API do YouTube.

Diante dessa restrição, optou-se pelo vídeo "Bolsonaro pergunta para Lula sobre corrupção na Petrobras | Band Eleições - Debate Presidencial 2022" do canal Band Jornalismo. Publicado há 3 anos, o vídeo possui 9,6 milhões de visualizações e 53831 comentários. Embora represente uma redução de aproximadamente 10 vezes no volume de dados, a natureza inerentemente polarizada do debate político compensaria a menor quantidade de comentários, garantindo a presença de opiniões divergentes necessárias para a análise.

**Vídeo selecionado:**
- Título: "Bolsonaro pergunta para Lula sobre corrupção na Petrobras | Band Eleições - Debate Presidencial 2022"
- Canal: Band Jornalismo
- Visualizações: 9,6 milhões
- Comentários: 53831
- Ano: 2022

### Configuração do Ambiente

O ambiente de desenvolvimento foi estruturado com:
- Ambiente virtual Python
- Dependências necessárias instaladas
- Arquivo `.env` configurado contendo:
  - Chave da API do YouTube
  - Caminhos para salvamento dos arquivos CSV
  - Código identificador do vídeo

### Extração dos Dados

**Arquivo:** `youtube_scratch.py`

A extração foi realizada utilizando a YouTube Data API v3. O processo envolveu:

1. Recuperação dos comentários principais através da função `commentThreads().list()`, obtendo conteúdo e datas de publicação
2. Para cada comentário principal recuperado, utilização da função `comments().list()` para recuperação de todas as respostas associadas
3. Armazenamento temporário dos dados em DataFrame do Pandas
4. Exportação completa para arquivo CSV

**Resultado:** Conjunto bruto de 53831 comentários recuperados com sucesso.

### Limpeza e Pré-processamento

**Arquivo:** `clean_data.py`

Os dados brutos apresentavam inconsistências típicas de textos de redes sociais. Para tratamento, utilizou-se a biblioteca NLTK (Natural Language Toolkit).

**Processo de limpeza:**

1. **Stopwords**: Utilização da lista de stopwords em português-BR fornecida pela NLTK, contendo 207 palavras (lista completa disponível via `print(sorted(stopwords_portugues))` no arquivo `clean_data.py`)

2. **Função `cleaning_comments()`**: 
   - Recebe conteúdo bruto do comentário
   - Converte para minúsculas
   - Remove acentuação
   - Remove stopwords
   - Tokenização através de `word_tokenize()`
   - Filtragem: mantém apenas tokens alfanuméricos não presentes na lista de stopwords
   - Retorna comentário limpo com tokens unidos por espaços

3. **Exportação**: Salvamento dos comentários processados em novo arquivo CSV

### Considerações sobre a Qualidade dos Dados

Após o processo de limpeza, observa-se que alguns elementos indesejados permanecem no conjunto de dados:
- Menções a nomes de usuário (@username)
- Comentários spam (combinações aleatórias de números e letras)

A remoção completa desses elementos comprometeria a veracidade e integridade do corpus. Avalia-se que sua presença não prejudicará significativamente as etapas subsequentes de modelagem e análise de redes textuais.

---

## Status Atual

- ✅ Corpus coletado e organizado
- ✅ Dados limpos e pré-processados
- ⏳ Implementação de modelagens de redes textuais (em andamento)

---

## Dependências
```bash
pip install python-dotenv pandas nltk google-api-python-client tqdm
```

### Bibliotecas utilizadas:
- `python-dotenv`: Gerenciamento de variáveis de ambiente
- `pandas`: Manipulação e análise de dados
- `nltk`: Processamento de linguagem natural
- `google-api-python-client`: Acesso à YouTube Data API v3
- `tqdm`: Barras de progresso para loops

### Configuração do NLTK

Após instalação, execute no Python:
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

---

## Referências

AGGARWAL, Tushar. *NetworkX: A comprehensive guide to mastering network analysis with Python.* Medium, 2023. Disponível em: [https://medium.com/@tushar_aggarwal/networkx-a-comprehensive-guide-to-mastering-network-analysis-with-python-fd7e5195f6a0](https://medium.com/@tushar_aggarwal/networkx-a-comprehensive-guide-to-mastering-network-analysis-with-python-fd7e5195f6a0). 

BIRD, Steven; KLEIN, Ewan; LOPER, Edward. *NLTK Documentation – Portuguese HOWTO.* Disponível em: [https://www.nltk.org/howto/portuguese_en.html](https://www.nltk.org/howto/portuguese_en.html). 

CARVALHO, André C. P. L. F. de; MENEZES, Ângelo G.; BONIDIA, Robson P. *Ciência de Dados: Fundamentos e Aplicações.* 1. ed. Rio de Janeiro: LTC, 2024. ISBN 9788521638766. E-book.

GOOGLE DEVELOPERS. *YouTube Data API v3 – Comments: list.* Disponível em: [https://developers.google.com/youtube/v3/docs/comments/list?hl=pt-br](https://developers.google.com/youtube/v3/docs/comments/list?hl=pt-br). 

SICSS. *Text Networks.* Disponível em: [https://sicss.io/2018/materials/day3-text-analysis/text-networks/rmarkdown/SICSS_Text_Networks.html](https://sicss.io/2018/materials/day3-text-analysis/text-networks/rmarkdown/SICSS_Text_Networks.html). 

VEGA, Diego; MAGNANI, Matteo. *Foundations of Temporal Text Networks.* *Applied Network Science*, v. 3, n. 25, 2018. DOI: [https://doi.org/10.1007/s41109-018-0082-3](https://doi.org/10.1007/s41109-018-0082-3). Disponível em: [https://appliednetsci.springeropen.com/articles/10.1007/s41109-018-0082-3](https://appliednetsci.springeropen.com/articles/10.1007/s41109-018-0082-3).

---