#!/usr/bin/env python3
"""
Generador completo para Academic Pages desde JSON
Convierte cv-data.json a archivos .md y actualiza templates
"""

import json
import os
from datetime import datetime
import re
import yaml

def sanitize_filename(text):
    """Convierte texto a filename válido"""
    filename = re.sub(r'[^\w\s-]', '', text.lower())
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-')

def generate_publications(cv_data, output_dir="_publications"):
    """Genera archivos .md para publicaciones - Vista simplificada"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Limpiar directorio existente
    for file in os.listdir(output_dir):
        if file.endswith('.md'):
            os.remove(os.path.join(output_dir, file))
    
    for pub in cv_data.get('publications', []):
        citation = pub['citation_info']
        title = citation['title']
        year = citation['year']
        date = citation.get('date', f"{year}-01-01")
        author = citation['author']['full_name']
        
        filename = f"{year}-{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Determinar categoría y venue
        doc_type = citation.get('document_type', {})
        if isinstance(doc_type, dict):
            excerpt = doc_type.get('en', 'Publication')
            category = pub.get('category', 'paper')
        else:
            excerpt = str(doc_type)
            category = 'thesis' if 'thesis' in str(doc_type).lower() else 'paper'
        
        repository_name = citation.get('repository', {}).get('name', '')
        if isinstance(repository_name, dict):
            venue = repository_name.get('en', '')
        else:
            venue = str(repository_name)
        
        paperurl = citation.get('repository', {}).get('url', '')
        abstract = citation.get('abstract', {}).get('en', '')
        keywords = citation.get('keywords', [])
        bibtex_path = pub.get('bibtex_website', '')
        
        # Front matter - SOLO información esencial para vista de archivo
        front_matter = {
            'title': title,
            'collection': 'publications',
            'category': category,
            'permalink': f'/publication/{year}-{sanitize_filename(title)}',
            'excerpt': f"{venue} ({year})",  # Solo venue y año
            'date': date,
            'venue': venue,
            'slidesurl': '',
            'paperurl': paperurl,
            'citation': pub.get("formatted_citations", {}).get("apa_style", ""),
            'tags': keywords,
            'bibtexurl': bibtex_path if bibtex_path else '',
        }
        
        # CONTENIDO COMPLETO - Solo visible al hacer clic
        supervisor_line = ""
        if citation.get('supervisor'):
            supervisor_line = f"**Supervisor:** {citation['supervisor']}  \n"
        
        keywords_line = ""
        if keywords:
            keywords_line = f"**Keywords:** {', '.join(keywords)}  \n"
        
        # Clean resources section
        resources_section = ""
        if paperurl or bibtex_path:
            resources_section = "\n<div class='cv-download-buttons'>\n"
            if paperurl:
                resources_section += f"<a href='{paperurl}' class='cv-download-btn' target='_blank'><i class='fas fa-external-link'></i> See Paper</a>\n"
            if bibtex_path:
                resources_section += f"<a href='{bibtex_path}' class='cv-download-btn' target='_blank'><i class='fas fa-code'></i> Download BibTeX</a>\n"
            resources_section += "</div>\n"
        
        # BibTeX section (separate from resources)
        bibtex_section = ""
        if pub.get('formatted_citations', {}).get('bibtex'):
            bibtex_content = pub['formatted_citations']['bibtex']
            bibtex_section = f"\n## BibTeX Citation\n\n```bibtex\n{bibtex_content}\n```\n"
        
        # Contenido del archivo - MÁS DETALLADO
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

## Abstract

{abstract if abstract else 'No abstract available.'}

## Details

**Author:** {author}  
**Year:** {year}  
**Institution:** {citation['institution']}  
**Publication Type:** {excerpt}  
{supervisor_line}{keywords_line}

## Citation

{pub.get("formatted_citations", {}).get("apa_style", "")}
{resources_section}{bibtex_section}"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated publication: {filename}")


def generate_talks(cv_data, output_dir="_talks"):
    """Genera archivos .md para talks/presentations - Vista simplificada"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Limpiar directorio existente
    for file in os.listdir(output_dir):
        if file.endswith('.md'):
            os.remove(os.path.join(output_dir, file))
    
    for talk in cv_data.get('talks', []):
        title = talk['title']['en']
        date = talk['date']
        event = talk['event']
        location = talk['location']
        talk_type = talk['type']
        
        filename = f"{date}-{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        
        abstract = talk.get('abstract', {}).get('en', '')
        talk_url = talk.get('url', '')
        slides_name = talk.get('id', '')
        
        slides_path = f"{{{{ base_path }}}}/files/slides/{slides_name}.pdf"
        # Front matter - SOLO información esencial para vista de archivo
        front_matter = {
            'title': title,
            'collection': 'talks',
            'type': talk_type,
            'permalink': f'/talks/{date}-{sanitize_filename(title)}',
            'venue': event,
            'date': date,
            'location': location,
            'slidesurl': slides_path if os.path.exists(slides_path) else '',
            'paperurl': talk_url
        }
        
        # CONTENIDO COMPLETO - Solo visible al hacer clic
        coauthors_line = ""
        if talk.get('coauthors'):
            coauthors_line = f"**Co-authors:** {', '.join(talk['coauthors'])}  \n"
        
        # Clean resources section for talks
        resources_section = ""
        if talk_url or slides_path:
            resources_section = "\n<div class='cv-download-buttons'>\n"
            if talk_url:
                resources_section += f"<a href='{talk_url}' class='cv-download-btn' target='_blank'><i class='fas fa-info-circle'></i> More Info</a>\n"
            if slides_path:
                resources_section += f"<a href='{slides_path}' class='cv-download-btn' target='_blank'><i class='fas fa-file-powerpoint'></i> Download {talk_type}</a>\n"
            resources_section += "</div>\n"
        
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

