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

## Primeira Rede Textual Gerada

### Implementação Preliminar da Rede

A fase inicial de prototipagem, no arquivo `first_network.py`, estabeleceu as bases metodológicas para a modelagem da rede. O processo iniciou-se com o pré-processamento textual utilizando a biblioteca SpaCy e o modelo de linguagem `pt_core_news_sm`. Nesta etapa, aplicou-se a lematização dos *tokens* visando a redução de variações morfológicas, seguida da exclusão de *tokens* com comprimento inferior a dois caracteres.

A estrutura da rede foi definida como um grafo não-direcionado (*NetworkX Graph*), fundamentado na co-ocorrência de palavras. A lógica de construção baseou-se na combinação par a par de todos os termos presentes em cada comentário, utilizando a função `itertools.combinations`. Os pesos das arestas foram incrementados proporcionalmente à frequência de aparição conjunta dos pares. Para refinar a topologia da rede, aplicaram-se filtros de exclusão para arestas com peso inferior a 2 e nós com grau menor que 2, com o objetivo de destacar pares recorrentes e eliminar termos isolados ou de baixa relevância estatística. Por fim, realizou-se a normalização dos pesos para a escala entre 0 e 1 em relação ao peso máximo da rede, exportando-se o resultado em formato GEXF (`coocorrencia_normalizada.gexf`) para posterior visualização no software Gephi.

### Refinamento Metodológico para Apresentação Científica

Visando a comunicação dos resultados em formato de pôster científico (`poster_network.ipynb`), desenvolveu-se uma versão aprimorada da rede. O pré-processamento avançado incorporou critérios mais rigorosos de seleção, incluindo um limiar de peso de aresta (*MIN\_EDGE\_WEIGHT*) de 15 e a restrição da análise aos 200 nós de maior relevância topológica (*TOP\_N\_NODES*). Adicionalmente, definiu-se um conjunto de *stop words* específico para o domínio, excluindo verbos genéricos e marcadores conversacionais que não agregam valor semântico ao discurso político.

O *pipeline* de processamento integrou a lematização otimizada, a filtragem manual de ruídos e a remoção de duplicatas intra-comentário. A construção do grafo ocorreu de maneira incremental, atualizando os pesos para conexões preexistentes. O refinamento estrutural envolveu o corte de conexões fracas, a exclusão de nós isolados e a seleção dos nós baseada na centralidade de grau. Restringiu-se a topologia final ao componente gigante conexo para assegurar a integridade da análise de comunidades.

O grafo resultante consolidou-se com 200 nós representando os termos mais centrais e 10.564 conexões, caracterizando-se pela ausência de nós isolados ou componentes desconectados.

### Análise de Comunidades e Métricas

A identificação de subestruturas na rede foi realizada através do algoritmo de Louvain, configurado com resolução 1.0 e randomização ativa sobre os pesos normalizados (*norm\_weight*). A métrica de modularidade obtida foi de 0,0859, indicando o grau de segregação da rede em módulos distintos. Complementarmente, calcularam-se métricas de centralidade de grau para identificar os nós mais conectados, utilizando pesos normalizados para facilitar a análise comparativa.

Através da análise qualitativa dos termos centrais em cada agrupamento, foram identificados quatro contextos discursivos principais, detalhados na tabela em data/tabela_poster_final_ordenada.png. 

Para a representação visual no pôster, gerou-se uma tabela em alta resolução (300 dpi) utilizando a paleta de cores correspondente à visualização no Gephi e ordenando os contextos conforme a narrativa analítica desejada.

### Conclusão

Os resultados preliminares indicam uma rede densa composta pelos 200 termos mais centrais e mais de 10 mil conexões. A detecção de quatro comunidades distintas, com modularidade de 0.0859, permitiu mapear os principais eixos do debate. O contexto "Ataques a Políticos" (Verde) revela um discurso focado em ataques a uma figura política específica, enquanto a "Pauta Econômica/Social" (Roxo) referencia preocupações do cenário nacional. O "Discurso Moralizante" (Laranja) agrupa a opinião pública a favor de um candidato específico do debate, e a Mobilização Ideológica" (Azul) mostra, finalmente, a discussão sobre o assunto central do vídeo: corrupção. Conclui-se que apesar do tema principal do vídeo ser corrupção, há a ação de um grupo a favor de um político específico que domina quase 50% da rede com ataque ao político que está sendo interrogado no vídeo + defesa do interrogador. Assim, é possível concluir que o vídeo foi usado por um grupo dominante para atacar o opositor de seu político favorito, fugindo do assunto principal do vídeo e usando-o como palanque para a disseminação de opiniões sobre candidatos à presidência de 2022.

