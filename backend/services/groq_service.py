import json
from groq import Groq
from utils.config import GROQ_MODEL, GROQ_MODEL_FAST

_current_api_key: str | None = None


def set_current_api_key(key: str):
    global _current_api_key
    _current_api_key = key.strip() if key else None


def _get_client() -> Groq:
    if not _current_api_key:
        raise ValueError("No Groq API key configured. Go to Settings in the app.")
    return Groq(api_key=_current_api_key)


def _safe_chat_completion(messages, temperature=0.7, max_tokens=4000, prefer_primary=True):
    from groq import RateLimitError, APIStatusError
    import time

    primary = GROQ_MODEL if prefer_primary else GROQ_MODEL_FAST
    fallback = GROQ_MODEL_FAST if prefer_primary else GROQ_MODEL

    # Calculo aproximado del tamaño del prompt
    prompt_size = sum(len(m.get('content', '')) for m in messages)
    estimated_tokens = prompt_size // 3

    # Si el prompt es muy grande, usar directamente el modelo grande
    if estimated_tokens > 5000 and prefer_primary:
        try:
            return _get_client().chat.completions.create(
                model=primary,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except RateLimitError:
            print(f"⚠️ Rate limit en {primary}, esperando 30s antes de reintentar...")
            time.sleep(30)
            try:
                return _get_client().chat.completions.create(
                    model=primary,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except Exception as e:
                raise Exception(f"Rate limit prolongado. Intenta en 1 minuto. Detalle: {e}")

    try:
        return _get_client().chat.completions.create(
            model=primary,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except RateLimitError:
        print(f"⚠️ Rate limit en {primary}, usando fallback {fallback}")
        try:
            return _get_client().chat.completions.create(
                model=fallback,
                messages=messages,
                temperature=temperature,
                max_tokens=min(max_tokens, 4000),
            )
        except (RateLimitError, APIStatusError) as e:
            print(f"⚠️ Fallback {fallback} también falló. Esperando 20s y reintentando primario...")
            time.sleep(20)
            return _get_client().chat.completions.create(
                model=primary,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )


def _lang_name(language: str) -> str:
    return "English" if language == "en" else "Spanish"


def _norm_lang(language) -> str:
    if not language:
        return "es"
    code = str(language).lower().strip()
    return "en" if code == "en" else "es"

def _difficulty_instruction(difficulty: str, seniority: str, lang: str) -> str:
    d = (difficulty or "similar").lower().strip()
    if lang == 'en':
        if d == 'easier':
            return (f"DIFFICULTY: Make this question EASIER than the previous one. "
                    f"The candidate is being evaluated for {seniority}, but this specific question should test "
                    f"more fundamental concepts. Use a simpler scenario, fewer technical layers, and concepts a less experienced "
                    f"developer would still handle. The bar is LOWER than the previous question.")
        if d == 'harder':
            return (f"DIFFICULTY: Make this question HARDER than the previous one. "
                    f"Push the candidate beyond the {seniority} baseline. Add more complexity: edge cases, "
                    f"performance tradeoffs, architectural implications, multi-step reasoning, or production scenarios "
                    f"with conflicting constraints. The bar is HIGHER than the previous question.")
        return (f"DIFFICULTY: Keep similar complexity to the previous question, matched to {seniority} level. "
                f"Same depth, different angle.")
    else:
        if d == 'easier':
            return (f"DIFICULTAD: Haz esta pregunta MÁS FÁCIL que la anterior. "
                    f"El candidato es evaluado como {seniority}, pero esta pregunta específica debe probar "
                    f"conceptos más fundamentales. Usa un escenario más simple, menos capas técnicas y conceptos que un developer "
                    f"con menos experiencia también podría manejar. La vara es MÁS BAJA que la pregunta anterior.")
        if d == 'harder':
            return (f"DIFICULTAD: Haz esta pregunta MÁS DIFÍCIL que la anterior. "
                    f"Lleva al candidato más allá de la línea base de {seniority}. Agrega más complejidad: edge cases, "
                    f"tradeoffs de performance, implicaciones de arquitectura, razonamiento multi-paso, o escenarios de producción "
                    f"con restricciones contradictorias. La vara es MÁS ALTA que la pregunta anterior.")
        return (f"DIFICULTAD: Mantén complejidad similar a la pregunta anterior, acorde al nivel {seniority}. "
                f"Misma profundidad, otro ángulo.")


# Preguntas de la entrevista
def generate_interview_questions(candidate: dict, language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)
    print(f"SERVICE LANG: language={language} | normalized={lang} | name={lang_name}")

    role_name = candidate.get('role_name', '').strip()
    mode = candidate.get('mode', 'general')
    seniority = candidate.get('seniority', 'Mid')
    years = candidate.get('experience_years', 0)
    total_questions = candidate.get('total_questions', 8)
    questions_per_skill = candidate.get('questions_per_skill', 3)
    include_behavioral = candidate.get('include_behavioral', True)
    axis_questions = candidate.get('axis_questions', {})
    selected_context = candidate.get('selected_skills_context', [])
    skills = candidate.get('selected_skills', candidate.get('skills', []))
    role_description = candidate.get('role_description', '').strip()
    fit_analysis = candidate.get('fit_analysis') or {}
    fit_gaps = fit_analysis.get('gaps', []) if fit_analysis else []
    fit_highlights = fit_analysis.get('highlights_from_cv', []) if fit_analysis else []
    fit_score = fit_analysis.get('fit_score', 0) if fit_analysis else 0

    if not role_name:
        fallback_area = candidate.get('area', 'technology' if lang == 'en' else 'tecnología')
        role_name = (
            f"{fallback_area} professional" if lang == 'en'
            else f"profesional de {fallback_area}"
        )

    sen_lower = seniority.lower()
    if lang == 'en':
        if 'junior' in sen_lower:
            depth = "basic and conceptual, ideal for someone starting out"
            seniority_examples = "JUNIOR EXAMPLES: 'What is a primary key in a database?', 'Explain the difference between var and let in JavaScript', 'What does HTTP status code 404 mean?'. Avoid complex architecture questions, system design, or leadership scenarios."
        elif 'principal' in sen_lower or 'architect' in sen_lower:
            depth = "strategic and architectural, about system decisions, tradeoffs and technical vision"
            seniority_examples = "PRINCIPAL/ARCHITECT EXAMPLES: 'Design a multi-region active-active system for a financial platform with strict consistency requirements. What tradeoffs would you make?', 'How would you migrate a 10-year-old monolith with 200 engineers to microservices without halting business?'. Questions MUST involve large-scale tradeoffs, organizational impact, and technical vision."
        elif 'lead' in sen_lower:
            depth = "about technical leadership, mentorship, decision making and team management"
            seniority_examples = "LEAD EXAMPLES: 'You have a junior dev consistently pushing low-quality PRs despite reviews. How do you handle it?', 'Your team wants to adopt a new framework but it would delay the roadmap 2 months. How do you decide?'. Questions MUST blend technical depth with team/mentorship/decision-making."
        elif 'senior' in sen_lower:
            depth = "advanced and deep, evaluating architecture, design decisions and technical leadership"
            seniority_examples = "SENIOR EXAMPLES: 'You need to add caching to a high-traffic API. Walk me through your decision between Redis, Memcached, or in-process cache, and what invalidation strategy you would choose.', 'Explain how you would refactor a 5000-line legacy class without breaking production'. Questions MUST require architecture decisions, tradeoffs, and explaining the 'why', not just the 'what'."
        else:
            depth = "intermediate, evaluating practical application and real problem solving"
            seniority_examples = "MID EXAMPLES: 'How would you implement pagination on an endpoint that returns thousands of records?', 'Describe a bug you solved that required reading library source code'. Questions MUST go beyond basics but not require deep system design — focus on practical implementation and problem solving."
    else:
        if 'junior' in sen_lower:
            depth = "básicas y conceptuales, ideales para alguien que está comenzando"
            seniority_examples = "EJEMPLOS JUNIOR: '¿Qué es una primary key en una base de datos?', 'Explica la diferencia entre var y let en JavaScript', '¿Qué significa el código HTTP 404?'. Evita preguntas de arquitectura compleja, diseño de sistemas o escenarios de liderazgo."
        elif 'principal' in sen_lower or 'architect' in sen_lower:
            depth = "estratégicas y arquitectónicas, sobre decisiones de sistema, tradeoffs y visión técnica"
            seniority_examples = "EJEMPLOS PRINCIPAL/ARCHITECT: 'Diseña un sistema activo-activo multi-región para una plataforma financiera con requisitos estrictos de consistencia. ¿Qué tradeoffs harías?', '¿Cómo migrarías un monolito de 10 años con 200 ingenieros a microservicios sin parar el negocio?'. Las preguntas DEBEN involucrar tradeoffs a gran escala, impacto organizacional y visión técnica."
        elif 'lead' in sen_lower:
            depth = "de liderazgo técnico, mentoría, toma de decisiones y gestión de equipo"
            seniority_examples = "EJEMPLOS LEAD: 'Tienes un junior que insistentemente envía PRs de baja calidad a pesar de los reviews. ¿Cómo lo manejas?', 'Tu equipo quiere adoptar un nuevo framework pero retrasaría el roadmap 2 meses. ¿Cómo decides?'. Las preguntas DEBEN combinar profundidad técnica con equipo/mentoría/toma de decisiones."
        elif 'senior' in sen_lower:
            depth = "avanzadas y profundas, que evalúen arquitectura, decisiones de diseño y liderazgo técnico"
            seniority_examples = "EJEMPLOS SENIOR: 'Necesitas agregar caché a una API de alto tráfico. Explícame tu decisión entre Redis, Memcached o caché en proceso, y qué estrategia de invalidación elegirías.', 'Explica cómo refactorizarías una clase legacy de 5000 líneas sin romper producción'. Las preguntas DEBEN requerir decisiones de arquitectura, tradeoffs, y explicar el 'por qué', no solo el 'qué'."
        else:
            depth = "intermedias, que evalúen aplicación práctica y resolución de problemas reales"
            seniority_examples = "EJEMPLOS MID: '¿Cómo implementarías paginación en un endpoint que devuelve miles de registros?', 'Describe un bug que resolviste que requirió leer código fuente de una librería'. Las preguntas DEBEN ir más allá de lo básico pero sin requerir diseño de sistemas profundo — enfócate en implementación práctica y resolución de problemas."

    if selected_context:
        limited = selected_context[:30]
        if lang == 'en':
            skills_context = "\n".join([
                f"- {s['name']} (in the context of {s['category']})"
                for s in limited
            ])
        else:
            skills_context = "\n".join([
                f"- {s['name']} (en contexto de {s['category']})"
                for s in limited
            ])
    else:
        skills_context = ", ".join(skills[:30]) if skills else (
            "not specified" if lang == 'en' else "no especificadas"
        )

    if mode == 'by_skill' and selected_context:
        total = len(selected_context) * questions_per_skill
        if lang == 'en':
            mode_instruction = (
                f"Generate {questions_per_skill} specific questions PER selected skill. "
                f"Total: {total} technical questions. "
                f"Adapt each question to the skill's category context "
                f"(e.g.: Linux in DevOps vs Linux in Networking yield different questions)."
            )
        else:
            mode_instruction = (
                f"Genera {questions_per_skill} preguntas específicas POR CADA skill seleccionado. "
                f"Total: {total} preguntas técnicas. "
                f"Adapta cada pregunta al contexto de categoría del skill "
                f"(ej: Linux en DevOps vs Linux en Networking generan preguntas distintas)."
            )
    else:
        if lang == 'en':
            mode_instruction = (
                f"Generate {total_questions} mixed technical questions based on the role "
                f"'{role_name}' and the candidate's skills."
            )
        else:
            mode_instruction = (
                f"Genera {total_questions} preguntas técnicas mixtas basadas en el rol "
                f"'{role_name}' y los skills del candidato."
            )

    axis_instruction = ""
    behavioral_count = 0
    if include_behavioral and axis_questions:
        active_axes = {k: v for k, v in axis_questions.items() if v > 0}
        if active_axes:
            behavioral_count = sum(active_axes.values())
            required_questions = []
            for axis, count in active_axes.items():
                for i in range(count):
                    required_questions.append(axis)

            numbered = "\n".join([
                f"   {i+1}. One question with axis = \"{axis}\""
                for i, axis in enumerate(required_questions)
            ])

            axis_instruction = f"""

=== BEHAVIORAL QUESTIONS — MANDATORY ===
You MUST generate EXACTLY {behavioral_count} behavioral questions, no more, no less.
Here is the EXACT list of behavioral questions to generate:
{numbered}

Each behavioral question's "axis" field must match EXACTLY the value specified above
(Communication, Cultural Fit, English, Workable, or Leadership — in English, never translated).
The "behavioral_questions" array MUST contain EXACTLY {behavioral_count} items following this list in order."""

    fit_block = ""
    if fit_gaps or fit_highlights:
        gaps_text = "\n".join([f"- {g}" for g in fit_gaps[:5]]) if fit_gaps else "(none detected)"
        highlights_text = "\n".join([f"- {h}" for h in fit_highlights[:5]]) if fit_highlights else "(none detected)"
        if lang == 'en':
            fit_block = f"""

=== FIT ANALYSIS — USE TO TARGET WEAK SPOTS ===
An AI fit analysis was performed (fit_score: {fit_score}%). Use this data to make the interview RIGOROUS.

DETECTED GAPS (areas where the CV does NOT clearly demonstrate the required skills):
{gaps_text}

CV HIGHLIGHTS (areas where the candidate shows strength):
{highlights_text}

MANDATORY RULES:
1. AT LEAST 30% of the technical questions MUST directly target the DETECTED GAPS above. Pick the most critical gaps and craft questions that force the candidate to demonstrate (or fail to demonstrate) competence in those areas.
2. AT LEAST 20% of the questions should challenge the HIGHLIGHTS — go deeper than what the CV claims. If the CV says "expert in X", ask a hard question about X to verify that depth.
3. Gap-targeted questions should be designed to be UNCOMFORTABLE if the candidate truly lacks the skill. They should not be trivially answerable with surface knowledge.
4. Do NOT label questions as "gap question" or "highlight question" — they should feel like normal technical questions, just strategically chosen.
"""
        else:
            fit_block = f"""

=== ANÁLISIS DE FIT — APROVÉCHALO PARA APUNTAR A PUNTOS DÉBILES ===
Se realizó un análisis de fit por IA (fit_score: {fit_score}%). Usa estos datos para hacer la entrevista RIGUROSA.

GAPS DETECTADOS (áreas donde el CV NO demuestra claramente las habilidades requeridas):
{gaps_text}

HIGHLIGHTS DEL CV (áreas donde el candidato muestra fortaleza):
{highlights_text}

REGLAS OBLIGATORIAS:
1. AL MENOS el 30% de las preguntas técnicas DEBEN apuntar directamente a los GAPS DETECTADOS arriba. Elige los gaps más críticos y diseña preguntas que obliguen al candidato a demostrar (o no poder demostrar) competencia en esas áreas.
2. AL MENOS el 20% de las preguntas deben CUESTIONAR los HIGHLIGHTS — ve más profundo de lo que dice el CV. Si el CV dice "experto en X", haz una pregunta difícil de X para verificar esa profundidad.
3. Las preguntas dirigidas a gaps deben estar diseñadas para ser INCÓMODAS si el candidato realmente carece de la habilidad. No deben responderse trivialmente con conocimiento superficial.
4. NO etiquetes las preguntas como "pregunta de gap" o "pregunta de highlight" — deben sentirse como preguntas técnicas normales, solo elegidas estratégicamente.
"""

    if lang == 'en':
        bad_q = '"What is OAuth?"'
        good_q = '"Imagine your mobile app must allow login with Google and Facebook. Explain step by step how you would implement OAuth2 for this and what security risks you must consider."'
        bad_exc = '"Demonstrates deep knowledge"'
        good_exc = '"Mentions PKCE flow, refresh token handling, specific scopes, and at least one known attack such as CSRF on the redirect."'
        good_avg = '"Explains the basic OAuth flow but does not mention PKCE or discuss token security."'
        good_weak = '"Only says \'it is for social network login\' without understanding the token flow or does not differentiate OAuth from OpenID."'
        bad_rf = '"Use of buzzwords without understanding"'
        good_rf = '"Confuses OAuth with pure authentication (it is authorization). Says \'JWT is the same as OAuth\'. Cannot explain what happens if a refresh token leaks."'
    else:
        bad_q = '"¿Qué es OAuth?"'
        good_q = '"Imagina que tu app móvil debe permitir login con Google y Facebook. Explica paso a paso cómo implementarías OAuth2 para esto y qué riesgos de seguridad debes considerar."'
        bad_exc = '"Demuestra conocimiento profundo"'
        good_exc = '"Menciona PKCE flow, manejo de refresh tokens, scopes específicos, y al menos un ataque conocido como CSRF en el redirect."'
        good_avg = '"Explica el flujo básico de OAuth pero no menciona PKCE ni discute seguridad de tokens."'
        good_weak = '"Solo dice \'es para login con redes sociales\' sin entender el flujo de tokens o no diferencia OAuth de OpenID."'
        bad_rf = '"Uso de buzzwords sin comprensión"'
        good_rf = '"Confunde OAuth con autenticación pura (es autorización). Dice \'JWT es lo mismo que OAuth\'. No puede explicar qué pasa si un refresh token se filtra."'

    role_desc_block = ""
    if role_description:
        if lang == 'en':
            role_desc_block = f"""
DETAILED ROLE DESCRIPTION (provided by interviewer):
{role_description[:1500]}

IMPORTANT: Tailor your questions to the specific requirements and responsibilities mentioned in this role description.
"""
        else:
            role_desc_block = f"""
DESCRIPCIÓN DETALLADA DEL ROL (proporcionada por el entrevistador):
{role_description[:1500]}

IMPORTANTE: Adapta tus preguntas a los requisitos y responsabilidades específicos mencionados en esta descripción.
"""

    prompt = f"""
You are an expert technical interviewer creating questions for a NON-TECHNICAL recruiter.

CRITICAL: The recruiter conducting this interview may NOT know the technical subject deeply.
ALL guidance must be SPECIFIC, CONCRETE, and ACTIONABLE — not generic.

=== ORAL INTERVIEW — NOT A TAKE-HOME EXAM ===
Every question will be SPOKEN OUT LOUD in a live conversation. The candidate must be able to ANSWER VERBALLY in 1-3 minutes.

PREFERRED QUESTION STYLES (use these often):

1. HYPOTHETICAL SCENARIOS — paint a concrete situation, then ask what they would do:
   - "Imagine your team has X problem. How would you approach it?"
   - "Suppose a junior developer asks you Y. What would you tell them?"
   - "In a hypothetical case where you have to choose between A and B with these constraints, which would you pick and why?"
   - "Picture this: production is down because of X. What's your first move?"

2. DECISION-BASED QUESTIONS — force tradeoff reasoning:
   - "How would you decide between X and Y for [specific use case]?"
   - "What factors would you weigh when choosing X over Y?"

3. EXPERIENCE-BASED QUESTIONS — let them tell stories:
   - "Tell me about a time when you had to..."
   - "Describe a situation where you faced X."

4. EXPLANATION QUESTIONS — verify depth of understanding:
   - "Explain how X works under the hood."
   - "Walk me through your understanding of Y."

FORBIDDEN verbs and phrasings (NEVER use these):
- "Develop a..." / "Desarrolla un..."
- "Implement a..." / "Implementa un..."
- "Write code that..." / "Escribe código que..."
- "Code a function..." / "Programa una función..."
- "Build an application..." / "Construye una aplicación..."
- "Design and code..." / "Diseña y programa..."

USE THESE verbs instead:
- "Explain how you would..." / "Explica cómo harías..."
- "Walk me through your approach to..." / "Cuéntame tu enfoque para..."
- "Describe step by step how..." / "Describe paso a paso cómo..."
- "What would you do if..." / "¿Qué harías si...?"
- "How would you decide between..." / "¿Cómo decidirías entre...?"
- "Talk me through..." / "Explícame..."

Every question must be answerable through SPEECH, citing concepts, decisions, tradeoffs, and reasoning — not by writing code or building artifacts.

CANDIDATE PROFILE:
- Role: {role_name}
- Seniority level: {seniority}
- Skills to evaluate:
{skills_context}
{role_desc_block}
MODE: {mode_instruction}
{fit_block}

=== SENIORITY IS THE PRIMARY DRIVER ===
The candidate is being evaluated for a {seniority} position.
The technical questions must be {depth}.

{seniority_examples}

CRITICAL RULES BY SENIORITY:
- Years of experience are CONTEXT, NOT the determining factor. A candidate with 8 years of experience applying for a JUNIOR role gets JUNIOR questions. A candidate with 2 years applying for a SENIOR role still gets SENIOR questions.
- Every single technical question MUST feel appropriate for the {seniority} level. If a question could be asked to any level, it is TOO GENERIC.
- A Senior question is NOT just "harder", it requires architectural thinking and tradeoff analysis.
- A Junior question is NOT just "easier", it tests fundamentals without expecting design experience.
- A Lead/Principal question MUST include team/business/organizational dimensions, not just code.
{axis_instruction}

REMINDER: The behavioral_questions array must contain EXACTLY {behavioral_count} questions if behavioral questions were requested above. Follow the exact axis distribution.

REQUIREMENTS FOR EACH QUESTION:

1. **question** (REQUIRED): Detailed and contextual. Minimum 2 sentences when possible.
   Include scenario or context, not just a one-line question.
   BAD: {bad_q}
   GOOD: {good_q}

2. **expected_answer**: A complete ideal answer, 3-5 sentences. Specific technical content.

3. **excellent_guide**: Concrete things the candidate SHOULD mention (use specific terms, examples, names of tools/patterns).
   BAD: {bad_exc}
   GOOD: {good_exc}

4. **average_guide**: What an OK but limited answer looks like. Be concrete.
   GOOD: {good_avg}

5. **weak_guide**: What a poor answer looks like. Be concrete.
   GOOD: {good_weak}

6. **suggested_red_flags**: 2-4 SPECIFIC red flags tied to THIS exact question. STRICT RULES:
   - Each red flag MUST be a complete sentence (15+ words minimum), describing a specific incorrect statement, confusion, or wrong reasoning the candidate might exhibit.
   - Each red flag MUST be CLEARLY DIFFERENT from the others — no paraphrases, no rewording of the same idea.
   - Each red flag MUST cite specific technical concepts, terms, or wrong patterns (not "lacks knowledge", not "is unclear", not "uses buzzwords").
   - If the question is about X, the red flags must describe specific wrong things someone might say about X — different categories of wrong.
   - One red flag = one distinct failure pattern. Don't just rewrite the same flaw with different words.
   BAD examples (DO NOT generate these):
     - "Lacks understanding"
     - "Cannot explain properly"
     - "Uses buzzwords without comprehension"
     - "Has surface-level knowledge"
   {bad_rf}
   GOOD examples (this is the bar):
     {good_rf}
     "Mentions JWT and OAuth interchangeably without distinguishing that JWT is a token format and OAuth is an authorization protocol."
     "Cannot describe what 'state' parameter does in the OAuth redirect, suggesting they have never implemented OAuth defensively against CSRF."
     "Confuses access_token expiration with session expiration, indicating they have never debugged token refresh flows in production."

7. **competency**: Specific competency name (e.g.: "Authentication & Authorization", "API Security", "Database Design")

Generate EXACTLY this JSON in {lang_name}, nothing else:
{{
    "technical_questions": [
        {{
            "question": "...",
            "expected_answer": "...",
            "skill": "...",
            "category": "...",
            "axis": "Technical",
            "competency": "...",
            "excellent_guide": "...",
            "average_guide": "...",
            "weak_guide": "...",
            "suggested_red_flags": ["specific red flag 1", "specific red flag 2", "specific red flag 3"]
        }}
    ],
    "behavioral_questions": [
        {{
            "question": "...",
            "expected_answer": "...",
            "skill": "",
            "category": "",
            "axis": "Communication | Cultural Fit | English | Workable (use EXACT requested distribution)",
            "competency": "...",
            "excellent_guide": "...",
            "average_guide": "...",
            "weak_guide": "...",
            "suggested_red_flags": ["...", "..."]
        }}
    ],
    "interview_focus": "..."
}}

ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with the JSON.
"""

    response = _safe_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=12000,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]

    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON incompleto en generate_interview_questions: {e}")
        # Intentar recuperar cerrando el JSON manualmente
        try:
            last_valid = content.rfind('}')
            if last_valid > 0:
                truncated = content[:last_valid + 1]
                open_braces = truncated.count('{') - truncated.count('}')
                open_brackets = truncated.count('[') - truncated.count(']')
                fixed = truncated + '}' * open_braces + ']' * open_brackets
                return json.loads(fixed)
        except Exception:
            pass
        raise Exception(
            "El modelo devolvió una respuesta incompleta. "
            "Prueba con menos preguntas totales o menos skills seleccionados."
        )


# Reporte basico (mas adelante lo reemplace por el mejorado empresarial, pero lo dejo por si acasito)
def generate_report(candidate: dict, scores: dict, language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    technical_score = scores.get('technical_score', 0)
    behavioral_score = scores.get('behavioral_score', 0)
    overall_score = scores.get('overall_score', 0)
    questions_detail = scores.get('questions_detail', [])

    if lang == 'en':
        if overall_score >= 4:
            recommendation = "Highly recommended"
        elif overall_score >= 3:
            recommendation = "Recommended"
        elif overall_score >= 2:
            recommendation = "Consider with reservations"
        else:
            recommendation = "Not recommended"
    else:
        if overall_score >= 4:
            recommendation = "Altamente recomendado"
        elif overall_score >= 3:
            recommendation = "Recomendado"
        elif overall_score >= 2:
            recommendation = "A considerar con reservas"
        else:
            recommendation = "No recomendado"

    prompt = f"""
You are an expert HR consultant writing a professional candidate evaluation report in {lang_name}.

Candidate data:
- Area: {candidate.get('area', '')}
- Seniority: {candidate.get('seniority', '')}
- Experience: {candidate.get('experience_years', 0)} years
- Skills: {', '.join(candidate.get('skills', []))}
- Technical score: {technical_score:.1f}/5
- Behavioral score: {behavioral_score:.1f}/5
- Overall score: {overall_score:.1f}/5
- Recommendation: {recommendation}

Questions and scores:
{chr(10).join([f"- {q['question']} → Score: {q.get('score', 'N/A')}/5" for q in questions_detail if q.get('score')])}

Write a professional evaluation report. Generate EXACTLY this JSON in {lang_name}, nothing else:
{{
    "executive_summary": "2-3 sentences summarizing the candidate",
    "technical_evaluation": "2-3 sentences about technical performance",
    "behavioral_evaluation": "2-3 sentences about behavioral performance",
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "areas_for_improvement": ["area 1", "area 2"],
    "recommendation": "{recommendation}",
    "recommendation_detail": "3-4 sentences justifying the recommendation",
    "suitable_roles": ["role 1", "role 2", "role 3"]
}}

ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with the JSON.
"""

    response = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=2500,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    return json.loads(content.strip())


# Regenerar una pregunta
def regenerate_single_question(payload: dict, language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    role = payload.get('role_name', '') or ('technical professional' if lang == 'en' else 'profesional técnico')
    seniority = payload.get('seniority', 'Mid')
    years = payload.get('experience_years', 0)
    skill = payload.get('skill', '')
    category = payload.get('category', '')
    axis = payload.get('axis', 'Technical')
    competency = payload.get('competency', '')
    previous = payload.get('previous_question', '')
    difficulty = payload.get('difficulty', 'similar')

    prompt = f"""
Generate ONE alternative interview question in {lang_name}.

Context:
- Role: {role}
- Seniority: {seniority}
- Experience: {years} years
- Skill: {skill}
- Category: {category}
- Axis: {axis}
- Competency: {competency}

The previous question was:
"{previous}"

Generate a DIFFERENT question that evaluates the same skill/competency but from another angle.
{_difficulty_instruction(difficulty, seniority, lang)}

CRITICAL: This is an ORAL interview question. The candidate must answer VERBALLY in 1-3 minutes.
NEVER use verbs like "develop", "implement", "code", "write", "build" — use "explain", "describe", "walk me through", "how would you" instead.

Return EXACTLY this JSON, nothing else:
{{
    "question": "...",
    "expected_answer": "...",
    "skill": "{skill}",
    "category": "{category}",
    "axis": "{axis}",
    "competency": "{competency}",
    "excellent_guide": "...",
    "average_guide": "...",
    "weak_guide": "...",
    "suggested_red_flags": ["...", "..."]
}}

ALL TEXT MUST BE IN {lang_name.upper()}.
"""

    response = _safe_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=2500,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    return json.loads(content.strip())


# Reporte generado
def generate_enterprise_report(candidate, setup, axis_scores, questions_detail, weighted_score, stats, post_notes=None, language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    role = setup.get('role_name', '') or candidate.get('area', 'N/A')
    candidate_name = setup.get('candidate_name', '').strip() or ('the candidate' if lang == 'en' else 'el candidato')
    declared_sen = setup.get('declared_seniority', candidate.get('seniority', 'Mid'))
    ai_sen = setup.get('ai_detected_seniority', candidate.get('seniority', ''))
    final_score = weighted_score.get('final_score', 0)

    if lang == 'en':
        if final_score >= 4.2:
            recommendation = "Advance immediately"
        elif final_score >= 3.3:
            recommendation = "Advance with reservations"
        elif final_score >= 2.5:
            recommendation = "Requires discussion"
        else:
            recommendation = "Do not advance"
    else:
        if final_score >= 4.2:
            recommendation = "Avanzar inmediatamente"
        elif final_score >= 3.3:
            recommendation = "Avanzar con reservas"
        elif final_score >= 2.5:
            recommendation = "Requiere discusión"
        else:
            recommendation = "No avanzar"

    answer_label = "Answer" if lang == 'en' else "Respuesta"
    note_label = "Note" if lang == 'en' else "Nota"
    general_label = "General" if lang == 'en' else "General"

    evidence_lines = []
    for q in questions_detail:
        if q.get('skipped'):
            continue
        score = q.get('score')
        if score is None:
            continue
        line = f"- [{q.get('skill', general_label)}] {q.get('question', '')[:80]}... → {score}/5"
        if q.get('answer_note'):
            line += f" | {answer_label}: {q['answer_note'][:120]}"
        if q.get('interviewer_note'):
            line += f" | {note_label}: {q['interviewer_note'][:120]}"
        evidence_lines.append(line)

    evidence_text = "\n".join(evidence_lines[:20])

    axis_text = "\n".join([
        f"- {axis}: {score:.1f}/5"
        for axis, score in axis_scores.items() if score > 0
    ])

    seniority_note = ""
    if declared_sen.lower() != ai_sen.lower() and ai_sen:
        seniority_note = f"\nIMPORTANT: There is a seniority discrepancy. Interviewer declared '{declared_sen}' but AI detected '{ai_sen}' from CV. Address this in the report."

    cv_text_raw = candidate.get('cv_text', '')
    cv_summary = {}
    if cv_text_raw.strip():
        try:
            cv_summary = summarize_cv(cv_text_raw, role_context=role, language=lang)
        except Exception:
            cv_summary = {}

    cv_context_lines = []
    if lang == 'en':
        if cv_summary.get('summary'):
            cv_context_lines.append(f"Professional summary: {cv_summary['summary']}")
        if cv_summary.get('education'):
            cv_context_lines.append(f"Education: {cv_summary['education']}")
        if cv_summary.get('experience_summary'):
            cv_context_lines.append(f"Experience: {cv_summary['experience_summary']}")
        if cv_summary.get('key_projects'):
            cv_context_lines.append(f"Key projects: {', '.join(cv_summary['key_projects'])}")
        if cv_summary.get('certifications'):
            cv_context_lines.append(f"Certifications: {', '.join(cv_summary['certifications'])}")
        if cv_summary.get('languages'):
            cv_context_lines.append(f"Languages: {', '.join(cv_summary['languages'])}")
        cv_block = "\n".join(cv_context_lines) if cv_context_lines else "(CV not available)"
    else:
        if cv_summary.get('summary'):
            cv_context_lines.append(f"Resumen profesional: {cv_summary['summary']}")
        if cv_summary.get('education'):
            cv_context_lines.append(f"Educación: {cv_summary['education']}")
        if cv_summary.get('experience_summary'):
            cv_context_lines.append(f"Experiencia: {cv_summary['experience_summary']}")
        if cv_summary.get('key_projects'):
            cv_context_lines.append(f"Proyectos clave: {', '.join(cv_summary['key_projects'])}")
        if cv_summary.get('certifications'):
            cv_context_lines.append(f"Certificaciones: {', '.join(cv_summary['certifications'])}")
        if cv_summary.get('languages'):
            cv_context_lines.append(f"Idiomas: {', '.join(cv_summary['languages'])}")
        cv_block = "\n".join(cv_context_lines) if cv_context_lines else "(CV no disponible)"

    post_notes = post_notes or {}
    final_comments = post_notes.get('final_comments', '').strip()
    candidate_qs = post_notes.get('candidate_questions', [])

    post_section = ""
    if final_comments:
        post_section += f"\n\nINTERVIEWER FINAL COMMENTS:\n{final_comments}"
    if candidate_qs:
        cq_text = "\n".join([
            f"- Q: {q.get('question', '')}\n  A: {q.get('answer', '')}"
            for q in candidate_qs if q.get('question')
        ])
        if cq_text:
            post_section += f"\n\nQUESTIONS THE CANDIDATE ASKED (and interviewer's answers):\n{cq_text}\nUse this to evaluate the candidate's curiosity, maturity, and interest level."

    prompt = f"""
You are a senior HR consultant writing a professional enterprise candidate evaluation report in {lang_name}.

CV ANALYZED BY AI (structured summary):
{cv_block}

CANDIDATE DATA:
- Candidate name: {candidate_name}
- Role applied: {role}
- Declared seniority: {declared_sen}
- AI-detected seniority: {ai_sen}
- Experience: {candidate.get('experience_years', 0)} years
- Skills: {', '.join(candidate.get('skills', []))}
- Final weighted score: {final_score}/5
- Recommendation level: {recommendation}{seniority_note}

SCORES BY AXIS:
{axis_text}

EVIDENCE (questions, scores, candidate answers, interviewer notes):
{evidence_text}{post_section}

INTERVIEW STATS:
- Questions skipped: {stats.get('skipped', 0)}
- Questions regenerated: {stats.get('regenerated', 0)}

Write a complete professional report. Generate EXACTLY this JSON in {lang_name}, nothing else:
{{
    "executive_summary": "3-4 sentences synthesizing {candidate_name} based on REAL evidence above. Use the candidate's name naturally in the narrative",
    "technical_evaluation": "3-4 sentences about technical performance citing specific skills and scores",
    "behavioral_evaluation": "2-3 sentences about soft skills/communication based on evidence",
    "seniority_analysis": "2-3 sentences analyzing the declared vs detected seniority and what the evidence suggests",
    "strengths": ["specific strength based on evidence", "another", "another"],
    "areas_for_improvement": ["specific area based on evidence", "another"],
    "red_flags": ["any concrete concern found in evidence, or empty if none"],
    "recommendation": "{recommendation}",
    "recommendation_detail": "4-5 sentences justifying the recommendation citing the weighted score and key evidence",
    "suitable_roles": ["role based on profile", "another", "another"]
}}

ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with the JSON.
"""

    response = _safe_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=3000,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    result = json.loads(content.strip())
    result['cv_summary'] = cv_summary
    return result


# Resumen del cv
def summarize_cv(cv_text: str, role_context: str = "", language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    if not cv_text or len(cv_text.strip()) < 50:
        return {
            "summary": "",
            "education": "",
            "experience_summary": "",
            "key_projects": [],
            "certifications": [],
            "languages": [],
        }

    cv_input = cv_text[:8000]

    if lang == 'en':
        context_line = f"Context: candidate is being evaluated for the role of {role_context}." if role_context else ""
    else:
        context_line = f"Contexto: el candidato está siendo evaluado para el rol de {role_context}." if role_context else ""

    prompt = f"""
You are a CV parser. Extract structured key information from this CV in {lang_name}.
{context_line}

CV:
{cv_input}

Return EXACTLY this JSON in {lang_name}, nothing else:
{{
    "summary": "2-3 sentence professional summary highlighting strongest qualifications",
    "education": "highest education + institution (1 line)",
    "experience_summary": "2-3 sentences about work experience trajectory",
    "key_projects": ["project 1 if mentioned", "project 2 if mentioned"],
    "certifications": ["cert 1", "cert 2"],
    "languages": ["language 1", "language 2"]
}}

If a field is not present in the CV, use empty string or empty array. ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with JSON.
"""

    response = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    try:
        return json.loads(content.strip())
    except Exception:
        return {
            "summary": "",
            "education": "",
            "experience_summary": "",
            "key_projects": [],
            "certifications": [],
            "languages": [],
        }


# Skills que se detecta
def detect_skills_from_cv(cv_text: str, known_skills: list = None, known_categories: list = None, language: str = "es") -> dict:
    lang = _norm_lang(language)

    if not cv_text or len(cv_text.strip()) < 50:
        return {"skills_by_category": {}, "skills": []}

    if lang == 'en':
        known_skills_str = ', '.join(known_skills) if known_skills else 'none'
    else:
        known_skills_str = ', '.join(known_skills) if known_skills else 'ninguna'

    valid_categories = known_categories or [
        'Backend', 'Frontend', 'Mobile', 'Database', 'DevOps',
        'Cloud Computing', 'Networking', 'SysAdmin', 'Infraestructura',
        'Soporte Técnico', 'Data Science', 'QA', 'Seguridad', 'Diseño', 'Fullstack'
    ]
    categories_str = ', '.join(valid_categories)

    cv_input = cv_text[:5000]

    print(f"CV INPUT COMPLETO:")
    print(cv_input)
    print(f"CV INPUT LENGTH: {len(cv_input)}")

    prompt = f"""You are a technical skills extractor. Your job is to find EVERY technical skill mentioned in this CV.

CV text:
---
{cv_input}
---

Skills already detected: {known_skills_str}

VALID CATEGORIES: {categories_str}

INSTRUCTIONS:
1. Read the CV carefully and identify ALL technical skills, technologies, frameworks, languages, tools, platforms, databases, and methodologies mentioned.
2. Include skills from work experience, education, projects, certifications, and any technical section.
3. Do NOT filter for "confidence" — if it's mentioned in the CV as a technical skill, include it.
4. DO include skills that may already be in the "already detected" list — we will deduplicate later.
5. Use canonical names (e.g. "PostgreSQL" not "postgres", "JavaScript" not "js", "Node.js" not "nodejs").
6. Group them by category from the valid list above.

Return ONLY this JSON structure, nothing else:
{{
    "skills_by_category": {{
        "Backend": ["Python", "FastAPI", "Django"],
        "Database": ["PostgreSQL", "MongoDB"],
        "DevOps": ["Docker", "Kubernetes"]
    }}
}}

Rules:
- Use ONLY category names from the valid categories list
- Include ANY technical skill mentioned in the CV
- Return empty object {{"skills_by_category": {{}}}} ONLY if the CV truly has no technical content
- Be GENEROUS in detection, we prefer more skills than fewer

Respond with the JSON only. No explanations, no markdown."""

    try:
        response = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2500,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content.strip()
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        result = json.loads(content.strip())
        skills_by_cat = result.get('skills_by_category', {})

        flat = []
        for cat_skills in skills_by_cat.values():
            flat.extend(cat_skills)
        result['skills'] = sorted(set(flat))
        return result
    except Exception as e:
        print(f"ERROR detect_skills_from_cv: {e}")
        import traceback
        traceback.print_exc()
        return {"skills_by_category": {}, "skills": []}


# Banco de preguntas
def generate_questions_for_bank(payload: dict, language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    role = payload.get('role_name', '') or ('technical professional' if lang == 'en' else 'profesional técnico')
    seniority = payload.get('seniority', 'Mid')
    skill = payload.get('skill', '')
    category = payload.get('category', '')
    axis = payload.get('axis', 'Technical')
    competency = payload.get('competency', '')
    custom = payload.get('custom_question', '').strip()
    count = max(1, min(payload.get('count', 1), 5))

    if custom:
        prompt = f"""
You are an expert interviewer. Generate the evaluation guides for this manually-written question.

Role: {role}
Seniority: {seniority}
Skill: {skill}
Category: {category}
Axis: {axis}
Competency: {competency}

The question (already written by the user):
"{custom}"

Return EXACTLY this JSON, nothing else, in {lang_name}:
{{
    "questions": [
        {{
            "question": "{custom}",
            "expected_answer": "...",
            "skill": "{skill}",
            "category": "{category}",
            "axis": "{axis}",
            "competency": "{competency or 'General'}",
            "excellent_guide": "concrete things a strong answer should mention",
            "average_guide": "what an OK answer looks like",
            "weak_guide": "what a poor answer looks like",
            "suggested_red_flags": ["specific red flag 1", "specific red flag 2"]
        }}
    ]
}}

ALL TEXT MUST BE IN {lang_name.upper()}.
"""
    else:
        prompt = f"""
You are an expert interviewer. Generate {count} NEW interview question(s) in {lang_name}.

Role: {role}
Seniority: {seniority}
Skill: {skill}
Category: {category}
Axis: {axis}

Requirements per question:
- Detailed and contextual (2+ sentences with scenario when possible)
- Match the seniority level
- Specific, concrete evaluation guides (not generic phrases)
- Red flags tied to THIS specific topic
- ORAL question: the candidate must answer VERBALLY in 1-3 minutes. NEVER use verbs like "develop", "implement", "code", "write", "build". Use "explain", "describe", "walk me through" instead.

Return EXACTLY this JSON, nothing else, in {lang_name}:
{{
    "questions": [
        {{
            "question": "...",
            "expected_answer": "...",
            "skill": "{skill}",
            "category": "{category}",
            "axis": "{axis}",
            "competency": "specific competency name",
            "excellent_guide": "...",
            "average_guide": "...",
            "weak_guide": "...",
            "suggested_red_flags": ["...", "..."]
        }}
    ]
}}

Generate EXACTLY {count} question(s). ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with the JSON.
"""

    response = _safe_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=3000,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    return json.loads(content.strip())


# Metadata del cv
def extract_cv_metadata(cv_text: str) -> dict:
    """Independent of language: extracts personal data only."""
    if not cv_text or len(cv_text.strip()) < 30:
        return {"name": "", "email": "", "phone": "", "location": ""}

    first_part = cv_text[:1500]

    prompt = f"""Extract the candidate's personal information from this CV.

CV (first 1500 characters):
---
{first_part}
---

The candidate's full name is usually at the TOP of the CV, often as the largest text. It is a person's name (first name + last name), NOT a company name, NOT a job title, NOT "Curriculum Vitae".

Return EXACTLY this JSON, nothing else:
{{
    "name": "FullName LastName",
    "email": "email@example.com or empty string",
    "phone": "phone number or empty string",
    "location": "City, Country or empty string"
}}

Strict rules:
- "name" MUST be the candidate's full personal name, found at the top of the CV
- If the name is unclear or absent, return empty string for name
- Never invent data. Never use "John Doe" or placeholders
- Capitalize the name correctly

Respond ONLY with valid JSON. No markdown, no explanations."""

    try:
        response = _get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=3000,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content.strip()
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        result = json.loads(content.strip())
        name = result.get('name', '').strip()
        if name.lower() in ['', 'unknown', 'n/a', 'john doe', 'curriculum vitae']:
            result['name'] = ''
        return result
    except Exception as e:
        print(f"Error extracting CV metadata: {e}")
        return {"name": "", "email": "", "phone": "", "location": ""}


def analyze_cv_role_fit(cv_text: str, role_name: str, declared_seniority: str = "", role_description: str = "", language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    if not cv_text or not role_name:
        return {
            "fit_score": 0,
            "summary": "Missing information for analysis." if lang == 'en' else "Falta información para el análisis.",
            "strengths": [],
            "gaps": [],
            "highlights_from_cv": [],
            "recommendation": "",
        }

    cv_input = cv_text[:4000]
    desc_block = ""
    if role_description.strip():
        desc_block = f"""

DETAILED ROLE DESCRIPTION (provided by interviewer):
{role_description.strip()[:2000]}"""

    not_specified = "not specified" if lang == 'en' else "no especificado"

    prompt = f"""You are a senior HR consultant analyzing how well a candidate's CV fits a specific role.

ROLE THE CANDIDATE IS APPLYING FOR:
{role_name}
Declared seniority: {declared_seniority or not_specified}{desc_block}

CANDIDATE'S CV:
---
{cv_input}
---

Analyze deeply how well this CV matches the role. Be objective, specific and concrete.
{"Pay special attention to how well the CV matches the DETAILED ROLE DESCRIPTION above." if role_description.strip() else ""}

=== STRICT SCORING RUBRIC (use these EXACT bands) ===
Calculate fit_score by averaging these four dimensions equally (each worth 25 points max):

1. CORE SKILLS MATCH (0-25): Does the CV explicitly mention the technical skills the role requires?
   - 25: Every required core skill clearly present with depth
   - 18-24: Most core skills present, 1-2 minor gaps
   - 10-17: About half the core skills present
   - 5-9: Few core skills present
   - 0-4: Almost no overlap

2. SENIORITY/EXPERIENCE MATCH (0-25): Does the years and depth of experience match the declared seniority?
   - 25: Years and experience clearly match or exceed seniority
   - 18-24: Slight gap but compensated by quality of experience
   - 10-17: Notable gap (e.g. junior years applying for senior)
   - 0-9: Major mismatch

3. RELEVANT PROJECTS/EXPERIENCE (0-25): Are there concrete projects or roles that align with the target role?
   - 25: Multiple highly relevant projects with measurable impact
   - 18-24: Several relevant projects
   - 10-17: Some tangentially relevant experience
   - 0-9: No clearly relevant experience

4. ROLE DESCRIPTION ALIGNMENT (0-25): How well does the CV match the specific role description provided?
   - 25: Direct alignment with most requirements mentioned in the description
   - 18-24: Aligns with main requirements
   - 10-17: Aligns with some requirements
   - 0-9: Little alignment
   - (If no role description was provided, give 18 by default — neutral)

CRITICAL: Compute the score as the EXACT SUM of these four components. Do NOT round or "feel" the score — calculate it.
The same CV evaluated twice MUST produce the same score. Be a calculator, not a feeling.

Return EXACTLY this JSON in {lang_name}, nothing else:
{{
    "fit_score": <integer 0-100, MUST EQUAL the sum of the 4 rubric components above>,
    "score_breakdown": {{
        "core_skills_match": <integer 0-25>,
        "seniority_match": <integer 0-25>,
        "relevant_projects": <integer 0-25>,
        "role_alignment": <integer 0-25>
    }},
    "summary": "<2-3 sentences synthesizing the fit, mentioning specific evidence from CV{' and how it aligns with the role description' if role_description.strip() else ''}>",
    "strengths": [
        "<specific strength from CV directly relevant to the role>",
        "<another concrete strength>",
        "<another>"
    ],
    "gaps": [
        "<specific gap or missing skill for this role>",
        "<another gap>"
    ],
    "highlights_from_cv": [
        "<specific project, experience or achievement from CV that stands out>",
        "<another highlight>"
    ],
    "recommendation": "<1-2 sentences: should the interviewer focus on something specific given the gaps and strengths?>"
}}

Be very specific. Cite concrete items from the CV. Don't be generic.
ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with the JSON."""

    try:
        response = _get_client().chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15,
            max_tokens=4000,
            response_format={"type": "json_object"},
            reasoning_effort="high",
        )
        content = response.choices[0].message.content.strip()
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        return json.loads(content.strip())
    except Exception as e:
        print(f"Error con GPT-OSS, fallback a Llama: {e}")
        try:
            response = _safe_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000,
            )
            content = response.choices[0].message.content.strip()
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            return json.loads(content.strip())
        except Exception:
            return {
                "fit_score": 0,
                "summary": "Could not generate the analysis." if lang == 'en' else "No se pudo generar el análisis.",
                "strengths": [],
                "gaps": [],
                "highlights_from_cv": [],
                "recommendation": "",
            }


def compare_candidates(payload: dict, language: str = "es") -> dict:
    lang = _norm_lang(language)
    lang_name = _lang_name(lang)

    role_name = payload.get('role_name', '').strip() or ('the indicated role' if lang == 'en' else 'el rol indicado')
    role_description = payload.get('role_description', '').strip()
    candidates = payload.get('candidates', [])
    anchors = payload.get('anchors', [])

    if len(candidates) < 1:
        raise ValueError("At least 1 new candidate is required for comparison" if lang == 'en' else "Se requiere al menos 1 candidato nuevo para comparar")

    if lang == 'en':
        no_name = 'No name'
        labels = {
            'cand': 'CANDIDATE', 'id': 'ID',
            'role_eval': 'Role originally evaluated',
            'orig_score': 'Original score (from their interview)',
            'exec_summary': 'Executive summary',
            'tech_eval': 'Technical evaluation',
            'behav_eval': 'Behavioral evaluation',
            'strengths': 'Strengths',
            'gaps': 'Gaps/improvement areas',
            'skills': 'Detected skills',
            'axis': 'Scores by axis (0-5)',
            'interview_evidence': 'INTERVIEW EVIDENCE (questions asked, candidate answers, scores, notes)',
            'no_evidence': '(no interview evidence available)',
            'question_label': 'Q',
            'answer_label': 'Answer',
            'note_label': 'Interviewer note',
            'score_label': 'Score',
            'skipped_label': 'SKIPPED',
        }
    else:
        no_name = 'Sin nombre'
        labels = {
            'cand': 'CANDIDATO', 'id': 'ID',
            'role_eval': 'Rol evaluado originalmente',
            'orig_score': 'Score original (de su entrevista)',
            'exec_summary': 'Resumen ejecutivo',
            'tech_eval': 'Evaluación técnica',
            'behav_eval': 'Evaluación conductual',
            'strengths': 'Fortalezas',
            'gaps': 'Gaps/áreas de mejora',
            'skills': 'Skills detectadas',
            'axis': 'Scores por eje (0-5)',
            'interview_evidence': 'EVIDENCIA DE LA ENTREVISTA (preguntas hechas, respuestas del candidato, scores, notas)',
            'no_evidence': '(no hay evidencia de entrevista disponible)',
            'question_label': 'P',
            'answer_label': 'Respuesta',
            'note_label': 'Nota del entrevistador',
            'score_label': 'Score',
            'skipped_label': 'OMITIDA',
        }

    candidates_block = ""
    for idx, c in enumerate(candidates, 1):
        evidence_lines = []
        interview_questions = c.get('interview_questions', [])
        for q in interview_questions[:25]:
            q_text = (q.get('question', '') or '')[:150]
            skill = q.get('skill', '')
            axis = q.get('axis', '')
            tag = f"[{axis}/{skill}]" if skill else f"[{axis}]"
            if q.get('skipped'):
                evidence_lines.append(f"  {tag} {labels['question_label']}: {q_text} → {labels['skipped_label']}")
                continue
            score = q.get('score')
            if score is None:
                continue
            line = f"  {tag} {labels['question_label']}: {q_text} → {labels['score_label']}: {score}/5"
            if q.get('answer_note'):
                line += f"\n    {labels['answer_label']}: {q['answer_note'][:200]}"
            if q.get('interviewer_note'):
                line += f"\n    {labels['note_label']}: {q['interviewer_note'][:200]}"
            evidence_lines.append(line)
        evidence_block = "\n".join(evidence_lines) if evidence_lines else f"  {labels['no_evidence']}"

        candidates_block += f"""

=== {labels['cand']} {idx}: {c.get('name', no_name)} ===
- {labels['id']}: {c.get('record_id', '')}
- {labels['role_eval']}: {c.get('role', 'N/A')}
- {labels['orig_score']}: {c.get('original_score', 0)}/5
- {labels['exec_summary']}: {c.get('summary', 'N/A')}
- {labels['tech_eval']}: {c.get('technical_eval', 'N/A')}
- {labels['behav_eval']}: {c.get('behavioral_eval', 'N/A')}
- {labels['strengths']}: {', '.join(c.get('strengths', []))}
- {labels['gaps']}: {', '.join(c.get('gaps', []))}
- {labels['skills']}: {', '.join(c.get('skills', [])[:15])}
- {labels['axis']}: {c.get('axis_scores', {})}

{labels['interview_evidence']}:
{evidence_block}
"""

    anchors_block = ""
    if anchors:
        if lang == 'en':
            anchors_block = "\n\n=== ANCHORS FROM PREVIOUS ROUNDS (DO NOT CHANGE WITHOUT JUSTIFICATION) ===\n"
            for a in anchors:
                anchors_block += f"""
- {a.get('name', no_name)} (ID: {a.get('record_id', '')}): previous_score = {a.get('comparison_score', 0)}
  axis_scores: {a.get('axis_scores', {})}
"""
        else:
            anchors_block = "\n\n=== ANCLAJES DE RONDAS ANTERIORES (NO CAMBIAR SIN JUSTIFICACIÓN) ===\n"
            for a in anchors:
                anchors_block += f"""
- {a.get('name', no_name)} (ID: {a.get('record_id', '')}): score_anterior = {a.get('comparison_score', 0)}
  axis_scores: {a.get('axis_scores', {})}
"""

    desc_block = ""
    if role_description:
        if lang == 'en':
            desc_block = f"\n\nDETAILED ROLE DESCRIPTION:\n{role_description[:2500]}"
        else:
            desc_block = f"\n\nDESCRIPCIÓN DETALLADA DEL PUESTO:\n{role_description[:2500]}"

    anchor_instructions = ""
    if anchors:
        anchor_instructions = """

CRITICAL INSTRUCTIONS ON ANCHORS:

1. Candidates in "ANCHORS" were ALREADY evaluated in previous rounds.
   Their scores are the system's mandatory reference.

2. By DEFAULT, KEEP their scores UNCHANGED. That is the expected behavior.

3. You can ONLY change an anchor's score if ALL these conditions are met:
   - NEW candidates reveal specific concrete information that directly affects
     the anchor's evaluation
   - The change is at most ±5 points (no more)
   - You have specific justification citing clear evidence

4. ABSOLUTELY FORBIDDEN:
   - Changing scores for "relative adjustment" or "recalibration"
   - Changing scores without specific justification with evidence
   - Changes greater than 5 points
   - Changing more than 30% of anchors in one round

5. For each anchor whose score you change, you MUST fill the
   "score_change_justification" field with the specific reason.
   If you do not change the score, return the same previous value and
   omit "score_change_justification" (leave it null).

6. For anchors that are NOT changed, return them with their original score
   WITHOUT modifying them.
"""

    prompt = f"""You are a SENIOR HR CONSULTANT with 20 years of experience comparing technical candidates for hiring decisions. You produce rigorous, evidence-based comparative analyses.

TARGET ROLE: {role_name}{desc_block}

CANDIDATES TO EVALUATE:{candidates_block}{anchors_block}{anchor_instructions}

YOUR TASK:

For EACH candidate (new ones + anchors if any), produce:
1. A score 0-100 representing how well they fit the TARGET ROLE
2. Axis scores 0-100 (technical, communication, cultural_fit, leadership, problem_solving)
3. Specific strengths for this role (cite evidence from their summary)
4. Specific weaknesses for this role
5. Detailed justification: why this score, citing concrete evidence

Then produce GLOBAL analysis:
- Executive summary (3-4 sentences synthesizing the comparison)
- Final recommendation (which candidate to hire and why, who is backup)
- Key differentiators between candidates (what makes each unique)
- Trade-offs (what you gain/lose choosing one over another)

EVALUATION RULES:
- Be objective and evidence-based. CITE SPECIFIC ANSWERS from the INTERVIEW EVIDENCE section.
- The "Original score" (0-5) from each candidate's individual interview is CONTEXT ONLY.
  It should inform your judgment but NOT be a starting point for the comparison_score.
- WEIGHT INTERVIEW EVIDENCE HEAVILY: when a candidate gave concrete answers, factual or technical knowledge they demonstrated, AND interviewer notes, these are the strongest signals. Use them.
- A candidate whose interview evidence shows shallow answers should score LOWER than one who shows depth, even if their original scores look similar.
- In strengths/weaknesses/justification, REFERENCE SPECIFIC interview answers when possible (e.g., "demonstrated solid grasp of X by mentioning Y in their answer to question about Z").
- Evaluate each candidate from ZERO based on how well they fit the TARGET ROLE.
- Two candidates with similar original scores (e.g. both 4/5) can have very different
  comparison_scores (e.g. 92 vs 65) because the comparison is ROLE-SPECIFIC.
- Use the full range 0-100, don't cluster candidates at similar values unless they
  truly are similar for THIS specific role.
- Score 90-100: outstanding fit, top-tier candidate
- Score 75-89: strong fit, very competitive
- Score 60-74: acceptable fit with notable gaps
- Score 40-59: weak fit, significant concerns
- Score 0-39: poor fit, do not recommend

CRITICAL: Differentiate clearly between candidates. If two candidates have similar
profiles BUT one has more specific evidence for the target role, the difference should
show in their scores (at least 5-10 points apart). Don't give identical or near-identical
scores unless candidates truly are equivalent.

Return EXACTLY this JSON in {lang_name.upper()}, nothing else:
{{
    "candidates": [
        {{
            "record_id": "<must match the input record_id>",
            "name": "<candidate name>",
            "comparison_score": <integer 0-100>,
            "previous_score": <integer or null, only if this was an anchor>,
            "score_change_justification": <string or null, ONLY if anchor score changed>,
            "axis_scores": {{
                "technical": <0-100>,
                "communication": <0-100>,
                "cultural_fit": <0-100>,
                "leadership": <0-100>,
                "problem_solving": <0-100>
            }},
            "strengths": ["specific strength 1", "specific strength 2", "..."],
            "weaknesses": ["specific weakness 1", "..."],
            "justification": "3-4 sentences explaining WHY this candidate got this score, citing concrete evidence from their profile"
        }}
    ],
    "executive_summary": "3-4 sentences synthesizing the overall comparison",
    "final_recommendation": "Clear recommendation: who to hire, who is backup, why",
    "key_differentiators": [
        "What makes Candidate A unique",
        "What makes Candidate B unique",
        "..."
    ],
    "tradeoffs": {{
        "Candidate A vs Candidate B": "What you gain/lose choosing one over the other",
        "Candidate B vs Candidate C": "..."
    }}
}}

ALL TEXT MUST BE IN {lang_name.upper()}. Respond ONLY with the JSON. Be specific, cite evidence, never be generic."""

    try:
        response = _get_client().chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=8000,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        result = json.loads(content.strip())
        return result
    except Exception as e:
        print(f"Error en compare_candidates: {e}")
        import traceback
        traceback.print_exc()
        try:
            response = _safe_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=8000,
            )
            content = response.choices[0].message.content.strip()
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            return json.loads(content.strip())
        except Exception as e2:
            raise Exception(f"Could not generate the comparison: {e2}" if lang == 'en' else f"No se pudo generar la comparación: {e2}")