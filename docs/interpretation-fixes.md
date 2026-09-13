# Correcciones de interpretación y construcción

Base revisada: `72f22179d2a10c2a1e5bdd49e88f65ea28481d56`.
Fecha: 12 de septiembre de 2026.

## Implementación

La skill ahora separa `observed`, `ruled_out`, `uncertain` y `preserve` antes de recuperar una intervención. Se incorporan un intérprete conservador ES/EN y el puente de doce lecciones condicionales, sin modificar el compilador, `construct.py`, `pixel_lab.py`, el buscador temático existente ni el renderer. No hay API de modelos, embeddings ni dependencias nuevas.

El intérprete conserva el texto, identifica negaciones simples, preguntas, citas, problemas históricos/resueltos, deseos y contradicciones. Las frases no soportadas quedan visibles; no se atribuye comprensión general del lenguaje ni inspección de imágenes. Una preferencia estética no se convierte en un defecto.

La selección considera sujeto, etapa, cámara y problema antes de ordenar coincidencias léxicas. Si falta una lección especializada, recupera el contenido del método base instalado. Un fallo de pose apunta a anatomía; una silueta mecánica, a construcción funcional; una arquitectónica, a volúmenes relacionados. Una incompatibilidad de etapa no se tapa con consejos sobre textura. Un fallo técnico de escala o movimiento no recurre a composición de paisajes como sustituto.

La validación del contexto rechaza campos desconocidos, claves duplicadas, tipos incorrectos, filtros contradictorios y entradas desmedidas. Los ejercicios se crean sin observaciones ni aprobaciones inventadas y no se sobrescriben sin `--force`.

## Correcciones del criterio artístico

El núcleo de `SKILL.md` y el [contrato de interpretación](../SKILLS/pixel-art-html/references/interpretation-contract.md) incorporan estas decisiones:

- Proteger una o dos relaciones que identifican al diseño, no todas sus coordenadas anteriores.
- Resolver gesto, apoyo, pertenencia de herramientas y relaciones entre superficies antes del detalle.
- Diferenciar contorno, contacto, costura, pliegue y transición de luz. Una frontera modifica los dos grupos vecinos.
- No eliminar automáticamente texturas, ojos, brillos útiles, antialiasing manual o asimetrías.
- Fijar cámara, fuentes de luz, materiales y alcance de paleta por asset y dominio visual.
- Separar el proceso didáctico reconstruido de una revisión realmente realizada entre etapas.
- Juzgar el resultado por sí solo y contra sus requisitos antes de compararlo con una versión más débil.
- Distinguir matriz lógica, backing canvas, escala CSS y píxeles físicos; no redibujar un sprite para ocultar un problema de presentación.

Se conservaron el estudio de tres direcciones cuando corresponde, las restricciones de reparación de fuentes construidas, las revisiones entre etapas y los niveles `draft`, `representative` y `production-candidate`.

## Metadatos de los ejemplos

Los seis JSON `before`/`after` del árbol, retrato y carguero tenían una instrucción heredada sobre interiores de linternas. Se sustituyó solamente `art_direction.light` por iluminación externa coherente con cada sujeto.

Los bytes de los seis originales recuperados coincidieron con sus hashes Git. Dimensiones, fondo, paletas y grillas permanecen idénticos después del cambio. [El registro de conservación](../SKILLS/pixel-art-html/evals/interpretation-metadata.json) permite comprobarlo. No se cambiaron imágenes de comparación, evaluaciones históricas ni niveles de evidencia.

## Pruebas realizadas y límites

Se ejecutaron **107 tests** de la nueva suite con resultado satisfactorio. Cubren interpretación, selección, filtros, catálogos, entradas inválidas, CLI, escritura exclusiva de ejercicios, aritmética, conservación de píxeles y cuatro pruebas de orquestación del runner.

Los métodos usados por los tests unitarios de selección son fixtures declarados. No se distribuyen como `techniques.json`. El runner del repositorio carga ambas suites y exige además validar las referencias contra el catálogo real instalado. Mantiene Pillow como requisito del perfil `full` y no permite omitir sus tests silenciosamente.

**No se ejecutó el `check:full` completo del repositorio en este entorno.** La clonación directa estuvo bloqueada por resolución de red; se trabajó con archivos seleccionados recuperados por el conector. Los tests de orquestación no sustituyen al CI completo. La rama se construye sobre el árbol Git existente para conservar todos los archivos no modificados.

Tampoco se afirma superioridad artística a partir de estos tests. Los [ocho briefs públicos](../SKILLS/pixel-art-html/evals/tutorial-transfer-evals.json) y el [protocolo de calibración y comparación](../SKILLS/pixel-art-html/evals/interpretation-evals.json) siguen sin resultados. Sus identificadores históricos `holdout-*` no significan que sean casos ocultos. Guardar los resultados de futuras ejecuciones en registros separados, identificando la versión exacta utilizada; no convertir este plan en evidencia retrospectiva.

## Ejecutar sobre el checkout

Desde la raíz del repositorio:

```powershell
python .\SKILLS\pixel-art-html\scripts\tutorial_bridge.py validate
python -m unittest discover -s .\SKILLS\pixel-art-html\scripts -p test_interpretation.py -v
pnpm run check:full
```

Consulta de control:

```powershell
python .\SKILLS\pixel-art-html\scripts\tutorial_bridge.py diagnose "no tiene ruido pero la pose es rígida" --subject character --stage block
```

La salida debe excluir `texture-noise` y recuperar `anatomy-before-costume`, no una limpieza de textura. Para registros duraderos usar `--context` con [la plantilla vacía](../SKILLS/pixel-art-html/assets/interpretation-input.json).

Las fuentes públicas y sus límites de acceso están documentados; no se incluyen artículos completos, imágenes de pago ni corpus privados. No se agregaron aprobaciones, puntuaciones de belleza ni nuevos renders promocionados como arte terminado.
