#  1️⃣ 🤖 Reforma Tributária AI Agent

> **Agente de Inteligência Artificial para consulta, capacitação e apoio à implementação da Reforma Tributária**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/AI-RAG-purple)]()
[![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/)
[![Oracle Cloud](https://img.shields.io/badge/Cloud-Oracle%20Cloud-red?logo=oracle)](https://www.oracle.com/cloud/)

---

## 2️⃣ 🚧 Status do projeto

**Status:** 🟡 Em desenvolvimento

O projeto está em fase de construção e validação do pipeline de **RAG (Retrieval-Augmented Generation)** para consulta inteligente a documentos oficiais relacionados à Reforma Tributária.

A primeira versão do projeto tem como foco documentos em **formato PDF**, priorizando qualidade de processamento, rastreabilidade das fontes e confiabilidade das respostas.

### 📊 Status atual do MVP

#### ✅ Concluído

- [x] Levantamento e seleção das fontes oficiais
- [x] Curadoria documental inicial
- [x] Catálogo documental
- [x] Organização dos documentos por módulo
- [x] Definição e padronização dos metadados
- [x] Definição da arquitetura RAG
- [x] Estruturação do projeto
- [x] Ingestão de documentos PDF
- [x] Extração de conteúdo
- [x] Limpeza e normalização do texto
- [x] Chunking
- [x] Validação da qualidade dos chunks
- [x] Geração de embeddings
- [x] Pipeline de processamento
- [x] Testes automatizados do pipeline

#### 🚧 Em desenvolvimento

- [ ] Indexação vetorial com Vector Store
- [ ] Busca por similaridade semântica
- [ ] Retriever
- [ ] Integração com LLM
- [ ] Geração de respostas fundamentadas nas fontes
- [ ] Interface conversacional
- [ ] Avaliação da qualidade das respostas
- [ ] Deploy na OCI

### 🔄 Pipeline atual

```text
📄 PDF oficial
      ↓
📥 PDF Loader                                       ✅
      ↓
🔎 Extraction     Arquivo → páginas                 ✅
      ↓
🧹 Cleaning       Páginas → páginas limpas          ✅
      ↓
✂️ Chunking       Texto + metadata → chunks         ✅
      ↓
🏷️ Metadata      Documento → metadata padronizado   ✅
      ↓
🔄 Pipeline       Orquestração                      ✅  
      ↓
🧠 Embeddings                                       ✅
      ↓
🗄️ Vector Store                                    ⏳ ← próximo
      ↓
🔍 Retriever               ⏳
      ↓
🤖 RAG                     ⏳
🔍 Retriever                                       ⏳
      ↓        
🤖 RAG                                             ⏳

```

## 🧪 Cobertura de testes

A camada de processamento possui 53 testes automatizados, com 53/53 testes passando.

| Módulo                  | Testes |    Status   |
| ----------------------- | -----: | :---------: |
| ✂️ Chunking             |     10 |      ✅      |
| 🧠 Qualidade dos chunks |      5 |      ✅      |
| 🧹 Cleaning             |      7 |      ✅      |
| 🔢 Embeddings           |      6 |      ✅      |
| 📄 Extraction           |      7 |      ✅      |
| 📥 Ingestion            |      2 |      ✅      |
| 🏷️ Metadata            |     10 |      ✅      |
| 🔄 Pipeline             |      6 |      ✅      |
| **Total**               | **53** | **✅ 53/53** |

Marco atual: o pipeline de processamento documental está validado por testes automatizados. A próxima etapa é concluir a indexação vetorial e validar a recuperação semântica.


### 🎯 Próxima etapa

Etapa 3 — Indexação vetorial

 Armazenamento dos embeddings no Vector Store
 Persistência da base vetorial
 Indexação para busca por similaridade
 Validação da recuperação dos chunks
 Preservação e utilização dos metadados
 Testes de busca semântica
🔮 Roadmap futuro

Após a consolidação do MVP:

 Citações das fontes por página
 Busca híbrida (semântica + lexical)
 Re-ranking
 Atualização automatizada da base documental
 Expansão para outros formatos de documentos
 Monitoramento e avaliação contínua do agente

###  3️⃣ 📌 Sobre o projeto

O **Reforma Tributária AI Agent** é um agente de Inteligência Artificial desenvolvido para facilitar a consulta, compreensão e capacitação sobre a **Reforma Tributária do Consumo**.

A solução utiliza **RAG — Retrieval-Augmented Generation** para transformar documentos oficiais e institucionais em uma base de conhecimento consultável por linguagem natural.

O usuário pode realizar perguntas sobre temas da Reforma Tributária e receber respostas contextualizadas a partir dos documentos recuperados, mantendo a **rastreabilidade da informação por meio dos metadados e das fontes documentais utilizadas**.

O projeto foi concebido com foco em **curadoria documental, recuperação semântica e respostas fundamentadas**, buscando reduzir o tempo necessário para localizar informações relevantes em documentos técnicos extensos.

---

## 4️⃣⭐ Diferencial do projeto

Uma solução de conhecimento documental baseada em RAG, com curadoria, catalogação, metadados, recuperação semântica e respostas fundamentadas em fontes oficiais.

O diferencial da solução está na construção da base de conhecimento.

Os documentos não são simplesmente disponibilizados ao modelo de linguagem. Antes da ingestão, passam por um processo de **seleção, identificação, catalogação e organização**, considerando informações como:

- Instituição responsável pela publicação;
- Módulo e tema;
- Título do documento;
- Data de publicação ou atualização;
- Data de acesso;
- URL oficial de origem;
- Tipo de documento;
- Status na curadoria;
- Metadados necessários para rastreabilidade.

Essa abordagem permite construir uma base documental estruturada e preparada para recuperação semântica, contribuindo para respostas mais contextualizadas e verificáveis.

```
🏛️ FONTES OFICIAIS
        ↓
📋 CATÁLOGO DOCUMENTAL
        ↓
🔎 CURADORIA
        ↓
🏷️ METADADOS
        ↓
📄 INGESTÃO
        ↓
✂️ CHUNKING
        ↓
🧮 EMBEDDINGS
        ↓
🗄️ VECTOR STORE
        ↓
🔍 RETRIEVAL
        ↓
🧠 LLM
        ↓
💬 RESPOSTA
        ↓
📚 FONTE + PÁGINA
```

```
ingestion/ → prepara o documento;
vectorstore/ → transforma chunks em vetores, armazena e recupera;
retriever.py → futuramente busca os chunks relevantes;
store.py → futuramente controla o banco vetorial.

O embeddings.py será responsável somente por:

carregar o modelo de embeddings;
                    │
                    ▼
transformar texto em vetores;
                    │
                    ▼
transformar vários chunks em vetores;
                    │
                    ▼
validar entradas;
                    │
                    ▼
manter a dimensão dos embeddings consistente.

paraphrase-multilingual-MiniLM-L12-v2 = porque o  projeto está em português e os documentos são da Reforma Tributária.
normalize_embeddings= deixa os vetores normalizados, o que é útil para buscas por similaridade posteriormente.

                DOCUMENTO
                    │
                    ▼
            ┌───────────────┐
            │  Extraction   │
            └───────┬───────┘
                    ▼
            ┌───────────────┐
            │   Cleaning    │
            └───────┬───────┘
                    ▼
            ┌───────────────┐
            │   Metadata    │
            └───────┬───────┘
                    ▼
            ┌───────────────┐
            │   Chunking    │
            └───────┬───────┘
                    ▼
             🧬 EMBEDDINGS
                    │
                    ▼
            ┌───────────────┐
            │ Vector Store  │
            └───────┬───────┘
                    ▼
               Retriever
                    │
                    ▼
                 RAG
                    │
                    ▼
                 Agent
```
---

## 5️⃣ 🎯 Objetivo

Desenvolver um agente de IA capaz de:

* Responder perguntas relacionadas à Reforma Tributária do Consumo;
* Apoiar a capacitação de profissionais da Contabilidade;
* Facilitar a consulta de documentos técnicos e institucionais;
* Estruturar uma base de conhecimento a partir de documentos oficiais;
* Recuperar informações relevantes por meio de busca semântica;
* Gerar respostas contextualizadas a partir dos trechos recuperados;
* Manter a rastreabilidade das informações por meio de metadados e fontes;
* Reduzir o tempo necessário para localizar informações em documentos extensos;
* Controlar respostas quando não houver evidências suficientes na base;
* Disponibilizar uma interface conversacional para consulta do conhecimento.

---

## 6️⃣💡 Problema

A Reforma Tributária envolve mudanças relevantes na estrutura tributária brasileira e demanda atualização contínua por parte dos profissionais de Contabilidade.

Informações importantes podem estar distribuídas em diferentes documentos, materiais técnicos, orientações e regulamentações, tornando a busca manual mais demorada e dificultando a localização rápida de informações específicas.

Diante desse cenário, surge a oportunidade de utilizar Inteligência Artificial para criar uma camada conversacional sobre essa base documental.

Em vez de o profissional precisar localizar manualmente determinada informação em diversos documentos, o agente permite realizar uma pergunta em linguagem natural e receber uma resposta baseada nos conteúdos disponíveis.

---

## 7️⃣👥 Público-alvo

O agente foi concebido principalmente para:

* Contadores;
* Profissionais da área contábil;
* Equipes fiscais e tributárias;
* Profissionais envolvidos na implementação da Reforma Tributária;
* Estudantes e profissionais que desejam compreender o tema;
* Usuários interessados em consultar informações sobre a Reforma Tributária.

O acesso ao agente será **aberto**, não havendo necessidade de restringir sua utilização a um grupo específico de usuários.

---

## 8️⃣🎯 Escopo do MVP

A primeira versão do projeto terá como foco:

- Documentos em formato PDF;
- Materiais oficiais relacionados à Reforma Tributária do Consumo;
- Base documental inicialmente concentrada nos materiais RFB/CFC;
- Processamento e fragmentação dos documentos;
- Geração de embeddings;
- Recuperação semântica;
- Geração de respostas por LLM;
- Apresentação das fontes recuperadas;
- Interface conversacional;
- Disponibilização da aplicação em ambiente cloud.

Formatos adicionais, novas instituições e funcionalidades avançadas serão incorporados em etapas posteriores.

---

---

## 9️⃣🧠 Como funciona?

A solução utiliza uma arquitetura baseada em **RAG — Retrieval-Augmented Generation**.

O fluxo conceitual é:

```text
                    📄 DOCUMENTOS
                         │
          ┌──────────────┼──────────────┐
          │              │              │
         CFC          FENACON      RECEITA FEDERAL
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                  📚 Base documental
                         ↓
                  🔎 Extração de texto
                         ↓
                    ✂️ Chunking
                         ↓
                   🧮 Embeddings
                         ↓
                  🗄️ Banco vetorial
                         ↓
                     🔍 Retriever
                         ↓
                 📑 Contexto relevante
                         ↓
                     🧠 Agente IA
                         ↓
                    🤖 Modelo LLM
                         ↓
                   💬 Resposta
                         ↓
                 📚 Fontes consultadas
```

> **Nota:** os documentos inicialmente selecionados para o MVP são materiais oficiais do **Curso Reforma Tributária RFB e CFC**, disponibilizados no portal da Receita Federal. Materiais do CFC e da Fenacon poderão ser incorporados posteriormente, conforme a evolução da base de conhecimento.

---

## 🔟🔎 RAG

O **RAG (Retrieval-Augmented Generation)** permite que o modelo de linguagem consulte informações recuperadas da base documental antes de gerar uma resposta.

Dessa forma, o agente não depende exclusivamente do conhecimento previamente aprendido pelo modelo.

O processo ocorre em duas etapas principais:

### Retrieval

```text
Pergunta
   ↓
Query Processing
   ↓
Retriever
   ↓
Top-K documentos
   ↓
Re-ranking
   ↓
Contexto relevante
   ↓
LLM
   ↓
Resposta + citações
```

### Generation

```text
Pergunta
   +
Contexto recuperado
   ↓
Modelo de linguagem
   ↓
Resposta contextualizada
```


# 📄 Documentos


## 1️⃣1️⃣📚 Fontes de conhecimento

A base documental inicial foi estruturada a partir de materiais relacionados à **Reforma Tributária do Consumo**, priorizando fontes oficiais e institucionais.

A primeira etapa da curadoria concentra-se nos materiais disponibilizados pela **Receita Federal do Brasil (RFB)** em parceria com o **Conselho Federal de Contabilidade (CFC)**.

## 🏛️ Receita Federal do Brasil — RFB

A principal fonte documental inicial do projeto será o **Curso Reforma Tributária RFB e CFC**, disponibilizado pela Receita Federal do Brasil.

### 🔗 Fonte oficial dos documentos

**[📖 Módulos do Curso Reforma Tributária RFB e CFC — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso)**

Os materiais são disponibilizados oficialmente em formato PDF e contemplam diferentes temas relacionados à Reforma Tributária do Consumo.

### 📌 Data de referência da curadoria

Os documentos utilizados na primeira seleção foram identificados com atualizações realizadas entre **29/07/2026 e 07/08/2026**, conforme as informações disponibilizadas no portal oficial da Receita Federal.

---

## 1️⃣2️⃣📋 Catálogo documental

> 📌 **O catálogo documental é a camada de governança da base de conhecimento.**
> Ele permite saber quais documentos foram selecionados, por quê,
> de onde vieram, qual versão foi utilizada e qual é o seu status no RAG.

Antes da ingestão dos documentos na base de conhecimento, foi realizada uma etapa de **curadoria e catalogação documental**.

O catálogo tem como objetivo registrar a origem, identificação, classificação e situação de cada documento, permitindo controlar quais materiais foram selecionados para o RAG e quais ainda estão previstos para incorporação.

### Informações catalogadas

| Campo | Descrição |
|---|---|
| Instituição | Organização responsável pelo documento |
| Módulo | Módulo ou agrupamento temático |
| Documento | Nome do material |
| Tema | Assunto principal abordado |
| Tipo | PDF, DOCX, XLSX etc. |
| Data de publicação | Data disponibilizada pela fonte |
| Última atualização | Data da última modificação informada pela fonte |
| Data de acesso | Data em que o documento foi consultado |
| URL oficial | Origem oficial do documento |
| Status | Selecionado, em análise ou futuro |
| Categoria | Classificação temática |
| Observações | Informações adicionais da curadoria |

### Processo de curadoria

```text
📚 Fonte institucional
        ↓
🔎 Identificação dos documentos
        ↓
📋 Catalogação
        ↓
🧹 Curadoria
        ↓
🏷️ Classificação e metadados
        ↓
✅ Seleção para ingestão
        ↓
📄 Processamento
        ↓
🧠 Base de conhecimento RAG
```

---


## 1️⃣3️⃣📑 Documentos utilizados na base inicial

### Módulo 1 — Normas Gerais da Tributação do Consumo

| Documento           | Tema                                   | Fonte oficial                                                                                                                                                                                                                                          |
| ------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Módulo 1 — 1ª parte | Normas Gerais da Tributação do Consumo | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-cfc-rfb-modulo-1-mombelli_maio-2026-final.pdf/view) |
| Módulo 1 — 2ª parte | Normas Gerais da Tributação do Consumo | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-cfc-rfb-modulo-1_roni_maio-2026.pdf/view)           |

### Módulo 2 — CBS na Importação e Exportação

| Documento           | Tema                                                                 | Fonte oficial                                                                                                                                                                                                                                                                         |
| ------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 2 — 1ª parte | A CBS na importação e na exportação de bens materiais                | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/cbs-no-comercio-exterior-curso-cfc-rfb-26-05-2026.pdf/view)                              |
| Módulo 2 — 2ª parte | A CBS na importação e na exportação de bens materiais — Aula prática | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/cbs-no-comercio-exterior-curso-cfc-rfb-26-05-2026_aula-pratica_sergio_completa.pdf/view) |