## Infraestrutura Computacional e Organização do Projeto

O desenvolvimento do projeto requer um ambiente Python configurado com um conjunto específico de bibliotecas. Utilizou-se o `python-dotenv` para gerenciamento seguro de variáveis de ambiente, `pandas` para manipulação tabular de dados e `tqdm` para monitoramento de processos iterativos. O núcleo do processamento de linguagem natural baseou-se no `nltk` e no `spacy` (modelo `pt_core_news_sm`), enquanto a coleta de dados foi intermediada pelo `google-api-python-client`. A modelagem e análise de redes complexas foram realizadas com `networkx` e `python-louvain`, sendo a visualização de dados suportada pelo `matplotlib`.

A estrutura de arquivos do projeto organiza-se de forma modular, separando scripts de coleta (`youtube_scratch.py`), limpeza (`clean_data.py`) e modelagem de redes (`first_network.py`, `poster_network.ipynb`). Os dados brutos e processados, bem como os arquivos de grafo (.gexf) e visualizações finais, encontram-se alocados no diretório `data/`.

## Andamento do Trabalho

✅ **Coleta e Organização do Corpus**
Finalizada a constituição da base de dados, composta por comentários de vídeos do YouTube selecionados para garantir a diversidade temática e temporal estipulada no plano de trabalho, estabelecendo o alicerce empírico para a investigação.

✅ **Limpeza e Pré-processamento**
Concluídos os protocolos de higienização, lematização e normalização textual. Esta etapa assegurou a integridade e a padronização dos dados, requisito fundamental para a aplicação precisa das diferentes técnicas de modelagem de redes.

⏳ **Implementação e Análise Comparativa de Modelagens**
Encontra-se em curso a expansão das técnicas de modelagem de redes textuais. Embora a análise exploratória via co-ocorrência tenha produzido resultados preliminares de comunidades léxicas, o trabalho prossegue com a implementação de variações nos critérios de construção (alternando unidades de análise, tipos de aresta como dependência sintática e janelas de contexto). Simultaneamente, avança-se para a aplicação de métricas estruturais e para a avaliação do desempenho destas topologias em tarefas de mineração de opinião, visando a futura comparação dos resultados e a elaboração das diretrizes metodológicas finais.

---

## Referências

AGGARWAL, Tushar. *NetworkX: A comprehensive guide to mastering network analysis with Python.* Medium, 2023. Disponível em: [https://medium.com/@tushar_aggarwal/networkx-a-comprehensive-guide-to-mastering-network-analysis-with-python-fd7e5195f6a0](https://medium.com/@tushar_aggarwal/networkx-a-comprehensive-guide-to-mastering-network-analysis-with-python-fd7e5195f6a0). 

BIRD, Steven; KLEIN, Ewan; LOPER, Edward. *NLTK Documentation – Portuguese HOWTO.* Disponível em: [https://www.nltk.org/howto/portuguese_en.html](https://www.nltk.org/howto/portuguese_en.html). 

BLONDEL, Vincent D. et al. *Fast unfolding of communities in large networks.* Journal of Statistical Mechanics: Theory and Experiment, v. 2008, n. 10, 2008.

CARVALHO, André C. P. L. F. de; MENEZES, Ângelo G.; BONIDIA, Robson P. *Ciência de Dados: Fundamentos e Aplicações.* 1. ed. Rio de Janeiro: LTC, 2024. ISBN 9788521638766. E-book.

GOOGLE DEVELOPERS. *YouTube Data API v3 – Comments: list.* Disponível em: [https://developers.google.com/youtube/v3/docs/comments/list?hl=pt-br](https://developers.google.com/youtube/v3/docs/comments/list?hl=pt-br). 

SICSS. *Text Networks.* Disponível em: [https://sicss.io/2018/materials/day3-text-analysis/text-networks/rmarkdown/SICSS_Text_Networks.html](https://sicss.io/2018/materials/day3-text-analysis/text-networks/rmarkdown/SICSS_Text_Networks.html). 

VEGA, Diego; MAGNANI, Matteo. *Foundations of Temporal Text Networks.* *Applied Network Science*, v. 3, n. 25, 2018. DOI: [https://doi.org/10.1007/s41109-018-0082-3](https://doi.org/10.1007/s41109-018-0082-3). Disponível em: [https://appliednetsci.springeropen.com/articles/10.1007/s41109-018-0082-3](https://appliednetsci.springeropen.com/articles/10.1007/s41109-018-0082-3).

---

## Licença e Contato

Este projeto está sendo desenvolvido como parte de pesquisa acadêmica. Para mais informações ou colaborações, entre em contato através do repositório do projeto.