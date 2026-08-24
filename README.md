# 1️⃣ 🤖 Reforma Tributária AI Agent

> **Agente de Inteligência Artificial para consulta, capacitação e apoio à implementação da Reforma Tributária**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/AI-RAG-purple)]()
[![Tests](https://img.shields.io/badge/Tests-204%20passed-success)]()
[![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/)
[![Oracle Cloud](https://img.shields.io/badge/Cloud-Oracle%20Cloud-red?logo=oracle)](https://www.oracle.com/cloud/)

---
## Links
[http://localhost:8501](http://localhost:8501?utm_source=chatgpt.com)

  
## 2️⃣ 🚧 Status do projeto

**Status:** 🟡 Em desenvolvimento

O projeto encontra-se em fase de construção e validação de um pipeline de **RAG (Retrieval-Augmented Generation)** para consulta inteligente a documentos oficiais relacionados à **Reforma Tributária do Consumo**.

A primeira versão prioriza documentos em **formato PDF**, com foco em:

- Curadoria documental;
- Organização da base de conhecimento;
- Extração e normalização de conteúdo;
- Chunking;
- Geração de embeddings;
- Busca semântica;
- Recuperação Top-K;
- Filtros por metadados;
- Controle de similaridade;
- Montagem de contexto;
- Geração de respostas com LLM;
- Rastreabilidade das fontes;
- Avaliação automatizada;
- Controle de respostas sem evidência.


### 📌 Checkpoint atual

#### Concluído

✅ Pipeline de ingestão

✅ Extração, limpeza e chunking

✅ Metadados

✅ Embeddings

✅ Vector Store

✅ Retriever + Reranker

✅ Pipeline RAG

✅ Agent

✅ Abstração da camada LLM

✅ Interface Streamlit

✅ Estrutura `app` como pacote Python

✅ `Dockerfile`

✅ `.dockerignore`

✅ `google-genai` declarado no `requirements.txt`

✅ Build da imagem Docker

✅ Imagem Docker criada

✅ Container iniciado

✅ Uvicorn

✅ Streamlit

✅ Aplicação disponível na porta `8501`

✅ Integração com Gemini validada em ambiente Docker

✅ Fluxo funcional end-to-end validado

✅ Respostas fundamentadas com fontes e páginas

✅ GitHub Actions

✅ 204 testes automatizados aprovados

#### Em validação / Próximas etapas

⬜ Deploy na Oracle Cloud Infrastructure (OCI)

⬜ Validar aplicação publicada na OCI

✅ Deploy na Oracle Cloud Infrastructure (OCI)

✅ Container Instance criada

✅ Aplicação publicada

✅ Streamlit acessível externamente

✅ Integração Gemini validada em produção

✅ RAG validado end-to-end na OCI

### 📊 Validação técnica

| Etapa                                | Status |
| ------------------------------------ | :----: |
| 204 testes automatizados             |    ✅   |
| GitHub Actions                       |    ✅   |
| `google-genai` configurado           |    ✅   |
| Docker build                         |    ✅   |
| Docker image                         |    ✅   |
| Container iniciado                   |    ✅   |
| Uvicorn                              |    ✅   |
| Streamlit                            |    ✅   |
| Porta 8501                           |    ✅   |
| Integração Gemini                    |    ✅   |
| RAG end-to-end                       |    ✅   |
| Respostas com evidências documentais |    ✅   |

| Item                  | Status           |
| --------------------- | ---------------- |
| Container Instance    | ✅                |
| `CI.Standard.E4.Flex` | ✅                |
| 1 OCPU                | ✅                |
| 16 GB RAM             | ✅                |
| Restart `Always`      | ✅                |
| VCN correta           | ✅                |
| Subnet pública        | ✅                |
| Public IP             | ✅                |
| NSG                   | ✅ Não necessário |
| Storage               | ✅ Nenhum         |
| Imagem Docker Hub     | ✅                |
| Tag `latest`          | ✅                |
| Command sobrescrito   | ✅ Não            |
| Command arguments     | ✅ Vazio          |
| Streamlit na imagem   | ✅ Porta 8501     |



### 🔄 Próximas etapas
☁️ Deploy da aplicação na Oracle Cloud Infrastructure (OCI);
🔗 Validação da aplicação publicada;
🔐 Configuração segura das variáveis de ambiente;
📦 Validação do container no ambiente de nuvem.


#### ⚠️ Evoluções futuras

Itens planejados para uma segunda etapa, após a entrega inicial:

Reranking avançado;
Oracle Autonomous Database / Vector Search;
Integração com Microsoft Teams;
Integração com Slack;
CI/CD avançado;
Observabilidade e monitoramento;
Atualização automática da base documental;
Suporte ampliado a múltiplos formatos;
Arquitetura distribuída;
Fine-tuning;
Melhorias adicionais de UX/UI.

### 📊 Indicadores atuais


| Indicador | Resultado |
|---|---:|
| 📄 PDFs processados | **34** |
| ✂️ Chunks criados | **1.302** |
| 🗄️ Registros no Vector Store | **1.302** |
| 📋 `index.json` | ✅ Criado |
| 🧠 Embeddings | ✅ Gerados |
| 🗄️ Vector Store | ✅ Persistido |
| 🧪 Testes automatizados | **204 aprovados** |
| 📊 Perguntas de avaliação RAG | **7** |
| 📚 Recuperação de documento esperado | **100%** |
| 🏛️ Recuperação da fonte esperada | **100%** |
| 📄 Recuperação da página esperada | **100%** |
| 🎯 Cobertura média dos tópicos | **91,2%** |

---

## 3️⃣ 📌 Sobre o projeto

O **Reforma Tributária AI Agent** é um agente de Inteligência Artificial desenvolvido para facilitar a **consulta, compreensão e capacitação** sobre a **Reforma Tributária do Consumo**.

A solução utiliza **RAG (Retrieval-Augmented Generation)** para transformar documentos oficiais e institucionais em uma **base de conhecimento estruturada e consultável por linguagem natural**.

Por meio de uma interface conversacional, o usuário pode realizar perguntas sobre temas relacionados à Reforma Tributária. O sistema recupera os trechos mais relevantes da base documental e utiliza esse contexto para gerar respostas fundamentadas, mantendo a **rastreabilidade por meio dos metadados, documentos e páginas recuperadas**.

O projeto foi concebido com foco em:

- 📚 Curadoria e organização documental;
- 🏛️ Governança da informação;
- 🔎 Recuperação semântica;
- 🧠 Geração de respostas contextualizadas;
- 🔗 Rastreabilidade das fontes;
- 🛡️ Controle de evidências;
- 🧪 Avaliação da qualidade da recuperação e das respostas.

---

# 4️⃣ ⭐ Diferencial do projeto

O principal diferencial da solução está na **construção, organização e governança da base de conhecimento**.

Os documentos não são simplesmente baixados e enviados para um modelo de linguagem. Antes de serem utilizados pelo agente, eles passam por um **pipeline estruturado de preparação documental**, garantindo maior qualidade na recuperação das informações e rastreabilidade das fontes.

### 🔄 Pipeline de construção da base

```text
Fontes oficiais
      ↓
Seleção
      ↓
Curadoria
      ↓
Catalogação
      ↓
Organização
      ↓
Extração
      ↓
Limpeza e normalização
      ↓
Enriquecimento com metadados
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Store
      ↓
Retriever + Reranker
      ↓
Contexto para o RAG
```

### 🗂️ Metadados documentais

* Instituição responsável;
* Módulo;
* Tema;
* Título;
* Data de publicação;
* Data de atualização;
* Data de acesso;
* URL oficial;
* Tipo de documento;
* Status de curadoria;
* Página;
* Seção;
* Identificador documental.

Essa abordagem permite construir uma base documental estruturada e preparada para recuperação semântica e rastreabilidade.

---

# 5️⃣ 🎯 Objetivo

Desenvolver um agente de IA capaz de:

🤖 Responder perguntas relacionadas à Reforma Tributária do Consumo;
📚 Apoiar a capacitação e consulta de profissionais da Contabilidade;
🔎 Facilitar a localização de informações em documentos técnicos e institucionais;
🗂️ Estruturar uma base de conhecimento documental;
🧠 Recuperar informações relevantes por busca semântica;
💬 Gerar respostas contextualizadas a partir das evidências recuperadas;
🔗 Apresentar as fontes utilizadas na resposta;
📄 Identificar documento e página de referência;
🛡️ Controlar respostas quando não houver evidências suficientes na base;
⏱️ Reduzir o tempo necessário para localizar informações;
🖥️ Disponibilizar uma interface conversacional para consulta.
---

# 6️⃣ 💡 Problema

A Reforma Tributária envolve mudanças relevantes na estrutura tributária brasileira e demanda atualização contínua por parte dos profissionais de Contabilidade.

As informações podem estar distribuídas em diferentes:

📄 Documentos oficiais;
📚 Materiais técnicos;
🏛️ Orientações institucionais;
📑 Publicações;
⚖️ Atos normativos e regulamentações.

A dispersão dessas informações pode tornar a busca manual demorada, dificultando a localização rápida de conteúdos específicos e a identificação da fonte correspondente.

Nesse cenário, o projeto propõe uma camada conversacional sobre uma base documental estruturada.

Em vez de realizar buscas manuais em diversos documentos, o usuário pode formular uma pergunta em linguagem natural. O agente então realiza a recuperação dos conteúdos mais relevantes na base de conhecimento e utiliza essas evidências para construir uma resposta contextualizada, acompanhada das respectivas referências documentais.

### 🎯 Em síntese

Busca manual em múltiplos documentos
                ↓
       Pergunta em linguagem natural
                ↓
      Recuperação semântica + Reranking
                ↓
       Contexto documental relevante
                ↓
           Agente de IA + LLM
                ↓
       Resposta fundamentada
                ↓
       Documento + página + fonte

---

# 7️⃣ 👥 Público-alvo

O Reforma Tributária AI Agent foi concebido para apoiar diferentes perfis de usuários que precisam consultar, compreender ou estudar informações relacionadas à Reforma Tributária do Consumo.

Principais públicos:
* Contadores;
* Profissionais da área contábil;
* Equipes fiscais e tributárias;
* Profissionais envolvidos na implementação da Reforma Tributária;
* Estudantes;
* Profissionais que desejam compreender o tema;
* Usuários interessados em consultar informações sobre a Reforma Tributária.

O agente foi projetado para acesso aberto, sem restrição a um grupo específico de usuários, permitindo sua utilização como ferramenta de consulta e capacitação.
---

# 8️⃣ 🎯 Escopo do MVP

O MVP concentra-se na construção de uma base documental estruturada e pesquisável, utilizando documentos oficiais e institucionais relacionados à Reforma Tributária do Consumo.

* Documentos em formato PDF;
* Materiais oficiais relacionados à Reforma Tributária do Consumo;
* Fontes inicialmente concentradas em RFB e CFC;
* Curadoria e catalogação documental;
* Ingestão e processamento dos documentos;
* Extração, limpeza e normalização do conteúdo;
* Enriquecimento com metadados;
* Chunking;
* Geração de embeddings;
* Persistência em Vector Store;
* Recuperação semântica;
* Recuperação Top-K;
* Filtros por metadados;
* Controle de similaridade;
* Reranking;
* Montagem de contexto;
* Geração de respostas utilizando LLM;
* Controle de evidências;
* Rastreabilidade das fontes;
* Identificação de documento e página;
* Interface conversacional com Streamlit;
* Empacotamento da aplicação em Docker

Evolução planejada

Após a validação do MVP, estão previstas evoluções como:

* Deploy na Oracle Cloud Infrastructure (OCI);
* Ampliação para novos formatos documentais;
* Integração com plataformas corporativas;
* Observabilidade avançada;
* Atualização automatizada da base documental;
* Evolução da infraestrutura de armazenamento e busca vetorial.

Nota: essas funcionalidades representam a evolução planejada da solução e não fazem parte necessariamente da versão atual do MVP.

---

# 9️⃣ 🧠 Arquitetura da solução

```text
                    REFORMA TRIBUTÁRIA AI AGENT
                              │
                              ▼
                    🖥️ Interface Streamlit
                              │
                              ▼
                    ❓ Pergunta do usuário
                              │
                              ▼
                         🤖 Agent
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
             🔎 Retriever              🧠 Gemini
                  │                       │
                  ▼                       │
            🗄️ Vector Store               │
                  │                       │
                  ▼                       │
          📑 Contexto relevante ─────────┘
                              │
                              ▼
                       💬 Resposta
                              │
                              ▼
                     📚 Fontes + páginas
```

---
Fluxo simplificado
* O usuário envia uma pergunta pela interface;
* O Agent interpreta a solicitação;
* O Retriever consulta a base vetorial;
* Os documentos/chunks mais relevantes são recuperados;
* Metadados e critérios de similaridade auxiliam na seleção das evidências;
* O contexto recuperado é enviado à camada de LLM;
* A resposta é gerada com base no contexto disponível;
* As fontes e páginas utilizadas são apresentadas para permitir rastreabilidade.

Essa arquitetura reduz a dependência de conhecimento exclusivamente armazenado nos parâmetros do modelo, utilizando a base documental como fonte de evidência para as respostas.
---

# 🔟 🔎 Pipeline RAG

O fluxo completo da solução é:

```text
🏛️ Fontes oficiais
        ↓
📋 Catálogo documental
        ↓
🔎 Curadoria
        ↓
📄 Ingestão
        ↓
📖 Extração
        ↓
🧹 Cleaning
        ↓
🏷️ Metadados
        ↓
✂️ Chunking
        ↓
🧮 Embeddings
        ↓
🗄️ Vector Store
        ↓
🔍 Retriever
        ↓
🏷️ Filtros
        ↓
📊 Controle de similaridade
        ↓
📝 Montagem do contexto
        ↓
🔄 Reranking
        ↓
🧠 LLM
        ↓
💬 Resposta fundamentada
        ↓
📚 Fonte + página
```

---
🔬 Princípio de funcionamento

O pipeline não envia os documentos integralmente para o modelo de linguagem.

Em vez disso, os documentos são:

curados → processados → fragmentados → vetorizados → indexados → recuperados

Durante uma consulta, somente os trechos mais relevantes são utilizados para construir o contexto da resposta.

Isso permite:

* reduzir o volume de informação enviado à LLM;
* melhorar a relevância do contexto;
* preservar a origem das informações;
* identificar documento e página;
* reduzir respostas sem evidência;
* facilitar a avaliação da qualidade da recuperação.
---

# 1️⃣1️⃣ 📚 Base documental

A primeira versão utiliza documentos oficiais relacionados à Reforma Tributária do Consumo.

As principais fontes consideradas são:

* **Receita Federal do Brasil (RFB)**
* **Conselho Federal de Contabilidade (CFC)**
* **Fenacon**

Os documentos inicialmente selecionados para o MVP são materiais oficiais do **Curso Reforma Tributária RFB e CFC**, disponibilizados no portal da Receita Federal.

### Fonte oficial

[Material de apoio — Reforma Tributária do Consumo — Receita Federal](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/curso/material-de-apoio/modulos-do-curso)

---

# 1️⃣2️⃣ 📋 Catálogo documental

O projeto possui uma camada específica de catalogação documental.

O catálogo tem como objetivo garantir:

* Identificação dos documentos;
* Origem institucional;
* Organização por módulo;
* Identificação das partes;
* Controle de duplicidades;
* Rastreabilidade;
* Governança documental.

Exemplo conceitual:

```text
Documento
    │
    ├── ID
    ├── Instituição
    ├── Módulo
    ├── Título
    ├── Arquivo
    ├── Tipo
    ├── Data de publicação
    ├── Data de atualização
    ├── Data de acesso
    ├── URL oficial
    └── Status de curadoria
```

---

# 1️⃣3️⃣ ⚙️ Processamento documental

O processamento dos documentos segue o pipeline:

```text
📄 PDF
   ↓
📥 Ingestion
   ↓
📖 Extraction
   ↓
🧹 Cleaning
   ↓
🏷️ Metadata
   ↓
✂️ Chunking
   ↓
🧪 Quality Validation
   ↓
🧮 Embeddings
   ↓
🗄️ Vector Store
```

### Extração

A etapa de extração realiza:

* Leitura dos documentos PDF;
* Extração de texto por página;
* Preservação da numeração das páginas;
* Validação do conteúdo;
* Tratamento de arquivos inválidos.

### Cleaning

A limpeza contempla:

* Normalização de espaços;
* Remoção de ruídos;
* Remoção de elementos repetitivos;
* Tratamento da numeração de páginas;
* Preservação de números relevantes;
* Validação da qualidade do texto.

### Chunking

Os documentos são divididos em unidades menores para permitir recuperação semântica mais eficiente.

São considerados:

* Tamanho dos chunks;
* Overlap;
* Página de origem;
* Documento;
* Identificadores únicos;
* Metadados.

---

# 1️⃣4️⃣ 🧬 Embeddings

O projeto utiliza o modelo:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

A escolha considera que:

* O projeto está em português;
* Os documentos são predominantemente em português;
* O conteúdo possui vocabulário técnico;
* A recuperação depende da similaridade semântica.

O módulo de embeddings é responsável por:

```text
Texto
  ↓
Modelo de Embedding
  ↓
Vetor
```

Também suporta:

```text
Vários chunks
      ↓
Embeddings
      ↓
Matriz de vetores
```

Os vetores são normalizados para facilitar operações de similaridade.

---

# 1️⃣5️⃣ 🗄️ Vector Store

O Vector Store é responsável pelo armazenamento e recuperação dos embeddings.

```text
Chunks
  ↓
Embeddings
  ↓
Vector Store
  ↓
Busca por similaridade
  ↓
Resultados Top-K
```

O projeto implementa:

* Persistência dos embeddings;
* Carregamento do índice;
* Busca por similaridade;
* Similaridade de cosseno;
* Ranking dos resultados;
* Preservação dos metadados.

Atualmente:

```text
PDFs processados:       34
Chunks:              1.302
Vetores:             1.302
```

---

# 1️⃣6️⃣ 🔍 Retriever

O Retriever recebe a pergunta do usuário e realiza a recuperação semântica.

```text
Pergunta
   ↓
Query Embedding
   ↓
Vector Store
   ↓
Busca semântica
   ↓
Top-K
   ↓
Filtros
   ↓
Controle de similaridade
   ↓
Chunks relevantes
```

O Retriever suporta filtros por:

* Organização;
* Módulo;
* Documento.

Também preserva:

* Documento;
* Página;
* Seção;
* Instituição;
* Conteúdo;
* Similaridade.

---

# 1️⃣7️⃣ 📊 Controle de similaridade

Foi implementado um controle mínimo de similaridade para reduzir a entrada de resultados pouco relacionados à pergunta.

Exemplo atual:

```python
MIN_SIMILARITY = 0.55
```

Somente resultados que atendem ao limiar mínimo são utilizados na montagem do contexto.

```text
Pergunta
   ↓
Retriever
   ↓
Top-K
   ↓
Similaridade
   ↓
┌──────────────────────┐
│ similarity >= 0.55   │
└──────────────────────┘
   ↓
Contexto
```

Essa camada contribui para reduzir a recuperação de trechos semanticamente fracos.

---

# 1️⃣8️⃣ 📝 Montagem do contexto

Após a recuperação, os chunks são organizados em um contexto estruturado.

Cada fonte preserva informações como:

```text
[Fonte 1]

Documento: ...
Instituição: ...
Página: ...
Seção: ...

Conteúdo:
...
```

Isso permite que o LLM receba não apenas o conteúdo recuperado, mas também informações necessárias para rastreabilidade.

---

# 1️⃣9️⃣ 🧠 LLM

O projeto possui uma abstração para o modelo de linguagem:

```text
BaseLLM
   │
   ├── FakeLLM
   │
   └── Gemini
```

Essa arquitetura permite separar:

* Pipeline RAG;
* Prompt;
* Modelo de linguagem;
* Testes;
* Integração com provedores externos.

O `FakeLLM` permite validar o fluxo sem depender de uma API externa.

O ambiente de desenvolvimento também possui integração com o **Gemini** para geração de respostas reais.

---

# 2️⃣0️⃣ 🔄 Fluxo RAG → LLM

```text
Pergunta do usuário
        ↓
Query Embedding
        ↓
Retriever
        ↓
Top-K
        ↓
Filtros
        ↓
Limiar de similaridade
        ↓
Contexto relevante
        ↓
Prompt
        ↓
LLM
        ↓
Resposta
        ↓
Fontes + páginas
```

---

# 2️⃣1️⃣ 🛡️ Controle de evidências

O agente foi projetado para evitar respostas baseadas apenas no conhecimento geral do modelo.

Quando não existe contexto suficiente, o pipeline pode utilizar um fallback.

```text
Pergunta
   ↓
Recuperação
   ↓
Existem evidências?
   │
   ├── SIM → Contexto → LLM → Resposta
   │
   └── NÃO → Fallback
```

Esse mecanismo é importante principalmente para perguntas fora do escopo documental.

---

# 2️⃣2️⃣ 🧪 Validação do RAG

O pipeline RAG foi submetido a um conjunto inicial de **7 perguntas de avaliação**, cobrindo diferentes tipos de consulta:

* Factual;
* Conceitual;
* Procedural;
* Jurídica;
* Perguntas sem evidência suficiente na base.

### Resultados

| Métrica                       | Resultado |
| ----------------------------- | --------: |
| Perguntas avaliadas           |     **7** |
| Respostas válidas             |  **100%** |
| Documento esperado recuperado |  **100%** |
| Fonte esperada recuperada     |  **100%** |
| Página esperada recuperada    |  **100%** |
| Cobertura média dos tópicos   | **91,2%** |

A avaliação também contempla perguntas sem evidência suficiente na base documental, permitindo verificar o comportamento de fallback.

---

# 2️⃣3️⃣ 🧪 Cobertura de testes

O projeto possui atualmente:

```text
204 testes automatizados aprovados
```

Resultado:

```text
204 passed
```

### Cobertura por camada

| Camada             | Status |
| ------------------ | :----: |
| 📄 Extraction      |    ✅   |
| 📥 Ingestion       |    ✅   |
| 🧹 Cleaning        |    ✅   |
| ✂️ Chunking        |    ✅   |
| 🏷️ Metadata        |    ✅   |
| 🧮 Embeddings      |    ✅   |
| 🗄️ Vector Store    |    ✅   |
| 🔎 Retriever       |    ✅   |
| Filtros            |    ✅   |
| 📝 Context Builder |    ✅   |
| 🤖 Agent           |    ✅   |
| 🧠 Prompt          |    ✅   |
| 🧠 LLM             |    ✅   |
| FakeLLM             |   ✅   |
| Gemini              |   ✅   |
| 🔄 RAG             |    ✅   |
| 🛡️ Fallback        |    ✅   |
| Fontes              |    ✅   |
| Testes              |    ✅ 204/204
| Avaliação RAG       |    ✅   |
| Interface           |    🚧   |
| Docker              |    🚧   |
| OCI                 |    🚧   |

### Resultado

```text
=============================
204 passed
=============================
```

A suíte cobre processamento documental, embeddings, Vector Store, recuperação semântica, Agent, prompts, LLM, RAG e mecanismos de fallback.

---

# 2️⃣4️⃣ 🔬 O que os testes validam

Os testes automatizados verificam:

* Processamento dos documentos;
* Extração do conteúdo;
* Limpeza e normalização;
* Geração dos chunks;
* Qualidade dos chunks;
* Preservação dos metadados;
* Geração dos embeddings;
* Normalização dos vetores;
* Persistência;
* Carregamento do Vector Store;
* Busca por similaridade;
* Ordenação dos resultados;
* Recuperação Top-K;
* Filtros por metadados;
* Montagem do contexto;
* Prompts;
* Agent;
* LLM;
* Fallback;
* Ausência de evidência;
* Integração entre as camadas do pipeline.

---

# 2️⃣5️⃣ 🏗️ Organização das etapas de desenvolvimento

## ETAPA 1 — Coleta e organização

### Fontes oficiais

* [x] Identificação das fontes oficiais
* [x] Receita Federal
* [x] Conselho Federal de Contabilidade
* [x] Fenacon
* [x] Seleção das fontes relevantes

### Coleta documental

* [x] Levantamento dos documentos
* [x] Download
* [x] Organização
* [x] Armazenamento
* [x] Padronização dos nomes

### Curadoria

* [x] Seleção dos documentos relevantes
* [x] Verificação da origem oficial
* [x] Identificação dos módulos
* [x] Identificação das partes
* [x] Verificação de duplicidades

### Catálogo

* [x] Catálogo CSV
* [x] Catálogo JSON
* [x] Identificação documental
* [x] Organização institucional
* [x] Registro das informações

### Governança

* [x] Critérios de inclusão
* [x] Critérios de curadoria
* [x] Padronização dos metadados
* [x] Rastreabilidade
* [x] Documentação da metodologia

---

# 2️⃣6️⃣ 📄 ETAPA 2 — Processamento e extração

### Extração

* [x] Ingestão PDF
* [x] PDF nativo
* [x] Extração por página
* [x] Preservação da numeração
* [x] Validação
* [x] Tratamento de arquivos inválidos

### Limpeza

* [x] Normalização de espaços
* [x] Remoção de ruídos
* [x] Tratamento da numeração
* [x] Preservação de números
* [x] Remoção de linhas repetidas
* [x] Validação da qualidade

### Chunking

* [x] Divisão em chunks
* [x] Controle de tamanho
* [x] Overlap
* [x] Chunking por página
* [x] IDs únicos
* [x] Validação

### Metadados

* [x] Documento
* [x] Nome
* [x] Tipo
* [x] Organização
* [x] Página
* [x] Seção
* [x] Metadados opcionais
* [x] Validação

### Formatos adicionais

* [ ] Word
* [ ] Excel
* [ ] PowerPoint
* [ ] Markdown
* [ ] CSV
* [ ] JSON
* [ ] HTML

---

# 2️⃣7️⃣ 🧮 ETAPA 3 — Indexação vetorial

### Embeddings

* [x] SentenceTransformer
* [x] Geração dos embeddings
* [x] Normalização
* [x] Preservação dos metadados

### Vector Store

* [x] Armazenamento
* [x] Persistência
* [x] Carregamento
* [x] Similaridade de cosseno
* [x] Ranking
* [x] Preservação dos metadados
* [x] Validações

---

# 2️⃣8️⃣ 🔎 ETAPA 4 — Recuperação RAG

### Query Embedding

* [x] Geração do embedding da consulta
* [x] Uso do mesmo modelo
* [x] Normalização

### Retriever

* [x] Consulta ao Vector Store
* [x] Busca por similaridade
* [x] Top-K
* [x] Ordenação
* [x] Preservação dos metadados

### Filtros

* [x] Organização
* [x] Módulo
* [x] Documento
* [x] Combinação de filtros

### Controle de similaridade

* [x] Definição do limiar mínimo
* [x] Filtragem dos resultados
* [x] Controle de contexto insuficiente

### Reranking

* [ ] Recuperação de candidatos
* [ ] Reordenação por relevância
* [ ] Seleção dos melhores resultados

### Contexto

* [x] Seleção dos chunks
* [x] Organização dos trechos
* [x] Metadados
* [x] Documento
* [x] Página
* [x] Seção
* [x] Construção do contexto

---

# 2️⃣9️⃣ 🧠 ETAPA 5 — Geração e validação

### LLM

* [x] Interface `BaseLLM`
* [x] `FakeLLM`
* [x] Integração com Gemini
* [x] Geração de respostas
* [x] Testes da integração

### Respostas

* [x] RAG → Prompt → LLM
* [x] Resposta baseada no contexto
* [x] Contexto insuficiente
* [x] Fallback

### Fontes

* [x] Preservação dos metadados
* [x] Documento
* [x] Página
* [x] Seção
* [x] Formatação das fontes
* [ ] Vinculação de cada afirmação à fonte específica

### Controle de alucinação

* [x] Validação da existência de contexto
* [x] Limiar mínimo de similaridade
* [x] Bloqueio quando não há evidência
* [ ] Verificação da resposta contra o contexto
* [ ] Detecção avançada de respostas sem evidência
* [ ] Regeneração/rejeição automática

---

# 3️⃣0️⃣ 🖥️ ETAPA 6 — Interface e experiência

### Interface

- [x] Interface web
- [x] Campo para perguntas
- [x] Exibição da resposta
- [x] Identidade visual
- [x] Exibição das fontes
- [x] Documento e página
- [x] Histórico
* [ ] Contexto da sessão
* [ ] Interface responsiva

### Experiência conversacional

- [x] Indicador de processamento
- [x] Histórico
- [x] Tratamento de erros
* [ ] Fallback visual
- [x] Nova pergunta na mesma sessão

### Feedback

* [ ] 👍 Avaliação positiva
* [ ] 👎 Avaliação negativa
* [ ] Registro do feedback
* [ ] Identificação da pergunta
* [ ] Identificação da resposta
* [ ] Análise dos feedbacks

---

# 3️⃣1️⃣ ☁️ ETAPA 7 — Deploy na OCI

A estratégia planejada de implantação utiliza:

```text
Streamlit
    ↓
Docker
    ↓
OCI Container Registry
    ↓
OCI Container Instance
    ↓
🌐 Streamlit público
```

### Preparação

* [ ] Validação local
* [ ] Validação da API
* [ ] Variáveis de ambiente
* [ ] Configuração de produção

### Containerização

* [ ] Dockerfile
* [ ] `.dockerignore`
* [ ] Imagem Docker
* [ ] Dependências
* [ ] Execução local
* [ ] Validação do container

### OCI Container Registry

* [ ] Criar repositório
* [ ] Autenticação
* [ ] Build da imagem
* [ ] Tag
* [ ] Push
* [ ] Validação

### OCI

* [ ] Configurar Container Instance
* [ ] CPU
* [ ] Memória
* [ ] Porta
* [ ] Variáveis de ambiente
* [ ] Deploy
* [ ] Validação


###🔥 O que NÃO fazer agora

❌ domínio próprio
❌ HTTPS customizado
❌ Load Balancer
❌ CI/CD
❌ Terraform
❌ Kubernetes
❌ monitoramento avançado
❌ feedback 👍/👎
❌ autenticação de usuários
❌ arquitetura de produção
❌ banco vetorial gerenciado na OCI
---

# 3️⃣2️⃣ 🔐 Segurança

Planejamento de segurança:

* [ ] Remover credenciais do código
* [x] Validar `.gitignore`
* [ ] Variáveis de ambiente
* [ ] OCI Vault
* [ ] IAM
* [ ] Políticas de acesso
* [ ] Validação das permissões

---

# 3️⃣3️⃣ 📚 Armazenamento documental em produção

Evolução planejada:

```text
Documentos
    ↓
OCI Object Storage
    ↓
Pipeline de ingestão
    ↓
Embeddings
    ↓
Vector Store
```

Itens planejados:

* [ ] Object Storage
* [ ] Bucket
* [ ] Organização documental
* [ ] Controle de acesso
* [ ] Upload
* [ ] Leitura
* [ ] Sincronização

---

# 3️⃣4️⃣ 🔄 Atualização da base documental

Planejamento para atualização automática:

```text
Fonte oficial
     ↓
Verificação
     ↓
Novo documento?
     │
     ├── SIM → Ingestão
     │          ↓
     │       Embeddings
     │          ↓
     │       Vector Store
     │
     └── NÃO → Manter índice
```

Funcionalidades planejadas:

* [ ] Identificação de novos documentos
* [ ] Identificação de documentos alterados
* [ ] Identificação de documentos removidos
* [ ] Reprocessamento
* [ ] Novos embeddings
* [ ] Atualização do Vector Store
* [ ] Remoção de conteúdo obsoleto
* [ ] Sincronização

---

# 3️⃣5️⃣ 📊 Monitoramento de qualidade

Indicadores planejados:

* [ ] Perguntas sem resposta
* [ ] Feedback negativo
* [ ] Tempo de resposta
* [ ] Qualidade da recuperação
* [ ] Qualidade das citações
* [ ] Falhas recorrentes
* [ ] Métricas de qualidade
* [ ] Faithfulness
* [ ] Answer Relevancy
* [ ] Context Precision
* [ ] Context Recall

---

# 3️⃣6️⃣ 🔄 CI/CD

Planejamento futuro:

```text
Git Push
   ↓
GitHub Actions
   ↓
Instalação das dependências
   ↓
Pytest
   ↓
Build Docker
   ↓
Push OCIR
   ↓
Deploy OCI
```

Funcionalidades planejadas:

* [ ] CI
* [ ] Execução automática dos testes
* [ ] Build automático
* [ ] Push para OCIR
* [ ] Deploy automático
* [ ] Rollback

---

# 3️⃣7️⃣ 📈 Observabilidade

Evoluções futuras:

* [ ] Logs estruturados
* [ ] Monitoramento da aplicação
* [ ] Monitoramento de recursos
* [ ] Monitoramento de erros
* [ ] Alertas
* [ ] Métricas de uso
* [ ] Métricas de recuperação
* [ ] Métricas de qualidade

---

# 3️⃣8️⃣ 🔮 Evoluções futuras

Após a conclusão do MVP, estão previstas:

* [ ] Reranking avançado;
* [ ] Avaliação avançada de faithfulness;
* [ ] Controle de perguntas fora do escopo;
* [ ] Atualização automática da base documental;
* [ ] Integração com fontes oficiais;
* [ ] Microsoft Teams;
* [ ] Slack;
* [ ] Intranet corporativa;
* [ ] Monitoramento contínuo;
* [ ] Reindexação automática;
* [ ] CI/CD;
* [ ] Observabilidade;
* [ ] Escalabilidade;
* [ ] Vector Search gerenciado;
* [ ] OCI Object Storage;
* [ ] OCI Vault;
* [ ] Autonomous Database.

---

# 3️⃣9️⃣ 🗂️ Estrutura do projeto

```text
reforma-tributaria-ai-agent/
│
├── app/
│   ├── agent.py
│   ├── app.py
│   ├── llm.py
│   ├── prompts.py
│   └── rag.py
│
├── catalog/
│   ├── catalog.csv
│   └── catalog.json
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── evaluation/
│
├── ingestion/
│   ├── cleaning.py
│   ├── chunking.py
│   ├── extraction.py
│   ├── metadata.py
│   └── pipeline.py
│
├── vectorstore/
│   ├── embeddings.py
│   ├── retriever.py
│   └── store.py
│
├── tests/
│   ├── test_agent.py
│   ├── test_chunking.py
│   ├── test_cleaning.py
│   ├── test_embeddings.py
│   ├── test_extraction.py
│   ├── test_ingestion.py
│   ├── test_llm.py
│   ├── test_metadata.py
│   ├── test_pipeline.py
│   ├── test_prompts.py
│   ├── test_rag.py
│   ├── test_retriever.py
│   └── test_vectorstore.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 4️⃣0️⃣ 🧩 Responsabilidades dos principais módulos

### `ingestion/`

Responsável por preparar os documentos:

```text
Documento
   ↓
Extraction
   ↓
Cleaning
   ↓
Metadata
   ↓
Chunking
```

### `vectorstore/`

Responsável por transformar os chunks em vetores e disponibilizar a recuperação:

```text
Chunks
   ↓
Embeddings
   ↓
Vector Store
   ↓
Retriever
```

### `embeddings.py`

Responsável exclusivamente por:

* Carregar o modelo;
* Transformar texto em vetores;
* Transformar múltiplos chunks em vetores;
* Validar entradas;
* Garantir consistência dimensional;
* Normalizar embeddings.

### `store.py`

Responsável por:

* Armazenar vetores;
* Persistir dados;
* Carregar índice;
* Executar busca;
* Ordenar resultados.

### `retriever.py`

Responsável por:

* Receber a consulta;
* Gerar embedding;
* Consultar o Vector Store;
* Aplicar filtros;
* Recuperar Top-K;
* Retornar chunks relevantes.

### `app/rag.py`

Responsável pela camada RAG:

```text
Pergunta
   ↓
Retriever
   ↓
Filtros
   ↓
Similaridade
   ↓
Contexto
```

### `app/agent.py`

Responsável pela orquestração:

```text
Pergunta
   ↓
RAG
   ↓
Prompt
   ↓
LLM
   ↓
Resposta
```

---

# 4️⃣1️⃣ 🔬 Métricas de avaliação

O projeto utiliza métricas relacionadas à recuperação e geração.

## Retrieval

```text
Hit@K
MRR
Recall@K
Page Hit
```

## Generation

```text
Faithfulness
Answer Relevancy
Context Precision
Context Recall
```

Essas métricas permitem avaliar não apenas se o documento correto foi recuperado, mas também a qualidade da resposta produzida.

---

# 4️⃣2️⃣ 📊 Fluxo de avaliação

```text
Pergunta de avaliação
        ↓
Retriever
        ↓
Top-K
        ↓
Documento esperado?
        ↓
Página esperada?
        ↓
Fonte esperada?
        ↓
Cobertura dos tópicos
        ↓
LLM
        ↓
Resposta
        ↓
Avaliação
```

---

# 4️⃣3️⃣ 🚦 Legenda de status

| Símbolo | Significado               |
| ------- | ------------------------- |
| ✅       | Concluído e validado      |
| 🧪      | Validado com Mock/FakeLLM |
| 🟡      | Implementação parcial     |
| 🚧      | Em desenvolvimento        |
| 🔮      | Planejado                 |
| ⏳       | Próxima etapa             |

> **Nota:** funcionalidades marcadas com 🧪 foram implementadas e validadas utilizando `FakeLLM`, permitindo testar o fluxo completo sem depender exclusivamente de um provedor externo.

---

# 4️⃣4️⃣ 🛠️ Tecnologias

### Linguagem

* Python 3.x

### Inteligência Artificial

* RAG
* LLM
* Sentence Transformers
* Embeddings
* Busca semântica

### Processamento

* PDF
* Extração de texto
* Cleaning
* Chunking
* Metadata

### Vector Search

* Vector Store
* Similaridade de cosseno
* Recuperação Top-K

### LLM

* Gemini
* FakeLLM para testes

### Interface

* Streamlit

### DevOps / Cloud

* Docker
* Oracle Cloud Infrastructure
* OCI Container Registry
* OCI Container Instance

### Qualidade

* Pytest
* Testes automatizados
* Dataset de avaliação
* Métricas de recuperação

---

# 4️⃣5️⃣ ▶️ Como executar

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd reforma-tributaria-ai-agent
```

## 2. Criar ambiente virtual

### Windows

```powershell
python -m venv .venv
```

Ativar:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

## 4. Configurar variáveis de ambiente

Criar:

```text
.env
```

A partir de:

```text
.env.example
```

## 5. Executar os testes

```bash
python -m pytest -q
```

Resultado esperado:

```text
204 passed
```

## 6. Executar a aplicação

```bash
streamlit run app/app.py
```

---

# 4️⃣6️⃣ 🧪 Exemplo de recuperação

Exemplo de consulta:

```text
Quais são os dois principais tributos que compõem
o IVA Dual da Reforma Tributária do Consumo?
```

O Retriever realiza:

```text
Pergunta
   ↓
Embedding
   ↓
Vector Store
   ↓
Top-K
   ↓
Ranking
   ↓
Filtro de similaridade
   ↓
Contexto
```

Exemplo de resultados recuperados:

```text
Modulo_1_parte_1.pdf | página 8
Modulo_1_parte_1.pdf | página 22
Modulo_10_parte_1.pdf | página 3
Modulo_12_parte_2.pdf | página 25
Modulo_1_parte_1.pdf | página 9
```

A recuperação preserva os metadados necessários para rastreabilidade.

---

# 4️⃣7️⃣ ⚠️ Limitações atuais

O projeto ainda está em desenvolvimento e possui algumas limitações:

* Base documental predominantemente em PDF;
* Reranking ainda não implementado;
* Interface conversacional ainda em evolução;
* Atualização automática da base ainda não implementada;
* Monitoramento ainda não implementado;
* Deploy em produção ainda em desenvolvimento;
* Integrações com Teams e Slack ainda planejadas;
* Avaliação avançada de faithfulness ainda pendente.

---

# 4️⃣8️⃣ 🚀 Roadmap

```text
                 MVP
                  │
                  ▼
        ┌──────────────────┐
        │ Pipeline RAG     │
        │ ✅ 204 testes    │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Reranking        │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Interface        │
        │ Conversacional   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Docker           │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ OCI              │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ CI/CD            │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Monitoramento    │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Escalabilidade   │
        └──────────────────┘
```

---

# 4️⃣9️⃣ 📌 Próximas prioridades

A sequência recomendada para evolução do projeto é:

### Prioridade 1 — RAG

* [ ] Reranking;
* [x] Limiar mínimo de similaridade;
* [ ] Validação da resposta contra o contexto;
* [ ] Detecção avançada de ausência de evidência;
* [ ] Avaliação de faithfulness.

### Prioridade 2 — Interface

* [ ] Streamlit final;
* [ ] Histórico;
* [ ] Fontes;
* [ ] Feedback;
* [ ] Tratamento de erros.

### Prioridade 3 — Deploy

* [ ] Dockerfile;
* [ ] Build;
* [ ] OCIR;
* [ ] OCI Container Instance;
* [ ] URL pública.

### Prioridade 4 — Engenharia

* [ ] CI/CD;
* [ ] Logs;
* [ ] Monitoramento;
* [ ] Atualização documental;
* [ ] Observabilidade.

---

# 5️⃣0️⃣ 🏁 Visão da solução

O objetivo final é evoluir de:

```text
Documentos
    ↓
RAG
    ↓
Resposta
```

para uma plataforma de conhecimento documental:

```text
                 FONTES OFICIAIS
                        │
                        ▼
                CURADORIA DOCUMENTAL
                        │
                        ▼
                  BASE GOVERNADA
                        │
                        ▼
                 PIPELINE DE RAG
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        RETRIEVAL                LLM
             │                     │
             └──────────┬──────────┘
                        ▼
               RESPOSTA FUNDAMENTADA
                        │
                        ▼
                 FONTE + PÁGINA
                        │
                        ▼
                  FEEDBACK
                        │
                        ▼
              MELHORIA CONTÍNUA
```

A visão é construir uma solução de IA **rastreável, avaliável, governada e preparada para evolução em ambiente corporativo**.

---

# 5️⃣1️⃣ 📜 Licença

Este projeto está disponibilizado sob a licença definida no arquivo [`LICENSE`](LICENSE).

---

# 5️⃣2️⃣ 👩‍💻 Autoria

Desenvolvido como projeto de **Inteligência Artificial, RAG, Engenharia de Dados e aplicação de LLMs**, com foco em conhecimento documental aplicado à Reforma Tributária do Consumo.

---

## ⭐ Projeto em evolução

> **Da documentação oficial à resposta fundamentada.**
>
> O objetivo não é apenas criar um chatbot, mas construir uma **base de conhecimento governada**, capaz de recuperar evidências, contextualizar informações e apresentar respostas com rastreabilidade documental.

```
```
---

## 👩‍💻 Equipe

| Integrante | Atuação |
|---|---|
| **Kelly Costa** | IA / RAG • Desenvolvimento • Dados • Cloud / OCI |

---

## 📄 Licença

Este projeto será disponibilizado para fins de estudo, demonstração e desenvolvimento tecnológico.

A licença definitiva será definida pela equipe durante a publicação do projeto.

---

## ⭐ Contribuição

Sugestões, melhorias e contribuições são bem-vindas.

Caso encontre algum problema ou tenha uma sugestão para evolução do projeto, abra uma **Issue** ou envie um **Pull Request**.

---


# 📄 Documentos


## 📚 Fontes de conhecimento

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

## 📋 Catálogo documental

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


## 📑 Documentos utilizados na base inicial

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

<p align="center">
  Desenvolvido com 🤖 Inteligência Artificial, RAG, Python e Oracle Cloud
</p>


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