### Módulo 3 — Fundo de Compensação de Benefícios Fiscais

| Documento           | Tema                                              | Fonte oficial                                                                                                                                                                                                                                            |
| ------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 3 — 1ª parte | Fundo de Compensação de Benefícios Fiscais — FCBF | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-rtc-cfc-rfb-3o-modulo-fcbf-gustavo-busato.pdf/view)   |
| Módulo 3 — 2ª parte | Fundo de Compensação de Benefícios Fiscais — FCBF | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-rtc-cfc-rfb-3o-modulo-fcbf-fernando-kreisig.pdf/view) |

### Módulo 4 — Cadastro

| Documento           | Tema     | Fonte oficial                                                                                                                                                                                                                                                                  |
| ------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Módulo 4 — 1ª parte | Cadastro | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/cadastronocontextodartc-modulo-4-roni-acertada-com-reriton-versao-final.pdf/view) |
| Módulo 4 — 2ª parte | Cadastro | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/4o-modulo-apresentacao-final-cadastro.pdf/view)                                   |
| Módulo 4 — 3ª parte | Cadastro | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/20260615-apresentacao-rtc-rev.pdf/view)                                           |

### Módulo 5 — Obrigações Acessórias

| Documento           | Tema                                                           | Fonte oficial                                                                                                                                                                                                                                                                                    |
| ------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Módulo 5 — 1ª parte | Obrigações Acessórias — Documentos Fiscais / NF-e / NFS-e      | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/5deg-modulo-cfc-rfb-obrigacoes-acessorias-documentos-fiscais-nfs-e-hermano.pdf/view)                |
| Módulo 5 — 2ª parte | Obrigações Acessórias — Calculadora / Motor Oficial de Cálculo | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/5o-modulo-cfc-rfb-obrigacoes-acessorias-calculadora-motor-oficial-de-calculo-ariel-bonzan.pdf/view) |
| Módulo 5 — 3ª parte | Obrigações Acessórias — Documentos Fiscais                     | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/5o-modulo-cfc-rfb-obrigacoes-acessorias-documentos-fiscais-marco-duran.pdf/view)                    |
| Módulo 5 — 4ª parte | Obrigações Acessórias — EFD Contribuições                      | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/5o-modulo-cfc-rfb-obrigacoes-acessorias-efd-contribuicoes-guilherme.pdf/view)                       |
| Módulo 5 — 5ª parte | Obrigações Acessórias — Legislação CBS/IBS                     | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/5o-modulo-cfc-rfb-obrigacoes-acessorias-legislacao-cbs-ibs-wolney.pdf/view)                         |

