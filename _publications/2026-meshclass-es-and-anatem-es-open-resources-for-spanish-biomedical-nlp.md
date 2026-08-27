---
bibtexurl: https://santiagom99.github.io/files/paper-bionlp-meshclass.bib
category: workshops
citation: 'Martínez Novoa, S., Gómez Mesa, L., Prieto, J., & Manrique, R. (2026).
  MeSHClass-ES and AnatEM-ES: Open Resources for Spanish Biomedical NLP. In BioNLP
  2026, pp. 617-629. Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.bionlp-1.49'
collection: publications
date: '2026-07-01'
excerpt: ACL Anthology (2026)
paperurl: https://aclanthology.org/2026.bionlp-1.49/
permalink: /publication/2026-meshclass-es-and-anatem-es-open-resources-for-spanish-biomedical-nlp
slidesurl: ''
tags: []
title: 'MeSHClass-ES and AnatEM-ES: Open Resources for Spanish Biomedical NLP'
venue: ACL Anthology
---

## Abstract

Despite Spanish being one of the most widely spoken languages in the world, biomedical NLP resources and systematic evaluations remain limited relative to English. We address this gap by constructing and releasing two Spanish biomedical corpora: (1) MeSHClass-ES, a 29,063 abstract bilingual corpus translated from PubMed with Opus-MT, and (2) AnatEM-ES, the AnatEM anatomical entity corpus translated with a chunk-level LLM-based pipeline that jointly preserves BIO annotations across 13,849 entity mentions. Both corpora achieve a mean COMET score of 0.73 despite using different translation systems. We benchmark nine encoder models spanning general-domain Spanish, domain-specific, and multilingual architectures for both tasks. RigoBERTa-2.0 leads both tasks (micro-F1 classification 0.69, tied with SciBETO-large; NER F1 0.66). Both domain pretraining and model capacity drive performance, with the gap slightly more pronounced for NER (4-point spread) than classification (3-point spread). XLM-RoBERTa-large emerges as a competitive multilingual baseline. A parallel evaluation of four open-weight decoders (7-9B) reveals a task-dependent encoder-decoder gap: QLoRA-adapted Gemma-2-9B reaches 88% of the best encoder on classification (micro-F1 .61 vs .69), but for NER every decoder configuration we tested stays at or below 40% of the best encoder F1. We release both corpora on the HuggingFace Hub, translation pipelines, and evaluation code on GitHub.

## Details

**Author:** Santiago Martínez Novoa, Lina Gómez Mesa, Juan Prieto, Rubén Manrique
**Year:** 2026
**Publication Type:** Paper presented at BioNLP 2026 (Biomedical Natural Language Processing Workshop, ACL), San Diego, California, pp. 617-629  


## Citation

Martínez Novoa, S., Gómez Mesa, L., Prieto, J., & Manrique, R. (2026). MeSHClass-ES and AnatEM-ES: Open Resources for Spanish Biomedical NLP. In BioNLP 2026, pp. 617-629. Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.bionlp-1.49

<div class='cv-download-buttons'>
<a href='https://aclanthology.org/2026.bionlp-1.49/' class='cv-download-btn' target='_blank'><i class='fas fa-external-link'></i> See Paper</a>
<a href='https://santiagom99.github.io/files/paper-bionlp-meshclass.bib' class='cv-download-btn' target='_blank'><i class='fas fa-code'></i> Download BibTeX</a>
</div>