## Abstract

{abstract if abstract else 'No abstract available for this talk.'}

## Event Details

**Event:** {event}  
**Type:** {talk_type.title()}  
**Location:** {location}  
**Date:** {date}  
{coauthors_line}{resources_section}"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated talk: {filename}")


def generate_experience(cv_data, output_dir="_experience"):
    """Genera archivos .md para experiencia (work + research)"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Limpiar archivos de experiencia existentes
    for file in os.listdir(output_dir):
        if file.endswith('.md') and ('work' in file or 'research' in file):
            os.remove(os.path.join(output_dir, file))
    
    # Ordenar experiencia laboral por fecha (más reciente primero)
    work_experience = sorted(
        cv_data.get('experience', []), 
        key=lambda x: x['startDate'], 
        reverse=True
    )
    
    # Generar experiencia laboral
    for exp in work_experience:
        title = exp['title']['en'] if isinstance(exp['title'], dict) else exp['title']
        company = exp['company']['en'] if isinstance(exp['company'], dict) else exp['company']
        start_date = exp['startDate']
        end_date = exp['endDate']
        
        filename = f"work-{start_date}-{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Crear excerpt con achievements
        achievements = []
        for achievement in exp.get('achievements', []):
            achievements.append(achievement['en'])
        excerpt = ""
        
        # Front matter
        front_matter = {
            'title': title,
            'collection': 'experience',
            'type': 'work',
            'permalink': f'/experience/work-{start_date}-{sanitize_filename(title)}',
            'date': f"{start_date}-01-01",
            'location': exp['location'],
            'company': company,
            'period': f"{start_date} - {end_date}",
            'venue': company,  # Para compatibilidad con el template
            'technologies': exp.get('technologies', []),
            'excerpt': excerpt
        }
        
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

### Key Achievements

"""
        
        for achievement in exp.get('achievements', []):
            content += f"* {achievement['en']}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated work experience: {filename}")
    
    # Ordenar investigación por fecha (más reciente primero)
    research_experience = sorted(
        cv_data.get('research', []), 
        key=lambda x: x['startDate'], 
        reverse=True
    )
    
    # Generar investigación
    for research in research_experience:
        title = research['title']['en']
        institution = research['institution']
        start_date = research['startDate']
        end_date = research['endDate']
        research_group = research.get('research_group', 'N/A')
        
        filename = f"research-{start_date}-{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Crear excerpt con description
        descriptions = []
        for desc in research.get('description', []):
            descriptions.append(desc['en'])
        excerpt = ""
        
        # Front matter
        front_matter = {
            'title': title,
            'collection': 'experience',
            'type': 'research',
            'permalink': f'/experience/research-{start_date}-{sanitize_filename(title)}',
            'date': f"{start_date}-01-01",
            'location': research['location'],
            'institution': institution,
            'period': f"{start_date} - {end_date}",
            'venue': institution,  # Para compatibilidad con el template
            'research_group': research_group,
            'supervisor': research.get('supervisor', ''),
            'technologies': research.get('technologies', []),
            'excerpt': excerpt
        }
        
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

