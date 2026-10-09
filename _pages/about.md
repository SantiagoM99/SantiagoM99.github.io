---
author_profile: true
permalink: /
redirect_from:
- /about/
- /about.html
title: About me
---


I am a Data Scientist at the EdTech Node of Universidad de los Andes, where I am also pursuing an M.Sc. in Information Engineering. My research focuses on multilingual NLP and multimodal systems that work for low-resource and underrepresented languages, with an emphasis on cross-lingual transfer and rigorous, culturally grounded evaluation. I pursue this line as a collaborating researcher at the Lee Language Lab (Ontario Tech University), which I joined through a Mitacs Globalink Research Internship.

In parallel, I build production data and machine learning systems for higher education: learning analytics, student-success prediction, and university-wide data products that support academic advising, work that has led to peer-reviewed publications at AIED and WEEF. More broadly, I care about human-centered AI that serves people, from underrepresented language communities to university classrooms.

In my free time, I enjoy playing chess and bowling.
    

<div class="homepage-bottom">
  <div class="interests-education-container">
    <div class="interests-section">
      <h2><i class="fas fa-flask"></i> Research Interests</h2>
      <ul class="interests-list">
        <li class='interest-item'>Multilingual NLP</li>
        <li class='interest-item'>Low-Resource Languages</li>
        <li class='interest-item'>Vision-Language Models</li>
        <li class='interest-item'>LLM Evaluation</li>
        <li class='interest-item'>Learning Analytics</li>
        <li class='interest-item'>Machine Learning</li>
      </ul>
    </div>
    
    <div class="education-section">
      <h2><i class="fas fa-graduation-cap"></i> Education</h2>
      <div class="education-item">
        <div class="degree-info">
          <i class="fas fa-university degree-icon"></i>
          <div class="degree-details">
            <strong class="degree-title">M.Sc. Information Engineering</strong><br>
            <span class="institution-name">Universidad de los Andes</span><br>
            <span class="education-date">2025 - 2026 | Expected</span><br><span class='gpa-line'>GPA: 4.80/5.00</span>
          </div>
        </div>
      </div>
      <div class="education-item">
        <div class="degree-info">
          <i class="fas fa-university degree-icon"></i>
          <div class="degree-details">
            <strong class="degree-title">B.Sc. Systems and Computing Engineering (Cum Laude)</strong><br>
            <span class="institution-name">Universidad de los Andes</span><br>
            <span class="education-date">2021 - 2024 | Completed</span><br><span class='gpa-line'>GPA: 4.58/5.00</span>
          </div>
        </div>
      </div>

    </div>
  </div>
  
  <div class="awards-section">
    <h2><i class="fas fa-trophy"></i> Distinctions</h2>
    <div class="award-list">
      {% comment %} Se genera desde _data/cv.json (awards), en el orden del JSON; el icono sale de `kind` {% endcomment %}
      {% for award in site.data.cv.awards %}
      <div class="award">
        <div class="award__year">{{ award.date | slice: 0, 4 }}</div>
        {% case award.kind %}
          {% when 'award' %}{% assign award_icon = 'fa-trophy' %}
          {% when 'fellowship' %}{% assign award_icon = 'fa-flask' %}
          {% else %}{% assign award_icon = 'fa-medal' %}
        {% endcase %}
        <i class="fas {{ award_icon }} award__icon" aria-hidden="true"></i>
        <div class="award__body">
          <p class="award__title"><strong>{{ award.title.en | default: award.title }}</strong> · <span class="award__institution">{{ award.institution.en | default: award.institution }}</span></p>
          {% if award.description_short %}<p class="award__why">{{ award.description_short.en }}</p>{% endif %}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>
