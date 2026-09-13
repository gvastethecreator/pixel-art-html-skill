#!/usr/bin/env python3
"""Conservative ES/EN observation routing, not image analysis or general NLP.

Keep the user's text. Distinguish absent defects, uncertainty and protected intent
before retrieving techniques. Unknown language is never turned into a diagnosis.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

STAGES = ('block', 'planes', 'material', 'edges', 'runtime')
PROJECTIONS = ('top-down-orthographic', 'top-down-oblique', 'side', 'isometric')
SUBJECTS = ('character', 'foliage', 'prop', 'architecture', 'machine', 'tile', 'scene', 'interface')
KINDS = ('construction', 'technical', 'style-preference', 'unspecified')
# Bounded defect vocabulary. Broad nouns ("light", "color", "silhouette") are not defects.
PATTERNS = {
    'texture-noise': r'\b(ruido|noisy|noise|speckles|flecks|pixel(?:es)? sueltos)\b',
    'banding': r'\b(banding|bandas paralelas|concentric bands|franjas concentricas)\b',
    'canopy-construction': r'\b(coliflor|cauliflower|topiary|bolas desconectadas|disconnected balls|foliage holes|agujeros entre hojas|hollow canopy)\b',
    'pose-rigidity': r'\b(rigid[ao]?s?|rigidez|stiff|stiffness|pose rigida|pose rigidity)\b',
    'anatomy-attachment': r'\b(anatomia incorrecta|bad anatomy|floating limbs|limbs attach|limbs? detached|extremidades desconectadas|articulaciones incorrectas|anatomy attachment)\b',
    'weapon-ownership': r'\b(weapon ownership|propiedad del arma|arma flotante|floating weapon|weapon grip|agarre incorrecto|ownership unclear|arma superpuesta)\b',
    'silhouette-read': r'\b(silueta confusa|silueta ilegible|confusing silhouette|unclear silhouette|silhouette read|silueta no se entiende)\b',
    'palette-separation': r'\b(paleta incorrecta|wrong palette|muddy colors|colores embarrados|sin separacion de valores|palette separation)\b',
    'lighting-planes': r'\b(pillow shading|luz incoherente|inconsistent light|sombras incoherentes|flat volume|volumen plano|lighting planes|sombra no describe|sombras no describen)\b',
    'mirror-light': r'\b(luz espejada incorrecta|mirrored highlights wrong|mirror light|espejado sin relight)\b',
    'projection-mismatch': r'\b(proyeccion incorrecta|wrong projection|perspectiva incorrecta|projection mismatch|no es cenital|not overhead|top down ambiguity)\b',
    'tile-seams': r'\b(costuras|tile seams?|seams|esquinas no encajan|corners do not fit|repeticion evidente)\b',
    'material-read': r'\b(agua parece pasto|water looks like grass|arena parece agua|same texture everywhere|misma textura|material indistinguishable|material read|metal parece plastico)\b',
    'background-read': r'\b(se pierde en el fondo|perdido en el fondo|lost in background|lost against background|background readability|fondo tapa|background read)\b',
    'directional-identity': r'\b(cambia de mano|changes hands|asymmetric equipment flips|directional identity|equipo cambia de lado)\b',
    'motion-contract': r'\b(jitter|shimmer|temblor|movimiento entrecortado|motion contract|subpixel motion)\b',
    'alpha-palette': r'\b(transparencia cambia colores|alpha palette|palette alpha|alpha blends?|transparency colors|mezcla alpha)\b',
    'depth-hierarchy': r'\b(profundidad confusa|depth hierarchy|flat landscape|paisaje plano|mismo detalle en todos los planos|distance detail)\b',
    'scale-mapping': r'\b(borroso|blurry|blur|fractional scale|escala fraccional|pixel ratio|dpr|scale mapping|470\s*[x×]\s*240)\b',
}
BASE_ROUTES = {
    'texture-noise': ('contour-and-clusters',), 'banding': ('contour-and-clusters',),
    'canopy-construction': ('foliage-bundles',), 'pose-rigidity': ('anatomy-before-costume',),
    'anatomy-attachment': ('anatomy-before-costume',), 'weapon-ownership': ('anatomy-before-costume',),
    'silhouette-read': ('contour-and-clusters',), 'palette-separation': ('palette-as-roles',),
    'lighting-planes': ('light-as-planes',), 'mirror-light': ('light-as-planes',),
    'projection-mismatch': ('projection-scaffold',), 'tile-seams': ('tiles-and-transitions',),
    'material-read': ('metal-glass', 'water-flow'), 'background-read': ('landscape-depth',),
    'directional-identity': ('anatomy-before-costume',), 'motion-contract': (),
    'alpha-palette': ('water-flow',), 'depth-hierarchy': ('landscape-depth',),
    'scale-mapping': (),
}
# These annotate the EXISTING technique IDs; they do not invent a second method library.
BASE_CONTEXT = {
    'contour-and-clusters': (('block','edges','material'), SUBJECTS),
    'foliage-bundles': (('block','planes','material','edges'), ('foliage','scene','tile')),
    'anatomy-before-costume': (('block','planes','edges'), ('character',)),
    'palette-as-roles': (('planes','material'), SUBJECTS),
    'light-as-planes': (('planes','material','edges'), SUBJECTS),
    'projection-scaffold': (('block',), SUBJECTS),
    'tiles-and-transitions': (('block','material','edges','runtime'), ('tile','scene','architecture')),
    'metal-glass': (('planes','material','edges'), ('prop','machine','character','architecture','interface')),
    'water-flow': (('planes','material','runtime'), ('tile','scene','prop')),
    'landscape-depth': (('block','planes','material','runtime'), SUBJECTS),
    'tiny-information-budget': (('block','runtime'), SUBJECTS),
    'functional-machines': (('block','planes'), ('machine',)),
    'constructive-architecture': (('block','planes'), ('architecture',)),
    'icon-affordance': (('block','planes','runtime'), ('prop','interface')),
}
SUBJECT_WORDS = {
    'character': r'\b(personaje|character|centinela|soldier|portrait|retrato|criatura|creature)\b',
    'foliage': r'\b(arbol|tree|foliage|follaje|copa|canopy|conifera|conifer)\b',
    'prop': r'\b(prop|objeto|item|frasco|flask|icono|icon)\b',
    'architecture': r'\b(edificio|building|santuario|shrine|castillo|castle|techo|roof)\b',
    'machine': r'\b(machine|maquina|mech|carguero|carrier|vehiculo|vehicle)\b',
    'tile': r'\b(tiles?|tileset|baldosa|terreno|terrain)\b',
    'scene': r'\b(scene|escena|paisaje|landscape)\b',
    'interface': r'\b(interface|interfaz|ui|hud)\b',
}


def normalize(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError('Observation text must be a string')
    return ''.join(c for c in unicodedata.normalize('NFKD', text.casefold())
                   if not unicodedata.combining(c)).replace('-', ' ')


def issues_in(text: str) -> set[str]:
    text = normalize(text)
    found = {key for key, pattern in PATTERNS.items() if re.search(pattern, text)}
    for key in PATTERNS:
        if re.search(r'\b' + re.escape(key.replace('-', ' ')) + r'\b', text):
            found.add(key)
    if re.search(r'\b(arma|weapon|lanza|spear)\b', text) and re.search(
            r'\b(pertenece|ownership|no se entiende|unclear|confus[ao])\b', text):
        found.add('weapon-ownership')
    return found


def classify_clause(raw: str) -> tuple[str, str]:
    """Return bounded polarity and the reason; unknown constructions stay uncertain."""
    t = normalize(raw)
    if re.search(r'\b(tutorial (dice|explica|muestra)|tutorial says|example says|segun el tutorial)\b', t):
        return 'uncertain', 'reported-source-not-current-observation'
    if re.search(r'\b(quiero|queremos|busco|me gusta|no me molesta|want to|would like|intentional noise)\b', t):
        return 'preserve', 'desired-style-not-defect'
    if re.search(r'\b(no solo|not only|no es que|it is not that)\b', t):
        return 'uncertain', 'unsupported-scope'
    if (re.search(r'[?¿]|[“”«»"]', raw) or re.search(r"'[^']+'", raw) or
        re.search(r'\b(quizas|quiza|tal vez|maybe|perhaps|podria|might|creo|no se si|not sure|dudo)\b|^\s*(si|if)\b', t)):
        return 'uncertain', 'question-quote-or-uncertainty'
    if re.search(r'\b(no (quiero|queremos|debes|debe|agregar|agregues|quitar|quites|eliminar|elimines|cambiar|cambies)|do not (add|remove|change)|don.t (add|remove|change)|preservar|conservar|mantener|preserve|keep)\b', t):
        return 'preserve', 'intent-not-defect'
    if re.search(r'\b(no (esta |se ha |se )?(corregid[oa]|resuelt[oa]|solucionad[oa]|corrigio|resolvio)|not (yet )?(fixed|resolved)|sin (corregir|resolver)|without (fixing|resolving)|no desaparec[ei]o)\b', t):
        return 'uncertain', 'negated-resolution-requires-observation'
    if re.search(r'\b(falta|necesita mas|needs more|too little|not intentional)\b', t):
        return 'uncertain', 'missing-or-intent-scope'
    if re.search(r'\b(ya no|no longer|corregid[oa]|solucionad[oa]|already fixed|resolved)\b', t):
        return 'ruled_out', 'resolved-or-no-longer'
    if re.search(r'\b(antes|previously|used to|anteriormente|historicamente)\b', t):
        return 'uncertain', 'historical-not-current'
    if len(re.findall(r'\b(no|not|never|nunca)\b', t)) > 1:
        return 'uncertain', 'multiple-negations'
    # "No ownership problem" is absence; "ownership cannot be read" is a defect.
    if re.search(r'\b(no (hay|tiene|presenta|existe) (un |ningun )?(problema|error)|no problem|without (a )?problem)\b', t):
        return 'ruled_out', 'explicit-absence'
    if re.search(r'\b(no se entiende|no encaja[n]?|no es cenital|not overhead|cannot read|can.t read|not readable|do not fit|does not fit|no describe[n]?|sin separacion de valores|espejado sin relight)\b', t):
        return 'observed', 'negative-capability-is-a-defect'
    if re.search(r'\b(no|not|sin|without|neither|nor|ni|never|nunca)\b|\b(?:doesn.t|isn.t|don.t)\b', t):
        if len(issues_in(raw)) > 1 and not re.search(r'\b(ni|nor|neither)\b', t):
            return 'uncertain', 'ambiguous-negation-scope'
        return 'ruled_out', 'simple-negation'
    return 'observed', 'affirmative-candidate'


def split_clauses(text: str) -> list[str]:
    clauses = re.split(r'[.;\n]+|\b(?:pero|but|ahora|now|y|and)\b', text, flags=re.I)
    result = []
    for clause in clauses:
        # A positive defect followed by a separate absence ("rigid pose without noise").
        # Do not split "tree is not cauliflower" or "silhouette is not readable".
        cut = None
        for match in re.finditer(r'\b(?:sin|without|no|not|never|nunca)\b', clause, re.I):
            if issues_in(clause[:match.start()]) and issues_in(clause[match.start():]):
                cut = match.start()
                break
        result.extend([clause[:cut], clause[cut:]] if cut is not None else [clause])
    return result


def _texts(value: Any, field: str, maximum: int = 32) -> list[str]:
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError(f'{field} must be a list of at most {maximum} strings')
    if any(not isinstance(v, str) or not v.strip() or len(v) > 2000 for v in value):
        raise ValueError(f'{field} needs nonempty strings of at most 2000 characters')
    return value.copy()


def interpret(query: str | None = None, context: dict | None = None, *,
              stage: str | None = None, projection: str | None = None,
              subject: str | None = None) -> dict:
    """Normalize observations without editing a source, receiving a review or accepting art."""
    if (query is None) == (context is None):
        raise ValueError('Provide exactly one query or context object')
    allowed = {'schema_version','subject','stage','projection','observed','ruled_out',
               'uncertain','preserve','problem_kind','original_text'}
    if context is not None:
        if not isinstance(context, dict) or set(context) - allowed:
            raise ValueError('Invalid context or unknown context fields')
        if type(context.get('schema_version', 1)) is not int or context.get('schema_version', 1) != 1:
            raise ValueError('Unsupported interpretation schema version')
        if 'observed' not in context:
            raise ValueError('Context must explicitly provide observed, even when empty')
        raw_text = context.get('original_text', '')
        if not isinstance(raw_text, str) or len(raw_text) > 16000:
            raise ValueError('original_text must be a string of at most 16000 characters')
        groups = {k: _texts(context.get(k, []), k, 2 if k == 'preserve' else 32)
                  for k in ('observed','ruled_out','uncertain','preserve')}
        filters = {}
        for key, cli in (('stage',stage), ('projection',projection), ('subject',subject)):
            given = context.get(key)
            if cli is not None and given is not None and cli != given:
                raise ValueError(f'Conflicting {key} in context and command line')
            filters[key] = cli if cli is not None else given
        kind = context.get('problem_kind', 'unspecified')
    else:
        if not isinstance(query, str) or not query.strip() or len(query) > 16000:
            raise ValueError('Query must be nonempty text of at most 16000 characters')
        raw_text, kind = query, 'unspecified'
        groups = {'observed':[query], 'ruled_out':[], 'uncertain':[], 'preserve':[]}
        filters = {'stage':stage, 'projection':projection, 'subject':subject}
    for key, values in (('stage',STAGES), ('projection',PROJECTIONS), ('subject',SUBJECTS)):
        if filters[key] is not None and filters[key] not in values:
            raise ValueError(f'Unknown {key}: {filters[key]}')
    if kind not in KINDS:
        raise ValueError(f'Unknown problem_kind: {kind}')

    statements, warnings = [], []
    for group in ('observed','ruled_out','uncertain','preserve'):
        for text in groups[group]:
            # Keep quotes intact: splitting a quote must not manufacture an assertion.
            quoted_or_question = bool(re.search(r'[?¿“”«»"]', text) or re.search(r"'[^']+'", text))
            clauses = [text] if group != 'observed' or quoted_or_question else split_clauses(text)
            for raw in clauses:
                raw = raw.strip(' ,:')
                if not raw:
                    continue
                polarity, reason = classify_clause(raw)
                found = issues_in(raw)
                if group != 'observed':
                    polarity, reason = group, 'explicit-field'
                if group == 'observed' and polarity == 'observed' and not found:
                    polarity, reason = 'uncertain', 'unrecognized-observation'
                statements.append({'text':raw, 'source_text':text, 'source_field':group,
                                   'polarity':polarity, 'issues':sorted(found), 'reason':reason})
                if polarity == 'uncertain':
                    warnings.append(f'{reason}: {raw}')
                elif group in ('ruled_out', 'uncertain') and not found:
                    warnings.append(f'unrecognized-{group}: {raw}')
    by_polarity = {key: set().union(*(set(s['issues']) for s in statements if s['polarity'] == key))
                   for key in ('observed','ruled_out','uncertain')}
    conflicts = by_polarity['observed'] & by_polarity['ruled_out']
    active = by_polarity['observed'] - conflicts
    if conflicts:
        warnings.append('Conflicting observations excluded: ' + ', '.join(sorted(conflicts)))
    if kind == 'style-preference':
        active.clear()
        warnings.append('Style preference requires a brief-based decision; no automatic defect route')
    inferred = False
    if filters['subject'] is None:
        positive_text = normalize(' '.join(s['text'] for s in statements
                                          if (s['polarity'] == 'observed' and set(s['issues']) & active)
                                          or s['reason'] == 'unrecognized-observation'))
        subjects = [s for s, p in SUBJECT_WORDS.items() if re.search(p, positive_text)]
        if len(subjects) == 1:
            filters['subject'], inferred = subjects[0], True
        elif len(subjects) > 1:
            active.clear()
            warnings.append('Multiple subjects: provide a separate structured observation for each asset')
    preserved = list(dict.fromkeys(s['text'] for s in statements if s['polarity'] == 'preserve'))
    return {'schema_version':1, 'original_text':raw_text, 'input_context':context,
            'filters':filters, 'subject_inferred':inferred, 'problem_kind':kind,
            'statements':statements, 'active_issues':sorted(active),
            'ruled_out_issues':sorted(by_polarity['ruled_out']),
            'uncertain_issues':sorted(by_polarity['uncertain']), 'conflicts':sorted(conflicts),
            'preserve':preserved, 'warnings':warnings,
            'status':'candidate-observations' if active else 'needs-observation',
            'authority':'Bounded ES/EN text routing only; no image inspection or artistic acceptance.'}