### Description

"""
        
        for desc in research.get('description', []):
            content += f"* {desc['en']}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated research experience: {filename}")


def generate_experience(cv_data, output_dir="_experience"):
    """Genera archivos .md para experiencia (work + research)"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Limpiar archivos de experiencia existentes
    for file in os.listdir(output_dir):
        if file.endswith('.md') and ('work' in file or 'research' in file):
            os.remove(os.path.join(output_dir, file))
    
    # Ordenar experiencia laboral por fecha (más reciente primero)
    work_experience = sorted(
        cv_data.get('experience', []), 
        key=lambda x: x['startDate'], 
        reverse=True
    )
    
    # Generar experiencia laboral
    for exp in work_experience:
        title = exp['title']['en'] if isinstance(exp['title'], dict) else exp['title']
        company = exp['company']['en'] if isinstance(exp['company'], dict) else exp['company']
        start_date = exp['startDate']
        end_date = exp['endDate']
        
        filename = f"work-{start_date}-{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        location = exp.get('location', 'Unknown Location')
        if isinstance(location, dict):
            location = location.get('en', 'Unknown Location')
        else:
            location = str(location)
        # Crear excerpt con achievements
        achievements = []
        for achievement in exp.get('achievements', []):
            achievements.append(achievement['en'])
        excerpt = ""
        
        # Front matter
        front_matter = {
            'title': title,
            'collection': 'experience',
            'type': 'work',
            'permalink': f'/experience/work-{start_date}-{sanitize_filename(title)}',
            'date': f"{start_date}-01-01",
            'location': location,
            'company': company,
            'period': f"{start_date} - {end_date}",
            'venue': company,  # Para compatibilidad con el template
            'technologies': exp.get('technologies', []),
            'excerpt': excerpt
        }
        
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

### Key Achievements

"""
        
        for achievement in exp.get('achievements', []):
            content += f"* {achievement['en']}\n"
        
        # Agregar tecnologías al final del contenido
        if exp.get('technologies'):
            content += f"""


<div class="archive__item-tags">
"""
            for tech in exp['technologies']:
                content += f'  <span class="archive__tag">{tech}</span>\n'
            content += "</div>\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated work experience: {filename}")
    
    # Ordenar investigación por fecha (más reciente primero)
    research_experience = sorted(
        cv_data.get('research', []), 
        key=lambda x: x['startDate'], 
        reverse=True
    )
    
    # Generar investigación
    for research in research_experience:
        title = research['title']['en']
        institution = research['institution']
        if isinstance(institution, dict):
            institution = institution.get('en', 'Unknown Institution')
        else:
            institution = str(institution)
        start_date = research['startDate']
        end_date = research['endDate']
        research_group = research.get('research_group', 'N/A')
        location = research.get('location', 'Unknown Location')
        if isinstance(location, dict):
            location = location.get('en', 'Unknown Location')
        else:
            location = str(location)
        filename = f"research-{start_date}-{sanitize_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Crear excerpt con description
        descriptions = []
        for desc in research.get('description', []):
            descriptions.append(desc['en'])
        
        excerpt = ""
        # Front matter
        front_matter = {
            'title': title,
            'collection': 'experience',
            'type': 'research',
            'permalink': f'/experience/research-{start_date}-{sanitize_filename(title)}',
            'date': f"{start_date}-01-01",
            'location': location,
            'institution': institution,
            'period': f"{start_date} - {end_date}",
            'venue': institution,  # Para compatibilidad con el template
            'research_group': research_group,
            'technologies': research.get('technologies', []),
            'excerpt': excerpt
        }
        
        # Solo agregar supervisor si existe y no está vacío
        if research.get('supervisor') and research['supervisor'].strip():
            front_matter['supervisor'] = research['supervisor']
        
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

### Description

"""
        
        for desc in research.get('description', []):
            content += f"* {desc['en']}\n"
        
        # Agregar tecnologías al final del contenido
        if research.get('technologies'):
            content += f"""


<div class="archive__item-tags">
"""
            for tech in research['technologies']:
                content += f'  <span class="archive__tag">{tech}</span>\n'
            content += "</div>\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated research experience: {filename}")