### Módulo 6 — Apuração Assistida da CBS

| Documento           | Tema                      | Fonte oficial                                                                                                                                                                                                                                               |
| ------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 6 — 1ª parte | Apuração Assistida da CBS | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-reforma-tributaria-rfb-e-cfc-modulo-6-1a-parte.pdf/view) |
| Módulo 6 — 2ª parte | Apuração Assistida da CBS | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-reforma-tributaria-rfb-e-cfc-modulo-6-2a-parte.pdf/view) |

### Módulo 7 — Compensação, Ressarcimento, Restituição e Transferências

| Documento           | Tema                                                     | Fonte oficial                                                                                                                                                                                                                                               |
| ------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 7 — 1ª parte | Compensação, Ressarcimento, Restituição e Transferências | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-reforma-tributaria-rfb-e-cfc-modulo-7-1a-parte.pdf/view) |
| Módulo 7 — 2ª parte | Compensação, Ressarcimento, Restituição e Transferências | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-reforma-tributaria-rfb-e-cfc-modulo-7-2a-parte.pdf/view) |
| Módulo 7 — 3ª parte | Compensação, Ressarcimento, Restituição e Transferências | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-reforma-tributaria-rfb-e-cfc-modulo-7-3a-parte.pdf/view) |
| Módulo 7 — 4ª parte | Compensação, Ressarcimento, Restituição e Transferências | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/curso-reforma-tributaria-rfb-e-cfc-modulo-7-4a-parte.pdf/view) |

