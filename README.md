<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/scaffold-logo.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/scaffold-logo.png" alt="Scaffold Banner" style="width:85%;height:100%"/></a>
</h1>

## Introduction

**Scaffold** is a specialized RAG (Retrieval-Augmented Generation) system designed to revolutionize how development teams interact with large codebases. Born from real-world frustrations with traditional documentation and AI-assisted development, Scaffold provides the structural foundation AI agents need to effectively construct, maintain, and repair complex software projects.

### The Challenge
Modern development teams face three critical problems:

1. **Documentation Decay**  
   Maintaining accurate and up-to-date technical documentation requires unsustainable manual effort

2. **AI Context Blindness**  
   LLMs lack awareness of project-specific architecture and business logic, requiring inefficient manual context provisioning

3. **Knowledge Fragmentation**  
   Critical system understanding exists only in tribal knowledge that's lost when team members leave
### Our Solution
Scaffold transforms your source code into a living knowledge graph stored in a graph database. This creates an intelligent context layer that:
- Captures structural relationships between code entities
- Maintains both vector and graph representations of your codebase
- Enables precise context injection for LLMs and AI agents
- Supports construction, maintenance, and refactoring workflows
> Like its physical namesake, Scaffold provides the temporary support structure needed to build something great - then disappears when the work is done.


## Project Organization

### Schemas

<details>
<summary><strong> Architecture Schema</strong> </summary>
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/architecture.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/architecture.png" alt="Scaffold Architecture" style="width:100%;height:100%"/></a></div>
</details>
<details>
<summary><strong> Usecase Schema </strong> </summary>
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/usecase-diagram.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/usecase-diagram.png" alt="Scaffold Usecase Diagram" style="width:100%;height:100%"/></a></div>
</details>
<details>
<summary><strong> Interfaces Schema</strong> </summary>
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/interfaces-diagram.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/interfaces-diagram.png" alt="Scaffold Interfaces" style="width:100%;height:100%"/></a></div>
</details>
<details>
<summary><strong> Internal Organization Schema</strong> </summary>
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/internals-diagram.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/internals-diagram.png" alt="Scaffold Internal Organization" style="width:100%;height:100%"/></a></div>
</details>

### Project Structure

```
.
├── docs
│   ├── docmost   # Docmost Configuration
│   ├── img       # Static Images
│   └── research  # Research reports
└── src
    ├── core      # RAG Context Fetching Algorithms
    ├── database  # Graph/Vector Database Logic
    ├── generator # Abstract Tree Generator
    ├── mcp       # MCP Interface
    └── parsers   # AST Parcers
```


## Team
| Team Member     | Telegram Alias   | Email Address           | Track         | Responsibilities                          |
| :-------------- | :--------------- | :---------------------- | :------------ | :---------------------------------------- |
| Melnikov Sergei        | @peplxx        | s.melnikov@innopolis.university        | Product Owner       | Team Management, RAG Fetching Algorithms |
| Razmakhov Sergei      | @onemoreslacker       | s.razmakhov@innopolis.university         | Developer      | Languages parsers, AT Generation |
| Prosvirkin Dmitry | @dmitry5567          | d.prosvirkin@innopolis.university          | Developer        | Vector, Graph Database Management|
| Mashenkov Timofei  | @mashfeii       | t.mashenkov@innopolis.university      | Developer, Researcher  |  MCP, Signal interfaces |
| Glazov Sergei      | @pushkin404          | s.glazov@innopolis.university       |  QA, Researcher     | QA, Market Research|

## FAQ

<details>
<summary><strong>What is RAG (Retrieval-Augmented Generation)?</strong></summary>

RAG (Retrieval-Augmented Generation) is a technique that enhances large language models (LLMs) by:
1. **Retrieving** relevant information from external knowledge sources
2. **Augmenting** the LLM's context with this retrieved information
3. **Generating** more accurate, context-aware responses

Unlike traditional LLMs that rely solely on their training data, RAG systems:
- Access up-to-date project-specific information
- Reduce hallucinations by grounding responses in actual codebase context
- Maintain knowledge beyond the LLM's token limit
</details>

<details>
<summary><strong>How does Graph RAG work?</strong></summary>

Graph RAG extends traditional RAG by representing knowledge as interconnected entities in a graph database.

</details>

## References & Resources
## Project Materials
- [Excalidraw Board](https://excalidraw.com/#json=DNp6vtk7Ps-d8IqUnFX5p,F8fM6s7Bx-8FcoYoUmuDmA)

- [Google Document](https://docs.google.com/document/d/1K4CPKvia2kNnlKm9MNFnxmQRqHM1KS_lJMJzueEnQVE/edit?usp=sharing)

- [Weekly Report](https://github.com/Beer-Bears/beer-bears/tree/master/content/docs/2025/beer-bears)

- [Weekly Role Distibution Table](https://docs.google.com/spreadsheets/d/1uc_GRhpqoXTGrU90zRO2Lp6TWDvCVzt__PE6KlVH9DU/edit?gid=0#gid=0)

### Useful Themed Videos
- [What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=T-D1OfcDW1M)

- [GraphRAG vs. Traditional RAG: Higher Accuracy & Insight with LLM](https://www.youtube.com/watch?v=Aw7iQjKAX2k)

- [GraphRAG Explained: AI Retrieval with Knowledge Graphs & Cypher](https://www.youtube.com/watch?v=Za7aG-ooGLQ)

- [What is MCP? Integrate AI Agents with Databases & APIs](https://youtu.be/eur8dUO9mvE?si=TzSu6l-6CvSklnFH)

- [Model Context Protocol (MCP) Explained in 20 Minutes](https://youtu.be/N3vHJcHBS-w?si=ZNlkgipXjdqfYZKe)