def generate_teaching(cv_data, output_dir="_teaching"):
    """Genera archivos .md para experiencia docente"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Limpiar directorio existente
    for file in os.listdir(output_dir):
        if file.endswith('.md'):
            os.remove(os.path.join(output_dir, file))
    
    # Ordenar enseñanza por fecha (más reciente primero)
    teaching_experience = sorted(
        cv_data.get('teaching', []), 
        key=lambda x: x['startDate'], 
        reverse=True
    )
    
    for teaching in teaching_experience:
        title = teaching['title']['en']
        course = teaching.get('course', {})
        course_name = course.get('en', 'Course') if isinstance(course, dict) else str(course)
        start_date = teaching['startDate']
        end_date = teaching['endDate']
        
        filename = f"{start_date}-{sanitize_filename(course_name)}.md"
        filepath = os.path.join(output_dir, filename)
        institution = teaching.get('institution', 'Unknown Institution')
        if isinstance(institution, dict):
            institution = institution.get('en', 'Unknown Institution')
        else:
            institution = str(institution)
        teaching_type = teaching.get('type', 'Teaching Assistant')
        
        # Crear excerpt con responsabilidades
        responsibilities = []
        for desc in teaching.get('description', []):
            responsibilities.append(desc['en'])
        excerpt = ""
        
        # Front matter
        front_matter = {
            'title': f"{title} - {course_name}",
            'collection': 'teaching',
            'type': teaching_type,
            'permalink': f'/teaching/{start_date}-{sanitize_filename(course_name)}',
            'institution': institution,
            'date': f"{start_date}-01-01",
            'location': teaching['location'],
            'period': f"{start_date} - {end_date}",
            'course_name': course_name,
            'excerpt': excerpt
        }
        
        # Contenido simplificado sin duplicar información
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

### Responsibilities

"""
        
        for desc in teaching.get('description', []):
            content += f"* {desc['en']}\n"
        
        # Agregar tecnologías al final si existen
        if teaching.get('technologies'):
            content += f"""


<div class="archive__item-tags">
"""
            for tech in teaching['technologies']:
                content += f'  <span class="archive__tag">{tech}</span>\n'
            content += "</div>\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated teaching: {filename}")