### Módulo 8 — Simples Nacional e MEI

| Documento           | Tema                                    | Fonte oficial                                                                                                                                                                                                                                                  |
| ------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 8 — 1ª parte | PGDAS-D e sua evolução para o PGDAS-A   | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/modulo-8-cfc-rfb-simples-nacional-mei-fabio-de-tarsis.pdf/view)   |
| Módulo 8 — 2ª parte | Mudanças nas normas do Simples Nacional | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/modulo-8-cfc-rtc-simples-nacional-mei-gustavo-salton-vf.pdf/view) |
| Módulo 8 — 3ª parte | Opções — Simples Nacional e IBS/CBS     | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/modulo-8-cfc-rtc-simples-nacional-mei-tiago-sfreddo-vf.pdf/view)  |

### Módulo 9 — Economia Digital

| Documento           | Tema             | Fonte oficial                                                                                                                                                                                                                                                         |
| ------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 9 — 1ª parte | Economia Digital | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/modulo-9-curso-rtc-cfc-rfb-economia-digital-joao-hamilton-rech.pdf/view) |
| Módulo 9 — 2ª parte | Economia Digital | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/modulo-9-curso-rtc-cfc-rfb-economia-digital-fabricio-betto.pdf/view)     |

### Módulo 10 — Regimes Específicos e Diferenciados

