# MIPVU-Based Metaphor Analysis Instrument

## Overview

This repository contains a systematized instrument for the identification, annotation, and analysis of conceptual metaphors in Spanish corpora. The instrument is based on the **MIPVU (Metaphor Identification Procedure Vrije Universiteit)** protocol and has been refined through multiple research projects in cognitive linguistics and discourse analysis.

## File

**[`MIPVU_Metaphor_Analysis_Instrument.xlsx`](MIPVU_Metaphor_Analysis_Instrument.xlsx)**

## Background and Development

This instrument has been developed and refined through several interconnected research initiatives:

### Research Lineage

1. **Initial Development**  
   As part of the research project *"Propuesta metodológica para el etiquetado de un corpus lingüístico con fines de identificación de metáforas conceptuales en español"* (Methodological Proposal for the Annotation of a Linguistic Corpus for the Identification of Conceptual Metaphors in Spanish), led by **Prof. María Isabel Marín Morales** as principal investigator.

2. **Doctoral Research**  
   Further refined in Prof. Marín Morales' doctoral research at the **University of Groningen, The Netherlands**: *"From Metaphor to Narrative: Computational Modeling of Cultural Discourse through MELT and Large Language Models"*.

3. **Undergraduate Thesis Projects**  
   Applied and validated as principal advisor in the following undergraduate research projects:
   - *"Conceptualización de las mujeres y del conflicto armado colombiano a través de las metáforas conceptuales en el Informe Final de la Comisión de la Verdad"* (Conceptualization of Women and the Colombian Armed Conflict through Conceptual Metaphors in the Final Report of the Truth Commission)
   - *"La esquizofrenia desde una perspectiva lingüística cognitiva: análisis de las metáforas conceptuales en El abismo de Neal Shusterman"* (Schizophrenia from a Cognitive Linguistic Perspective: Analysis of Conceptual Metaphors in Neal Shusterman's *Challenger Deep*) [ongoing]

### Research Group

This work has been developed within the **ExMachina Research Seminar - Universidad de Antioquia** under the direction of **PhD(c) María Isabel Marín Morales**.

## Theoretical Framework

The instrument integrates methodological approaches from:

- **Conceptual Metaphor Theory** (Lakoff & Johnson, 1980)
- **MIPVU Protocol** (Steen et al., 2010) - Metaphor Identification Procedure Vrije Universiteit
- **Coll-Florit & Climent Methodology** (2019) - Systematic approach for conceptual metaphor detection and formulation in corpora
- **Cognitive Linguistics** frameworks for metaphor analysis
- **Corpus Linguistics** methodologies for systematic annotation

## Instrument Structure

The Excel-based instrument contains **19 fields** designed to capture comprehensive information about each metaphorical expression identified in a corpus.

### Field Descriptions

#### 1. **ID**
- **Purpose**: Unique identifier for each metaphorical expression
- **Format**: Alphanumeric code (e.g., CEV_1, CEV_2)
- **Function**: Enables systematic referencing and database management

#### 2-4. **Título 1, Título 2, Título 3** (Hierarchical Headers)
- **Purpose**: Document structure and organizational metadata
- **Format**: Nested hierarchical levels
- **Function**: Captures the documentary context (e.g., document title, chapter, section)
- **Example**: 
  - Título 1: Main document title
  - Título 2: Chapter or major section
  - Título 3: Subsection or specific segment

#### 5. **Página** (Page)
- **Purpose**: Page reference in source document
- **Format**: Numeric
- **Function**: Enables precise location tracking for verification and citation

#### 6. **Expresión metafórica** (Metaphorical Expression)
- **Purpose**: Complete textual unit containing the metaphor
- **Format**: Full sentence or relevant textual segment
- **Function**: Preserves the complete linguistic context of the metaphorical usage

#### 7. **Contexto** (Context)
- **Purpose**: Extended textual environment surrounding the metaphor
- **Format**: Multi-sentence excerpt (typically ±2-3 sentences)
- **Function**: Provides interpretive context for accurate metaphor identification and analysis

#### 8. **Foco** (Focus)
- **Purpose**: The specific word or phrase that carries the metaphorical meaning
- **Format**: Single word or minimal phrase
- **Function**: Identifies the precise linguistic element subject to metaphorical extension

#### 9. **Foco lematizado** (Lemmatized Focus)
- **Purpose**: Dictionary form of the focus word
- **Format**: Lemma (base form)
- **Function**: Enables systematic analysis and frequency counts across inflected forms
- **Example**: "construido" → "construir"

#### 10. **Categoría gramatical del foco** (Grammatical Category of Focus)
- **Purpose**: Part-of-speech classification
- **Format**: Grammatical category label (Sustantivo/Noun, Verbo/Verb, Adjetivo/Adjective, etc.)
- **Function**: Facilitates grammatical pattern analysis in metaphor usage

#### 11. **Significado contextual** (Contextual Meaning)
- **Purpose**: The meaning of the focus word as used in this specific context
- **Format**: Brief definition or explanation
- **Function**: Captures the target domain interpretation (abstract meaning)

#### 12. **Significado básico** (Basic Meaning)
- **Purpose**: The more concrete, physical, or historically prior meaning of the focus word
- **Format**: Dictionary definition (with source citation, typically DLE - Diccionario de la Lengua Española)
- **Function**: Essential for MIPVU protocol - establishes the contrast that signals metaphor

#### 13. **Metáfora conceptual** (Conceptual Metaphor)
- **Purpose**: The underlying conceptual mapping
- **Format**: "TARGET DOMAIN IS SOURCE DOMAIN" (in capitals)
- **Function**: Identifies the systematic conceptual correspondence
- **Example**: "LA CONFIANZA ES UN EDIFICIO" (TRUST IS A BUILDING)

#### 14. **Dominio fuente** (Source Domain)
- **Purpose**: The concrete domain from which the metaphorical mapping originates
- **Format**: Single concept or semantic field (in capitals)
- **Function**: Identifies the experiential basis of the metaphor
- **Example**: EDIFICIO (BUILDING), ESPEJO (MIRROR)

#### 15. **Dominio meta** (Target Domain)
- **Purpose**: The abstract domain being conceptualized metaphorically
- **Format**: Single concept or semantic field (in capitals)
- **Function**: Identifies what is being understood through metaphor
- **Example**: CONFIANZA (TRUST), TESTIMONIO (TESTIMONY)

#### 16. **Correspondencias ontológicas** (Ontological Correspondences)
- **Purpose**: Systematic mappings between entities in source and target domains
- **Format**: Detailed description of structural correspondences
- **Function**: Explicates how elements of the source domain map onto the target
- **Example**: "Trust (building) is constructed by builders (the commission and the conflict actors)"

#### 17. **Correspondencias epistémicas** (Epistemic Correspondences)
- **Purpose**: Knowledge and inferential patterns transferred from source to target
- **Format**: Detailed description of reasoning and inference patterns
- **Function**: Captures how source domain knowledge structures understanding of target domain

#### 18. **Tipología** (Typology)
- **Purpose**: Classification of metaphor type
- **Format**: Category label
- **Function**: Enables systematic categorization
- **Common types**: 
  - Estructural (Structural)
  - Ontológica (Ontological)
  - Orientacional (Orientational)

#### 19. **Observaciones** (Observations)
- **Purpose**: Additional notes, analytical comments, or methodological remarks
- **Format**: Free text
- **Function**: Captures analyst insights, ambiguities, or special considerations

## Complete Example

### Metaphor Entry: "Building Trust"

| Field | Content |
|-------|---------|
| **ID** | CEV_2 |
| **Título 1** | COLOMBIA ADENTRO, Relatos territoriales sobre el conflicto armado: Amazonía |
| **Título 2** | Presentación |
| **Título 3** | Relatos territoriales del conflicto armado |
| **Página** | 23 |
| **Expresión metafórica** | Eso ha sido posible solo por la confianza que antecede al encuentro, confianza que en ocasiones hemos construido en el momento |
| **Contexto** | Eso ha sido posible solo por la confianza que antecede al encuentro, confianza que en ocasiones hemos construido en el momento, |
| **Foco** | Construido |
| **Foco lematizado** | Construir |
| **Categoría gramatical del foco** | Verbo |
| **Significado contextual** | La confianza es un proceso de interacción que se va dando entre personas con el pasar del tiempo |
| **Significado básico** | Hacer de nueva planta una obra de arquitectura o ingeniería, un monumento o en general cualquier obra pública. (DLE) |
| **Metáfora conceptual** | LA CONFIANZA ES UN EDIFICIO |
| **Dominio fuente** | EDIFICIO |
| **Dominio meta** | CONFIANZA |
| **Correspondencias ontológicas** | La confianza como un edificio; La comisión y los actores del conflicto como los constructores |
| **Correspondencias epistémicas** | Los edificios (la confianza) son construidos por edificadores (la comisión y los actores del conflicto) |
| **Tipología** | Estructural |
| **Observaciones** | [blank] |

### Analysis of Example

In this entry, the verbal form "construido" (built/constructed) is identified as metaphorical because:

1. **Contextual meaning**: Trust develops through interpersonal interaction over time
2. **Basic meaning**: Physical construction of architectural structures
3. **Metaphorical mapping**: The abstract concept of TRUST is understood through the concrete domain of BUILDING/CONSTRUCTION
4. **Ontological correspondences**: 
   - Trust ↔ Building
   - People developing trust ↔ Construction workers
   - Interpersonal process ↔ Construction process
5. **Epistemic correspondence**: Just as buildings require systematic construction by builders, trust requires systematic development by the parties involved

## Application Guidelines

### Using the Instrument

1. **Preparation**
   - Read the source text thoroughly
   - Familiarize yourself with MIPVU protocol
   - Prepare dictionary resources (especially DLE for Spanish)

2. **Identification Phase**
   - Apply MIPVU procedure to identify potential metaphorical expressions
   - For each candidate, verify contrast between contextual and basic meanings

3. **Documentation Phase**
   - Complete all relevant fields systematically
   - Pay special attention to ontological and epistemic correspondences
   - Maintain consistency in formulation of conceptual metaphors

4. **Analysis Phase**
   - Use the structured data for quantitative and qualitative analysis
   - Identify patterns in source/target domain mappings
   - Examine distribution across document sections

### Best Practices

- **Consistency**: Maintain uniform criteria across all entries
- **Dictionary citations**: Always cite the specific dictionary entry for basic meanings
- **Conceptual metaphor formulation**: Use consistent format (TARGET DOMAIN IS SOURCE DOMAIN)
- **Context preservation**: Include sufficient context for independent verification
- **Correspondence detail**: Explicate mappings thoroughly to enable replication


## Citation

If you use this instrument in your research, please cite:

```
Marín Morales, M. I. (2025). MIPVU-Based Metaphor Analysis Instrument. 
ExMachina Research Seminar. [DOI/Repository URL]
```

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Contact

**María Isabel Marín Morales**  
Candidata a doctora
Universidad de Groningen  
m.i.marin.morales@rug.nl

## Acknowledgments

This instrument has been developed through collaborative work within the ExMachina Research Seminar and refined through multiple research projects examining conceptual metaphors in diverse discourse contexts, from political testimony to literary narratives of mental illness.

## References

- Coll-Florit, M., & Climent, S. (2019). A new methodology for conceptual metaphor detection and formulation in corpora: A case study on a mental health corpus. *Metaphor and the Social World*, *9*(1), 32-54. https://doi.org/10.1075/msw.00001.col
- Lakoff, G., & Johnson, M. (1980). *Metaphors We Live By*. University of Chicago Press.
- Steen, G. J., Dorst, A. G., Herrmann, J. B., Kaal, A. A., Krennmayr, T., & Pasma, T. (2010). *A Method for Linguistic Metaphor Identification: From MIP to MIPVU*. John Benjamins Publishing.