def generate_teaching(cv_data, output_dir="_teaching"):
    """Genera archivos .md para experiencia docente"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Limpiar directorio existente
    for file in os.listdir(output_dir):
        if file.endswith('.md'):
            os.remove(os.path.join(output_dir, file))
    
    # Ordenar enseñanza por fecha (más reciente primero)
    teaching_experience = sorted(
        cv_data.get('teaching', []), 
        key=lambda x: x['startDate'], 
        reverse=True
    )
    
    for teaching in teaching_experience:
        title = teaching['title']['en']
        course = teaching.get('course', {})
        course_name = course.get('en', 'Course') if isinstance(course, dict) else str(course)
        start_date = teaching['startDate']
        end_date = teaching['endDate']
        
        filename = f"{start_date}-{sanitize_filename(course_name)}.md"
        filepath = os.path.join(output_dir, filename)
        institution = teaching.get('institution', 'Unknown Institution')
        if isinstance(institution, dict):
            institution = institution.get('en', 'Unknown Institution')
        else:
            institution = str(institution)
        teaching_type = teaching.get('type', 'Teaching Assistant')
        
        # Crear excerpt con responsabilidades
        responsibilities = []
        for desc in teaching.get('description', []):
            responsibilities.append(desc['en'])
        excerpt = ""
        
        # Front matter
        front_matter = {
            'title': f"{title} - {course_name}",
            'collection': 'teaching',
            'type': teaching_type,
            'permalink': f'/teaching/{start_date}-{sanitize_filename(course_name)}',
            'institution': institution,
            'date': f"{start_date}-01-01",
            'location': teaching['location'],
            'period': f"{start_date} - {end_date}",
            'course_name': course_name,
            'excerpt': excerpt
        }
        
        # Contenido simplificado sin duplicar información
        content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

### Responsibilities

"""
        
        for desc in teaching.get('description', []):
            content += f"* {desc['en']}\n"
        
        # Agregar tecnologías al final si existen
        if teaching.get('technologies'):
            content += f"""


<div class="archive__item-tags">
"""
            for tech in teaching['technologies']:
                content += f'  <span class="archive__tag">{tech}</span>\n'
            content += "</div>\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated teaching: {filename}")


def generate_cv_page(cv_data, output_file="_pages/cv.md"):
    """Genera la página de CV web"""
    front_matter = {
        'layout': 'archive',
        'title': 'Curriculum Vitae',
        'permalink': '/cv/',
        'author_profile': True,
        'redirect_from': ['/resume']
    }
    
    content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

<div class="cv-container">
  <div class="cv-header">
    <div class="cv-download-links">
      <a href="/files/CV.pdf" class="btn btn--primary" target="_blank">
        <i class="fa fa-file-pdf-o"></i> Download PDF CV
      </a>
      <a href="/files/Resume_Santiago_Martinez.pdf" class="btn btn--inverse" target="_blank">
        <i class="fa fa-file-text-o"></i> Download PDF Resume
      </a>
    </div>
  </div>
</div>
"""
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Generated CV page: {output_file}")

def generate_homepage(cv_data, output_file="_pages/about.md"):
    """Genera la página principal personalizada"""
    personal = cv_data['personal']
    
    # Crear biografía personalizada basada en el template de Sainyam
    name = personal['name']
    title = personal['title']['en']
    
    # Obtener información de educación más reciente
    education = cv_data.get('education', [])
    current_education = education[0] if education else {}
    
    # Obtener trabajo actual
    experience = cv_data.get('experience', [])
    current_work = experience[0] if experience else {}
    
    # Generar párrafo biográfico (adaptarlo a la información de Santiago)
    bio_paragraph = f"""I am a {title} currently pursuing my {current_education.get('degree', {}).get('en', 'M.Sc.')} at {current_education.get('institution', 'Universidad de los Andes')}. I work as a {current_work.get('title', {}).get('en', 'Research Assistant') if isinstance(current_work.get('title'), dict) else current_work.get('title', 'Research Assistant')} at {current_work.get('company', {}).get('en', current_work.get('company', '')) if isinstance(current_work.get('company'), dict) else current_work.get('company', '')}.

My research focuses on developing advanced natural language processing techniques and data-oriented tools for improving student support services in universities. I specialize in comparing highly-trained models against Large Language Models (LLMs) for Spanish linguistic tasks, and work on computer vision applications for medical imaging.