| Documento            | Tema                                              | Fonte oficial                                                                                                                                                                                                                                                   |
| -------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 10 — 1ª parte | Regimes Específicos e Diferenciados               | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/01_claudia_regimes_especificos_e_diferenciados_modulo_10.pdf/view) |
| Módulo 10 — 2ª parte | Regimes Específicos e Diferenciados               | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/02_anelise_regimes_diferenciados_modulo_10.pdf/view)               |
| Módulo 10 — 3ª parte | Normas sobre Regimes Específicos                  | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/03_gustavo_normas_sobre_regimes_especificos_modulo_10.pdf/view)    |
| Módulo 10 — 4ª parte | Regimes Específicos e Diferenciados               | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/04_huning_regimes_especificos_e_diferenciados_modulo_10.pdf/view)  |
| Módulo 10 — 5ª parte | Regimes Específicos e Diferenciados — Operacional | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/05_flores_operacional_modulo_10.pdf/view)                          |

### Módulo 11 — Planos de Assistência à Saúde e Concursos de Prognóstico

| Documento            | Tema                                                     | Fonte oficial                                                                                                                                                                                                   |
| -------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Módulo 11 — 1ª parte | Planos de Assistência à Saúde e Concursos de Prognóstico | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/mdulo1-1.pdf/view) |
| Módulo 11 — 2ª parte | Planos de Assistência à Saúde e Concursos de Prognóstico | [📄 PDF oficial](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso/mdulo1-2.pdf/view) |

---

## 1️⃣4️⃣📊 Organização temática da base

A documentação catalogada está organizada por módulos e temas, permitindo associar cada fragmento recuperado ao seu contexto documental de origem.

```text
Reforma Tributária do Consumo
│
├── Módulo 1
│   └── Normas Gerais da Tributação do Consumo
│
├── Módulo 2
│   └── CBS na Importação e Exportação
│
├── Módulo 3
│   └── Fundo de Compensação de Benefícios Fiscais
│
├── Módulo 4
│   └── Cadastro
│
├── Módulo 5
│   └── Obrigações Acessórias
│
├── Módulo 6
│   └── Apuração Assistida da CBS
│
├── Módulo 7
│   └── Compensação, Ressarcimento, Restituição e Transferências
│
├── Módulo 8
│   └── Simples Nacional e MEI
│
├── Módulo 9
│   └── Economia Digital
│
├── Módulo 10
│   └── Regimes Específicos e Diferenciados
│
└── Módulo 11
    └── Planos de Assistência à Saúde e Concursos de Prognóstico
```

A organização temática é complementada pelos metadados documentais, permitindo recuperar não apenas o conteúdo, mas também seu contexto, origem e localização.

---

## 1️⃣5️⃣🏛️ Governança documental

A base de conhecimento foi projetada considerando que documentos relacionados à Reforma Tributária podem ser atualizados ao longo do tempo.

Por isso, cada documento deverá possuir informações que permitam identificar:

- sua instituição de origem;
- sua versão ou data de atualização;
- sua data de acesso;
- seu endereço oficial;
- seu módulo e tema;
- seu status na base;
- sua relação com os demais documentos.

### Objetivos da governança

```text
📋 Identificação
      ↓
🏷️ Classificação
      ↓
🔎 Rastreabilidade
      ↓
🔄 Atualização
      ↓
🗄️ Controle da base
      ↓
🤖 Respostas mais confiáveis
```

---
## 1️⃣6️⃣ 🔄 Atualização da base documental

Como os materiais oficiais podem receber atualizações durante a implementação da Reforma Tributária, o projeto deverá considerar a **data de publicação ou última modificação do documento** como parte dos metadados da base.

No momento da inclusão dos documentos, serão registrados, sempre que disponíveis:

```text
Fonte
Módulo
Título
Tema
Data de atualização
URL oficial
Página
Tipo de documento
```

Essa abordagem permite identificar a versão do conteúdo utilizada pelo agente e facilita futuras atualizações da base de conhecimento.

---


## 1️⃣7️⃣ Formato inicial

O MVP será inicialmente desenvolvido para trabalhar com documentos em:

```text
PDF
```

A arquitetura será preparada para permitir a expansão futura para outros formatos:

```text
PDF
DOCX
XLSX
PPTX
Markdown
CSV
JSON
HTML
```

A ideia é permitir que diferentes formatos possam passar por uma camada de normalização antes de serem incorporados à base de conhecimento.

---

## 1️⃣8️⃣🗂️ Metadados dos documentos

Além do conteúdo textual, os documentos serão associados a metadados para melhorar a recuperação e a rastreabilidade das respostas.

Exemplo:

```text
document_id
fonte
instituicao
nome_documento
tipo_documento
modulo
categoria
tema
data_publicacao
data_atualizacao
data_acesso
pagina
url_origem
status_documento
```

### Exemplo de metadados

```json
{
  "document_id": "RFB-CFC-M01-P01",
  "instituicao": "Receita Federal / CFC",
  "modulo": "Módulo 1",
  "categoria": "Normas Gerais",
  "tipo_documento": "PDF",
  "data_atualizacao": "2026-07-29",
  "pagina": 15,
  "status_documento": "selecionado"
}
```

Esses metadados acompanham os fragmentos durante o processo de recuperação e podem ser utilizados para apresentar a origem do conteúdo ao usuário.

---

## 1️⃣9️⃣🔄 Pipeline de ingestão

O processo de preparação dos documentos seguirá, inicialmente, o seguinte fluxo:

