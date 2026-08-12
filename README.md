# 🤖 Reforma Tributária AI Agent

> **Agente de Inteligência Artificial para consulta, capacitação e apoio à implementação da Reforma Tributária**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/AI-RAG-purple)]()
[![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/)
[![Oracle Cloud](https://img.shields.io/badge/Cloud-Oracle%20Cloud-red?logo=oracle)](https://www.oracle.com/cloud/)

---

## 📌 Sobre o projeto

O **Reforma Tributária AI Agent** é um agente de Inteligência Artificial desenvolvido para facilitar o acesso ao conhecimento relacionado à **Reforma Tributária**, apoiando principalmente profissionais e equipes da área de Contabilidade na compreensão e implementação das novas regras.

A solução utiliza uma abordagem baseada em **RAG — Retrieval-Augmented Generation**, permitindo que o agente consulte uma base de conhecimento construída a partir de documentos selecionados de fontes institucionais e oficiais.

O objetivo é transformar documentos técnicos e regulatórios em uma **base de conhecimento conversacional**, permitindo que o usuário faça perguntas em linguagem natural e receba respostas contextualizadas e fundamentadas nas fontes disponíveis.

---

## 🎯 Objetivo

Desenvolver um agente de IA capaz de:

* Responder perguntas relacionadas à Reforma Tributária;
* Apoiar a capacitação de profissionais da Contabilidade;
* Facilitar a consulta de documentos técnicos e institucionais;
* Recuperar informações relevantes a partir de documentos PDF;
* Apresentar respostas contextualizadas com base na documentação disponível;
* Indicar as fontes utilizadas na construção das respostas;
* Reduzir o tempo necessário para localizar informações em documentos extensos;
* Servir como uma base de conhecimento conversacional acessível aos usuários.

---

## 💡 Problema

A Reforma Tributária envolve mudanças relevantes na estrutura tributária brasileira e demanda atualização contínua por parte dos profissionais de Contabilidade.

Informações importantes podem estar distribuídas em diferentes documentos, materiais técnicos, orientações e regulamentações, tornando a busca manual mais demorada e dificultando a localização rápida de informações específicas.

Diante desse cenário, surge a oportunidade de utilizar Inteligência Artificial para criar uma camada conversacional sobre essa base documental.

Em vez de o profissional precisar localizar manualmente determinada informação em dezenas de documentos, o agente permite realizar uma pergunta em linguagem natural e receber uma resposta baseada nos conteúdos disponíveis.

---

## 👥 Público-alvo

O agente foi concebido principalmente para:

* Contadores;
* Profissionais da área contábil;
* Equipes fiscais e tributárias;
* Profissionais envolvidos na implementação da Reforma Tributária;
* Estudantes e profissionais que desejam compreender o tema;
* Usuários interessados em consultar informações sobre a Reforma Tributária.

O acesso ao agente será **aberto**, não havendo necessidade de restringir sua utilização a um grupo específico de usuários.

---

# 🧠 Como funciona?

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

### 🔎 RAG

O RAG permite que o modelo de linguagem consulte informações recuperadas da base documental antes de gerar uma resposta.

Dessa forma, o agente não depende exclusivamente do conhecimento previamente aprendido pelo modelo.

O processo ocorre em duas etapas principais:

**Retrieval**

```text
Pergunta do usuário
        ↓
Busca semântica
        ↓
Trechos relevantes dos documentos
```

**Generation**

```text
Pergunta
   +
Contexto recuperado
   ↓
Modelo de linguagem
   ↓
Resposta contextualizada
```

---

# 📚 Fontes de conhecimento

A base de conhecimento será construída a partir de documentos relacionados à Reforma Tributária provenientes de fontes institucionais e oficiais.

### Conselho Federal de Contabilidade — CFC

Materiais relacionados à atuação e capacitação dos profissionais de Contabilidade.

### Federação Nacional das Empresas de Serviços Contábeis — Fenacon

Materiais e conteúdos relacionados ao ambiente contábil, fiscal e empresarial.

### Receita Federal

Documentos, orientações, materiais de apoio e informações oficiais relacionadas à Reforma Tributária do Consumo.

A Receita Federal mantém atualmente um programa específico sobre a Reforma Tributária do Consumo, incluindo informações sobre implementação, marcos legais, projetos tecnológicos, regulamentação e materiais de apoio.

Entre os materiais disponibilizados estão conteúdos do **Curso Reforma Tributária RFB e CFC**, incluindo temas como normas gerais da tributação do consumo, CBS, cadastro, obrigações acessórias, apuração assistida e compensação.

> **Importante:** as fontes utilizadas pelo agente deverão ser mantidas identificadas e atualizadas, permitindo maior rastreabilidade das informações utilizadas nas respostas.

---

# 📄 Documentos

### Formato inicial

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

# 🗂️ Metadados dos documentos

Além do conteúdo textual, os documentos poderão ser associados a metadados para melhorar a recuperação e a rastreabilidade das respostas.

Exemplo:

```text
fonte
nome_documento
tipo_documento
data_publicacao
categoria
tema
pagina
url_origem
```

Essas informações poderão ser utilizadas pelo agente para apresentar ao usuário a origem do conteúdo recuperado.

---

# 💬 Exemplos de perguntas

O usuário poderá realizar perguntas como:

> **O que muda com a Reforma Tributária?**

> **Quais são os principais impactos da Reforma Tributária para a Contabilidade?**

> **Como funciona a transição para o novo modelo tributário?**

> **O que é o IBS?**

> **O que é a CBS?**

> **Quais são as principais obrigações acessórias relacionadas à Reforma Tributária?**

> **Segundo os materiais do CFC, quais são os principais pontos de atenção para os profissionais de Contabilidade?**

> **Quais orientações a Receita Federal disponibilizou para 2026?**

A Receita Federal já disponibiliza orientações específicas para 2026, incluindo informações sobre CBS, IBS e documentos fiscais eletrônicos.

---

# 📚 Respostas fundamentadas

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
• Documento: Orientações da Reforma Tributária para 2026
• Página: XX

• CFC
• Documento: XXXXX
• Página: XX
```

Essa abordagem busca aumentar a **transparência, rastreabilidade e confiabilidade** das respostas.

---

# 🛡️ Confiabilidade e controle de respostas

O agente deverá priorizar informações presentes na base documental disponibilizada.

Quando não houver informações suficientes para responder determinada pergunta, o comportamento esperado será informar ao usuário que não foram encontrados elementos suficientes na base de conhecimento.

Exemplo:

> ⚠️ Não foram encontradas informações suficientes nos documentos disponíveis para responder a essa pergunta com segurança.

Essa estratégia busca reduzir respostas sem fundamentação documental e minimizar o risco de geração de informações não suportadas pelas fontes.

---

# 🏗️ Arquitetura do projeto

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
│   CFC / Fenacon / RFB │
└───────────────────────┘
```

---

# 🧰 Tecnologias

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

# 🔄 Pipeline de ingestão

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

# 🤖 Pipeline do agente

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

# 📊 Avaliação do agente

A qualidade do agente será avaliada por meio de um conjunto de perguntas de teste.

Os testes deverão contemplar diferentes cenários:

| Cenário                               | Objetivo                        |
| ------------------------------------- | ------------------------------- |
| Pergunta direta                       | Avaliar recuperação simples     |
| Pergunta conceitual                   | Avaliar compreensão             |
| Pergunta específica                   | Avaliar precisão                |
| Pergunta envolvendo diferentes fontes | Avaliar recuperação múltipla    |
| Pergunta sem resposta na base         | Avaliar controle de alucinação  |
| Pergunta fora do escopo               | Avaliar comportamento do agente |
| Pergunta com termos técnicos          | Avaliar recuperação semântica   |

A avaliação permitirá identificar oportunidades de melhoria no processo de ingestão, chunking, recuperação e geração das respostas.

---

# ☁️ Deploy na Oracle Cloud Infrastructure

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

O serviço OCI utilizado será documentado nesta seção após a definição e implementação da arquitetura de infraestrutura.

---

# 🎥 Demonstração

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

# 📁 Estrutura do projeto

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
├── ingestion/
│   ├── pdf_loader.py
│   ├── chunking.py
│   └── embeddings.py
│
├── vectorstore/
│
├── notebooks/
│   └── exploracao_rag.ipynb
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

A estrutura poderá ser ajustada conforme a evolução da arquitetura.

---

# 🚀 Como executar localmente

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

# 🗺️ Roadmap

### 🟢 Etapa 1 — Definição

* [x] Definição do problema
* [x] Definição do público-alvo
* [x] Definição da abordagem RAG
* [x] Definição das fontes iniciais
* [ ] Definição da arquitetura final

### 🟡 Etapa 2 — Base de conhecimento

* [ ] Seleção dos documentos
* [ ] Download e organização dos PDFs
* [ ] Extração de texto
* [ ] Tratamento dos documentos
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
* [ ] Ajustes no RAG

### 🔵 Etapa 6 — Cloud

* [ ] Configuração da OCI
* [ ] Deploy
* [ ] Testes em ambiente cloud
* [ ] Disponibilização online
* [ ] Registro da demonstração
* [ ] Atualização do README

---

# 🔐 Segurança

O projeto deverá seguir boas práticas de segurança, incluindo:

* Não versionar chaves de API;
* Utilizar variáveis de ambiente;
* Não armazenar credenciais no código;
* Utilizar `.gitignore`;
* Avaliar cuidadosamente os documentos incorporados à base;
* Manter identificadas as fontes utilizadas;
* Evitar respostas não fundamentadas nos documentos disponíveis.

---

# ⚠️ Limitações

O agente não substitui a análise de profissionais habilitados nem constitui, por si só, orientação ou parecer contábil, fiscal ou jurídico.

As respostas dependem da qualidade, atualização e abrangência dos documentos incorporados à base de conhecimento.

Como a Reforma Tributária está em processo de implementação, documentos e orientações podem ser atualizados. A Receita Federal, por exemplo, mantém páginas específicas com orientações e marcos regulatórios que são atualizados ao longo da implementação.

Por isso, a base documental deverá possuir mecanismos de atualização e identificação da origem dos conteúdos.

---

# 🌱 Possíveis evoluções

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
* Expansão para outros temas contábeis e tributários.

---

# 📚 Referências institucionais

* **Receita Federal — Programa da Reforma Tributária do Consumo**
* **Receita Federal — Orientações da Reforma Tributária para 2026**
* **Receita Federal — Material de Apoio do Curso Reforma Tributária RFB e CFC**
* **Conselho Federal de Contabilidade — CFC**
* **Federação Nacional das Empresas de Serviços Contábeis — Fenacon**

A Receita Federal disponibiliza materiais específicos do curso RFB/CFC sobre a Reforma Tributária, incluindo conteúdos sobre normas gerais, CBS, cadastro, obrigações acessórias, apuração assistida e outros temas.

---

# 👩‍💻 Equipe

Projeto desenvolvido como parte do desafio de desenvolvimento de soluções com **Inteligência Artificial, RAG e Oracle Cloud Infrastructure**.

### Integrantes

| Nome               | Atuação         |
| ------------------ | --------------- |
| Nome do integrante | IA / RAG        |
| Nome do integrante | Desenvolvimento |
| Nome do integrante | Dados           |
| Nome do integrante | Cloud / OCI     |

---

# 📄 Licença

Este projeto será disponibilizado para fins de estudo, demonstração e desenvolvimento tecnológico.

A licença definitiva será definida pela equipe durante a publicação do projeto.

---

## ⭐ Contribuição

Sugestões, melhorias e contribuições são bem-vindas.

Caso encontre algum problema ou tenha uma sugestão para evolução do projeto, abra uma **Issue** ou envie um **Pull Request**.

---

<p align="center">
  Desenvolvido com 🤖 Inteligência Artificial, RAG, Python e Oracle Cloud
</p>