{personal['research_interests']['en']}"""
    
    # Obtener intereses de investigación para la sección de intereses
    interests = [
        "Natural Language Processing",
        "Large Language Models", 
        "Computer Vision",
        "Medical Imaging",
        "Data Science",
        "Machine Learning"
    ]
    
    # Crear contenido de la página
    front_matter = {
        'permalink': '/',
        'title': f"About me",
        'author_profile': True,
        'redirect_from': ['/about/', '/about.html']
    }
    
    content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

{bio_paragraph}

<div class="homepage-bottom">
  <div class="interests-education-container">
    <div class="interests-section">
      <h2><i class="fas fa-flask"></i> Research Interests</h2>
      <ul class="interests-list">
{chr(10).join([f"        <li class='interest-item'>{interest}</li>" for interest in interests])}
      </ul>
    </div>
    
    <div class="education-section">
      <h2><i class="fas fa-graduation-cap"></i> Education</h2>
"""
    
    # Agregar educación
    for edu in education:
        degree = edu['degree']['en']
        institution = edu['institution']
        status = "Expected" if edu['status'] == 'expected' else "Completed"
        gpa_line = f"<br><span class='gpa-line'>GPA: {edu['gpa']}</span>" if edu.get('gpa') else ""
        honors = ""
        if edu.get('honors'):
            honor_strings = [h.get('en', str(h)) if isinstance(h, dict) else str(h) for h in edu['honors']]
            honors = f" ({', '.join(honor_strings)})"
                
        content += f"""      <div class="education-item">
        <div class="degree-info">
          <i class="fas fa-university degree-icon"></i>
          <div class="degree-details">
            <strong class="degree-title">{degree}{honors}</strong><br>
            <span class="institution-name">{institution}</span><br>
            <span class="education-date">{edu['startDate']} - {edu['endDate']} | {status}</span>{gpa_line}
          </div>
        </div>
      </div>
"""
    
    # Agregar awards si existen
    awards = cv_data.get('awards', [])
    if awards:
        content += """
    </div>
  </div>
  
  <div class="awards-section">
    <h2><i class="fas fa-trophy"></i> Distinctions</h2>
    <div class="awards-grid">
"""
        for award in awards:
            content += f"""      <div class="award-item">
        <i class="fas fa-medal award-icon"></i>
        <div class="award-details">
          <strong class="award-title">{award['title']}</strong><br>
          <span class="award-institution">{award['institution']}</span> | <span class="award-date">{award['date']}</span>
        </div>
      </div>
"""
        content += "    </div>\n"
    
    content += """  </div>
</div>
"""
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Generated homepage: {output_file}")

def generate_data_files(cv_data, output_dir="_data"):
    """Genera archivos de datos para Jekyll"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generar cv.yml para Jekyll
    cv_yml_path = os.path.join(output_dir, "cv.yml")
    with open(cv_yml_path, 'w', encoding='utf-8') as f:
        yaml.dump(cv_data, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✅ Generated data file: {cv_yml_path}")

def generate_data_files(cv_data, output_dir="_data"):
    """Genera archivos de datos para Jekyll"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generar cv.yml para Jekyll
    cv_yml_path = os.path.join(output_dir, "cv.yml")
    with open(cv_yml_path, 'w', encoding='utf-8') as f:
        yaml.dump(cv_data, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✅ Generated data file: {cv_yml_path}")

def main():
    """Función principal"""
    try:
        with open('_data/cv.json', 'r', encoding='utf-8') as f:
            cv_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: cv.json not found!")
        print("Make sure the file is in the current directory.")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return
    
    print("🚀 Generating Academic Pages files from JSON...")
    
    # Generar todas las secciones
    generate_publications(cv_data)
    print("\n📚 Publications generated!")
    generate_talks(cv_data)
    print("\n🎤 Talks generated!")
    generate_experience(cv_data)  # Nueva sección
    print("\n💼 Experience (work + research) generated!")
    generate_teaching(cv_data)
    print("\n👨‍🏫 Teaching experience generated!")
    generate_homepage(cv_data)
    print("\n🏠 Homepage updated!")
    generate_cv_page(cv_data)  
    print("\n📄 CV web page generated!")
    generate_data_files(cv_data)
    print("\n📊 Data files for Jekyll generated!")
    
    
    print("\n✅ Generation complete!")



if __name__ == "__main__":
    main()