```text
📄 PDF
   ↓
📥 Carregamento
   ↓
📝 Extração de texto
   ↓
✂️ Chunking
   ↓
🧮 Geração de embeddings
   ↓
🗄️ Armazenamento vetorial
   ↓
🔎 Recuperação semântica
```

O objetivo é transformar documentos extensos em unidades menores de conhecimento que possam ser recuperadas de acordo com a pergunta realizada pelo usuário.

---

## 2️⃣0️⃣🤖 Pipeline do agente

Durante a interação:

```text
Pergunta do usuário
        ↓
Análise da pergunta
        ↓
Busca na base de conhecimento
        ↓
Recuperação dos trechos relevantes
        ↓
Construção do contexto
        ↓
LLM
        ↓
Resposta
        ↓
Referências / fontes
```

---
## 2️⃣1️⃣🔗 Fluxo completo de dados

O projeto pode ser dividido em dois fluxos principais:

### 📥 Ingestão

```text
Fonte oficial
    ↓
Documento
    ↓
Catálogo documental
    ↓
Curadoria
    ↓
Extração
    ↓
Chunking
    ↓
Metadados
    ↓
Embeddings
    ↓
Vector Store
```
---

## 2️⃣2️⃣💬 Exemplos de perguntas

O usuário poderá realizar perguntas como:

> **O que muda com a Reforma Tributária?**

> **Quais são os principais impactos da Reforma Tributária para a Contabilidade?**

> **Como funciona a transição para o novo modelo tributário?**

> **O que é o IBS?**

> **O que é a CBS?**

> **Quais são as principais obrigações acessórias relacionadas à Reforma Tributária?**

> **Quais são os principais pontos de atenção para os profissionais de Contabilidade?**

> **Como funciona a apuração assistida da CBS?**

> **Como funcionam os mecanismos de compensação, ressarcimento e restituição?**

> **Quais são as mudanças relacionadas ao Simples Nacional?**

> **Como a Reforma Tributária impacta a economia digital?**

---

## 2️⃣3️⃣📚 Respostas fundamentadas

Um dos principais objetivos do projeto é permitir que o usuário não receba apenas uma resposta gerada pela IA.

A resposta deverá, sempre que possível, estar acompanhada das referências utilizadas.

Exemplo conceitual:

```text
💬 Pergunta:

Quais são as principais mudanças para 2026?

🤖 Resposta:

[Resposta gerada pelo agente com base nos documentos recuperados.]

📚 Fontes consultadas:

• Receita Federal
• Documento: [nome do documento]
• Módulo: [número do módulo]
• Página: XX
• URL: [fonte oficial]
```

Essa abordagem busca aumentar a **transparência, rastreabilidade e confiabilidade** das respostas.

---

## 2️⃣4️⃣🛡️ Confiabilidade e controle de respostas

O agente deverá priorizar informações presentes na base documental disponibilizada.

Quando não houver informações suficientes para responder determinada pergunta, o comportamento esperado será informar ao usuário que não foram encontrados elementos suficientes na base de conhecimento.

Exemplo:

> ⚠️ Não foram encontradas informações suficientes nos documentos disponíveis para responder a essa pergunta com segurança.

Essa estratégia busca reduzir respostas sem fundamentação documental e minimizar o risco de geração de informações não suportadas pelas fontes.

---

## 2️⃣5️⃣🧩 Estratégia de redução de alucinações

O agente foi projetado para priorizar respostas sustentadas pelos documentos recuperados na base de conhecimento.

O fluxo esperado é:

```text
Pergunta
   ↓
Recuperação de documentos
   ↓
Avaliação da relevância
   ↓
Contexto disponível?
   │
   ├── NÃO → Informar ausência de evidência suficiente
   │
   └── SIM
         ↓
       LLM
         ↓
   Resposta fundamentada
         ↓
      Referências
```
Quando o contexto recuperado não apresentar evidências suficientes, o agente deverá evitar completar a resposta com informações não presentes na base documental.

---

## 2️⃣6️⃣🏗️ Arquitetura do projeto

A arquitetura proposta é:

```text
┌───────────────────────┐
│       Usuário         │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│   Interface Web       │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│      Agente IA        │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│       Retriever       │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│    Banco Vetorial     │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│  Base de Conhecimento │
│      RFB / CFC        │
└───────────────────────┘
```

---

## 2️⃣7️⃣🧰 Tecnologias

As tecnologias serão definidas e evoluídas durante a implementação do projeto.

A stack prevista inclui:

| Tecnologia                            | Finalidade                             |
| ------------------------------------- | -------------------------------------- |
| **Python**                            | Desenvolvimento da aplicação           |
| **LangChain**                         | Construção do pipeline de RAG          |
| **LangGraph**                         | Orquestração do agente                 |
| **LLM**                               | Interpretação e geração das respostas  |
| **Embeddings**                        | Representação semântica dos documentos |
| **Vector Store**                      | Armazenamento e recuperação semântica  |
| **PDF Loader**                        | Extração dos documentos                |
| **Streamlit**                         | Interface web                          |
| **GitHub**                            | Versionamento e colaboração            |
| **Oracle Cloud Infrastructure (OCI)** | Deploy da solução                      |

> A definição final dos modelos, banco vetorial e serviços específicos da OCI será realizada durante a implementação e validação da arquitetura.

---

## 2️⃣8️⃣📊 Avaliação do agente

A qualidade do agente será avaliada por meio de um conjunto de perguntas de teste.

Os testes deverão contemplar diferentes cenários:

| Cenário                                   | Objetivo                        |
| ----------------------------------------- | ------------------------------- |
| Pergunta direta                           | Avaliar recuperação simples     |
| Pergunta conceitual                       | Avaliar compreensão             |
| Pergunta específica                       | Avaliar precisão                |
| Pergunta envolvendo diferentes documentos | Avaliar recuperação múltipla    |
| Pergunta sem resposta na base             | Avaliar controle de alucinação  |
| Pergunta fora do escopo                   | Avaliar comportamento do agente |
| Pergunta com termos técnicos              | Avaliar recuperação semântica   |
| Pergunta solicitando fonte                | Avaliar rastreabilidade         |

A avaliação permitirá identificar oportunidades de melhoria no processo de ingestão, chunking, recuperação e geração das respostas.

## 2️⃣9️⃣📏 Métricas - Critérios de avaliação

A avaliação poderá considerar diferentes dimensões:

| Métrica | Objetivo |
|---|---|
| Relevância da recuperação | Verificar se os trechos recuperados respondem à pergunta |
| Precisão da resposta | Avaliar se a resposta está correta em relação ao contexto |
| Fidelidade ao contexto | Verificar se a resposta é suportada pelos documentos |
| Cobertura das fontes | Avaliar se documentos relevantes foram recuperados |
| Taxa de respostas sem evidência | Identificar situações de possível alucinação |
| Rastreabilidade | Verificar se a origem da informação pode ser identificada |

O conjunto de avaliação deverá conter perguntas com respostas conhecidas, perguntas que exigem múltiplos documentos e perguntas para as quais não existe evidência suficiente na base.

---

## 3️⃣0️⃣☁️ Deploy na Oracle Cloud Infrastructure

O projeto será disponibilizado na **Oracle Cloud Infrastructure (OCI)**, atendendo ao requisito de utilização de pelo menos um serviço OCI.

Fluxo esperado:

```text
GitHub
   ↓
Aplicação
   ↓
Oracle Cloud Infrastructure
   ↓
Deploy
   ↓
🌐 Agente disponível online
```

O projeto utilizará a **Oracle Cloud Infrastructure (OCI)** como ambiente de execução da solução.

O serviço OCI selecionado, sua configuração e arquitetura de deployment serão documentados nesta seção após a implementação.

---

## 3️⃣1️⃣🎥 Demonstração

## Agente funcionando em nuvem

> 📌 **Em construção**

Após o deploy na OCI, será adicionada aqui uma demonstração do agente funcionando em ambiente online.

### Screenshot

```text
[ INSERIR IMAGEM DO AGENTE FUNCIONANDO NA OCI ]
```

### Vídeo

```text
[ INSERIR LINK DO VÍDEO / GIF DE DEMONSTRAÇÃO ]
```

---

## 3️⃣2️⃣📁 Estrutura do projeto

Estrutura inicial proposta:

```text
reforma-tributaria-ai-agent/
│
├── app/
│   ├── app.py
│   ├── agent.py
│   ├── rag.py
│   └── prompts.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── catalog/
│   └── catalogo_documental.csv
│
├── ingestion/
│   ├── loaders/
│   │   └── pdf_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   └── metadata.py
│
├── vectorstore/
│
├── evaluation/
│   ├── questions.json
│   └── evaluation.py
│
├── notebooks/
│   └── exploracao_rag.ipynb
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

A estrutura poderá ser ajustada conforme a evolução da arquitetura.

---

## 3️⃣3️⃣🚀 Como executar localmente

## 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/reforma-tributaria-ai-agent.git
```

## 2. Acessar o projeto

```bash
cd reforma-tributaria-ai-agent
```

## 3. Criar ambiente virtual

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

## 4. Instalar dependências

```bash
pip install -r requirements.txt
```

## 5. Configurar variáveis de ambiente

Criar um arquivo:

```text
.env
```

Exemplo:

```text
LLM_API_KEY=sua_chave
```

> Nunca publique chaves de API, senhas ou credenciais no GitHub.

## 6. Executar a aplicação

```bash
streamlit run app/app.py
```


---


## 3️⃣4️⃣🗺️ Roadmap

### 🟢 Etapa 1 — Definição e coleta inicial

- [x] Definição do problema
- [x] Definição do público-alvo
- [x] Definição da abordagem RAG
- [x] Definição das fontes iniciais
- [x] Identificação dos documentos oficiais
- [x] Organização inicial dos documentos por módulo
- [x] Criação do catálogo documental
- [x] Registro da instituição responsável pela publicação
- [x] Registro da última modificação informada pela fonte oficial
- [x] Registro da data de acesso
- [x] Registro do status de cada documento
- [x] Definição da arquitetura proposta

### 🟡 Etapa 2 — Base de conhecimento

* [ ] Seleção definitiva dos documentos
* [ ] Download e organização dos PDFs
* [ ] Extração de texto
* [ ] Tratamento dos documentos
* [ ] Criação dos metadados
* [ ] Chunking
* [ ] Geração dos embeddings
* [ ] Implementação do banco vetorial

### 🟡 Etapa 3 — Agente

* [ ] Implementação do Retriever
* [ ] Implementação do prompt
* [ ] Integração com LLM
* [ ] Implementação do agente
* [ ] Controle de respostas sem evidência
* [ ] Apresentação das fontes
* [ ] Referência por documento e página

### 🟡 Etapa 4 — Interface

* [ ] Desenvolvimento da interface
* [ ] Campo de perguntas
* [ ] Exibição das respostas
* [ ] Exibição das fontes
* [ ] Melhorias de UX

### 🟠 Etapa 5 — Avaliação

* [ ] Criação do conjunto de perguntas
* [ ] Testes de recuperação
* [ ] Testes de respostas
* [ ] Testes de perguntas fora do escopo
* [ ] Avaliação de alucinação
* [ ] Avaliação das fontes recuperadas
* [ ] Ajustes no RAG

### 🔵 Etapa 6 — Cloud

* [ ] Configuração da OCI
* [ ] Deploy
* [ ] Testes em ambiente cloud
* [ ] Disponibilização online
* [ ] Registro da demonstração
* [ ] Atualização do README

---

## 3️⃣5️⃣🔐 Segurança

O projeto deverá seguir boas práticas de segurança, incluindo:

* Não versionar chaves de API;
* Utilizar variáveis de ambiente;
* Não armazenar credenciais no código;
* Utilizar `.gitignore`;
* Avaliar cuidadosamente os documentos incorporados à base;
* Manter identificadas as fontes utilizadas;
* Evitar respostas não fundamentadas nos documentos disponíveis.

---

## 3️⃣6️⃣⚠️ Limitações

O agente não substitui a análise de profissionais habilitados nem constitui, por si só, orientação ou parecer contábil, fiscal ou jurídico.

As respostas dependem da qualidade, atualização e abrangência dos documentos incorporados à base de conhecimento.

Como a Reforma Tributária está em processo de implementação, documentos e orientações oficiais podem ser atualizados.

Por isso, a base documental deverá possuir mecanismos de atualização e identificação da origem dos conteúdos.

> **Atenção:** as respostas geradas pelo agente devem ser utilizadas como apoio à consulta e capacitação, sendo recomendada a validação da informação diretamente na fonte oficial e, quando necessário, junto a profissionais habilitados.

---

## 3️⃣7️⃣🌱 Possíveis evoluções

Após a implementação do MVP, o projeto poderá evoluir para:

* Suporte a múltiplos formatos de documentos;
* Busca híbrida;
* Re-ranking dos resultados;
* Memória conversacional;
* Agentes especializados por tema;
* Comparação entre documentos;
* Respostas com citações por página;
* Dashboard de utilização;
* Avaliação automática das respostas;
* Atualização automatizada da base documental;
* Monitoramento do agente em produção;
* Expansão para outros temas contábeis e tributários;
* Inclusão de documentos adicionais do CFC;
* Inclusão de documentos da Fenacon;
* Controle de versões dos documentos;
* Atualização periódica da base de conhecimento.

---

## 3️⃣8️⃣📚 Referências institucionais

### Receita Federal do Brasil

**Curso Reforma Tributária RFB e CFC — Módulos do Curso**

[📖 Acessar página oficial dos módulos](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso)

### Conselho Federal de Contabilidade — CFC

Materiais institucionais relacionados à capacitação e atuação dos profissionais da Contabilidade poderão ser incorporados à base de conhecimento conforme a evolução do projeto.

### Fenacon

Materiais institucionais relacionados ao ambiente contábil, fiscal e empresarial poderão ser incorporados à base de conhecimento em etapas futuras.

---

## 3️⃣9️⃣👩‍💻 Equipe

| Integrante | Atuação |
|---|---|
| **Kelly Costa** | IA / RAG • Desenvolvimento • Dados • Cloud / OCI |

---

## 4️⃣0️⃣📄 Licença

Este projeto será disponibilizado para fins de estudo, demonstração e desenvolvimento tecnológico.

A licença definitiva será definida pela equipe durante a publicação do projeto.

---

## 4️⃣1️⃣⭐ Contribuição

Sugestões, melhorias e contribuições são bem-vindas.

Caso encontre algum problema ou tenha uma sugestão para evolução do projeto, abra uma **Issue** ou envie um **Pull Request**.

---

<p align="center">


### Indice

1. 🤖 Título
2. Status
3. Sobre o projeto
4. ⭐ Diferencial
5. 🎯 Objetivo
6. 💡 Problema
7. 👥 Público-alvo
8. 🎯 Escopo do MVP
9. 🧠 Como funciona
10. 🔎 RAG
11. 📚 Fontes de conhecimento
12. 📋 Catálogo documental
13. 📑 Documentos utilizados
14. 📊 Organização temática
15. 🏛️ Governança documental
16. 🔄 Atualização da base
17. 📄 Formatos
18. 🗂️ Metadados
19. 📥 Pipeline de ingestão
20. 📤 Pipeline do agente
21. 🔗 Fluxo completo de dados
22. 💬 Exemplos de perguntas
23. 📚 Respostas fundamentadas
24. 🛡️ Confiabilidade
25. 🧩 Controle de alucinação
26. 🏗️ Arquitetura
27. 🧰 Tecnologias
28. 📊 Avaliação
29. 📏 Métricas
30. ☁️ OCI
31. 🎥 Demonstração
32. 📁 Estrutura
33. 🚀 Execução local
34. 🗺️ Roadmap
35. 🔐 Segurança
36. ⚠️ Limitações
37. 🌱 Evoluções
38. 📚 Referências
39. 👩‍💻 Equipe
40. 📄 Licença
41. ⭐ Contribuição
  Desenvolvido com 🤖 Inteligência Artificial, RAG, Python e Oracle Cloud
</p>
