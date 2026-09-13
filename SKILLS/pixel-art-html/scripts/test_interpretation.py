"""Regression tests for observation routing, catalog contracts and unchanged masters.

No artistic acceptance is inferred by this suite. Fixture methods test routing;
when available, the real bundled catalog is also checked by the integration gate.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import interpretation as ip
import tutorial_bridge as bridge
ROOT = HERE.parent
# Routing-only fixture, never shipped as the skill's techniques.json.
BASE = {'sources':[], 'techniques':[
    {'id':tid, 'title':tid, 'when':'Routing fixture only', 'chapters':[],
     'decisions':['Inspect the relationship'], 'pixel_actions':['Test the intervention'],
     'check':'Observe the result', 'failure':'No artistic claim', 'exercise':'Test routing'}
    for tid in sorted(set(ip.BASE_CONTEXT) | {'stone-facets'})
]}

class InterpretationTests(unittest.TestCase):
    def test_positive_noise(self):
        self.assertEqual(ip.interpret('tiene ruido')['active_issues'], ['texture-noise'])

    def test_negative_noise(self):
        r=ip.interpret('no tiene ruido')
        self.assertEqual(r['active_issues'], [])
        self.assertEqual(r['ruled_out_issues'], ['texture-noise'])

    def test_accented_canopy(self):
        r=ip.interpret('Árbol parece coliflor')
        self.assertEqual(r['active_issues'], ['canopy-construction'])
        self.assertEqual(r['filters']['subject'], 'foliage')

    def test_negative_canopy(self):
        self.assertEqual(ip.interpret('árbol no parece coliflor')['active_issues'], [])

    def test_contrast_scope(self):
        r=ip.interpret('no tiene ruido pero la pose es rígida')
        self.assertEqual(r['active_issues'], ['pose-rigidity'])
        self.assertEqual(r['ruled_out_issues'], ['texture-noise'])

    def test_conjunction_scope(self):
        r=ip.interpret('no tiene ruido y la pose es rígida')
        self.assertEqual(r['active_issues'], ['pose-rigidity'])

    def test_negative_capability(self):
        self.assertIn('weapon-ownership',ip.interpret('no se entiende a quién pertenece el arma')['active_issues'])

    def test_negative_readability(self):
        self.assertEqual(ip.interpret('la silueta no se entiende')['active_issues'],['silhouette-read'])

    def test_negated_ownership_problem(self):
        self.assertEqual(ip.interpret('no hay problema de propiedad del arma')['active_issues'],[])

    def test_question(self):
        self.assertEqual(ip.interpret('¿Tiene ruido?')['active_issues'],[])

    def test_uncertainty(self):
        self.assertEqual(ip.interpret('quizás tiene ruido')['active_issues'],[])

    def test_english_uncertainty(self):
        self.assertEqual(ip.interpret('maybe stiff')['active_issues'],[])

    def test_quote_does_not_become_current_observation(self):
        self.assertEqual(ip.interpret('El tutorial dice "tiene ruido y pose rígida"')['active_issues'],[])

    def test_history(self):
        self.assertEqual(ip.interpret('antes tenía ruido')['active_issues'],[])

    def test_historical_then_current(self):
        self.assertEqual(ip.interpret('antes tenía ruido; ahora la pose es rígida')['active_issues'],['pose-rigidity'])

    def test_resolved(self):
        self.assertEqual(ip.interpret('ruido corregido')['active_issues'],[])

    def test_no_longer(self):
        self.assertEqual(ip.interpret('ya no tiene ruido')['ruled_out_issues'],['texture-noise'])

    def test_preserved_intent(self):
        r=ip.interpret('no quiero quitar textura')
        self.assertEqual(r['active_issues'],[])
        self.assertEqual(r['preserve'],['no quiero quitar textura'])

    def test_double_negation_is_not_positive(self):
        self.assertEqual(ip.interpret('no es que no tenga ruido')['active_issues'],[])

    def test_not_only_is_ambiguous(self):
        self.assertEqual(ip.interpret('not only noise')['active_issues'],[])

    def test_english_simple_absence(self):
        self.assertEqual(ip.interpret('not noisy')['ruled_out_issues'],['texture-noise'])

    def test_english_contrast(self):
        self.assertEqual(ip.interpret('not noisy but stiff')['active_issues'],['pose-rigidity'])

    def test_unknown_language(self):
        self.assertEqual(ip.interpret('雑音はありません')['status'],'needs-observation')

    def test_broad_nouns_are_not_defects(self):
        self.assertEqual(ip.interpret('luz, color, silueta')['active_issues'],[])

    def test_asymmetry_is_not_a_defect(self):
        self.assertEqual(ip.interpret('asimetría del hombro')['active_issues'],[])

    def test_mirroring_alone_is_not_a_defect(self):
        self.assertEqual(ip.interpret('mirror geometry')['active_issues'],[])

    def test_no_subject_inference_from_exclusions(self):
        r=ip.interpret('el árbol no parece coliflor pero tiene ruido')
        self.assertIsNone(r['filters']['subject'])

    def test_multiple_subjects_require_scope(self):
        self.assertEqual(ip.interpret('el árbol y el personaje tienen ruido')['status'],'needs-observation')

    def test_original_text_is_lossless(self):
        text=' ÁRBOL: no parece coliflor; ¿ruido? '
        self.assertEqual(ip.interpret(text)['original_text'],text)

    def test_empty_observed_is_not_inferred(self):
        r=ip.interpret(context={'observed':[], 'ruled_out':['texture noise'], 'preserve':['pose-rigidity']})
        self.assertEqual(r['active_issues'],[])

    def test_structured_context(self):
        r=ip.interpret(context={'subject':'character','stage':'block','observed':['pose reads rigid', 'weapon ownership unclear'],
            'ruled_out':['texture noise','wrong palette'],'preserve':['asymmetric shoulder','left-facing stance']})
        self.assertEqual(r['active_issues'],['pose-rigidity','weapon-ownership'])
        self.assertEqual(r['preserve'],['asymmetric shoulder','left-facing stance'])

    def test_observed_field_does_not_override_negation(self):
        self.assertEqual(ip.interpret(context={'observed':['no tiene ruido']})['active_issues'],[])

    def test_conflicts_do_not_recommend(self):
        r=ip.interpret(context={'observed':['texture-noise','pose-rigidity'],'ruled_out':['texture-noise']})
        self.assertEqual(r['conflicts'],['texture-noise'])
        self.assertEqual(r['active_issues'],['pose-rigidity'])

    def test_explicit_uncertain_field(self):
        self.assertEqual(ip.interpret(context={'observed':[],'uncertain':['pose-rigidity']})['active_issues'],[])

    def test_style_preference_is_not_a_repair(self):
        r=ip.interpret(context={'observed':['pose-rigidity'],'problem_kind':'style-preference'})
        self.assertEqual(r['active_issues'],[])

    def test_context_fields_fail_closed(self):
        with self.assertRaises(ValueError): ip.interpret(context={'observed':[],'obseved':['noise']})

    def test_observed_is_required(self):
        with self.assertRaises(ValueError): ip.interpret(context={'ruled_out':['noise']})

    def test_version_boolean_is_not_integer(self):
        with self.assertRaises(ValueError): ip.interpret(context={'observed':[],'schema_version':True})

    def test_conflicting_filters(self):
        with self.assertRaises(ValueError): ip.interpret(context={'observed':[],'stage':'block'},stage='material')

    def test_unknown_subject(self):
        with self.assertRaises(ValueError): ip.interpret('noise',subject='dragon')

    def test_unknown_projection(self):
        with self.assertRaises(ValueError): ip.interpret('noise',projection='3d')

    def test_unknown_stage(self):
        with self.assertRaises(ValueError): ip.interpret('noise',stage='polish')

    def test_unknown_kind(self):
        with self.assertRaises(ValueError): ip.interpret(context={'observed':[],'problem_kind':'beautiful'})

    def test_no_input(self):
        with self.assertRaises(ValueError): ip.interpret()

    def test_dual_input(self):
        with self.assertRaises(ValueError): ip.interpret('noise',{'observed':[]})

    def test_empty_input(self):
        with self.assertRaises(ValueError): ip.interpret(' ')

    def test_large_input(self):
        with self.assertRaises(ValueError): ip.interpret('x'*16001)

    def test_nonlist_observations(self):
        with self.assertRaises(ValueError): ip.interpret(context={'observed':'noise'})

    def test_two_identity_relations(self):
        with self.assertRaises(ValueError): ip.interpret(context={'observed':[],'preserve':['a','b','c']})

    def test_positive_before_absence(self):
        r=ip.interpret('pose rígida sin ruido')
        self.assertEqual(r['active_issues'],['pose-rigidity'])
        self.assertEqual(r['ruled_out_issues'],['texture-noise'])

    def test_english_positive_before_absence(self):
        self.assertEqual(ip.interpret('stiff pose without noise')['active_issues'],['pose-rigidity'])

    def test_desired_noise_not_a_defect(self):
        self.assertEqual(ip.interpret('quiero ruido en la ropa')['active_issues'],[])

    def test_tutorial_report_not_an_observation(self):
        self.assertEqual(ip.interpret('el tutorial dice tiene ruido')['active_issues'],[])

    def test_unrecognized_exclusion_is_visible(self):
        r=ip.interpret(context={'observed':[],'ruled_out':['something unclassified']})
        self.assertTrue(r['warnings'])

    def test_two_excluded_defects(self):
        r=ip.interpret('no tiene ruido ni pose rígida')
        self.assertEqual(r['active_issues'],[])
        self.assertEqual(r['ruled_out_issues'],['pose-rigidity','texture-noise'])

    def test_ambiguous_scope_not_asserted(self):
        r=ip.interpret('no tiene ruido pose rígida')
        self.assertEqual(r['active_issues'],[])
        self.assertTrue(r['uncertain_issues'])

class RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.registry=bridge.load_catalog(ROOT)

    def call(self, text=None, **kwargs):
        return bridge.diagnose(text,self.catalog,self.registry,base=BASE,**kwargs)

    def test_positive_and_negative_differ(self):
        self.assertTrue(self.call('tiene ruido')['lessons'])
        self.assertFalse(self.call('no tiene ruido')['lessons'])

    def test_canopy_target(self):
        self.assertEqual(self.call('árbol parece coliflor')['lessons'][0]['id'],'canopy-overlap-repair')

    def test_pose_uses_real_base_id(self):
        r=self.call('la pose es rígida',subject='character',stage='block')
        self.assertFalse(r['lessons'])
        self.assertEqual(r['techniques'][0]['id'],'anatomy-before-costume')

    def test_exclusion_not_used_for_ranking(self):
        r=self.call('no tiene ruido pero la pose es rígida',subject='character',stage='block')
        self.assertFalse(r['lessons'])
        self.assertEqual(r['techniques'][0]['id'],'anatomy-before-costume')

    def test_character_silhouette_is_not_texture(self):
        r=self.call('silueta confusa',subject='character',stage='block')
        self.assertEqual(r['techniques'][0]['id'],'anatomy-before-costume')
        self.assertFalse(r['lessons'])

    def test_stage_mismatch_does_not_force_texture(self):
        r=self.call('pose rígida',subject='character',stage='material')
        self.assertFalse(r['lessons']); self.assertFalse(r['techniques'])
        self.assertEqual(r['stage_mismatches'][0]['id'],'anatomy-before-costume')

    def test_subject_filter(self):
        r=self.call('coliflor',subject='machine',stage='block')
        self.assertFalse(r['lessons']); self.assertFalse(r['techniques'])

    def test_generic_lighting_not_mirror(self):
        r=self.call('luz incoherente',stage='planes')
        self.assertFalse(r['lessons'])
        self.assertEqual(r['techniques'][0]['id'],'light-as-planes')

    def test_water_material(self):
        r=self.call('agua parece pasto',stage='material')
        self.assertEqual(r['lessons'][0]['id'],'material-direction-not-density')

    def test_metal_is_not_water(self):
        r=self.call('metal parece plastico',subject='prop',stage='material')
        self.assertFalse(r['lessons'])
        self.assertEqual(r['techniques'][0]['id'],'metal-glass')

    def test_exclusions_only(self):
        r=self.call(context={'observed':[], 'ruled_out':['texture-noise'], 'subject':'character'})
        self.assertEqual(r['status'],'needs-observation')

    def test_no_fabricated_fallback(self):
        r=bridge.diagnose('pose rígida',self.catalog,self.registry)
        self.assertFalse(r['techniques']); self.assertFalse(r['base_catalog_available'])

    def test_determinism(self):
        self.assertEqual(self.call('noise; banding'), self.call('noise; banding'))

    def test_context_not_mutated(self):
        c={'observed':['pose-rigidity'],'preserve':['left-facing stance']}; old=deepcopy(c)
        r=self.call(context=c); self.assertEqual(c,old); self.assertEqual(r['preserve'],old['preserve'])

    def test_bounded_results(self):
        r=self.call('noise; tile seams; depth hierarchy',limit=1)
        self.assertLessEqual(len(r['lessons'])+len(r['techniques']),1)

    def test_invalid_limit(self):
        with self.assertRaises(ValueError): self.call('noise',limit=0)

    def test_boolean_limit(self):
        with self.assertRaises(ValueError): self.call('noise',limit=True)

    def test_catalog_valid(self):
        result=bridge.validate_catalog(self.catalog,self.registry,BASE)
        self.assertEqual(result['lessons'],12)
        self.assertTrue(result['baseline_ids_checked'])

    def test_invalid_catalog_issue(self):
        d=deepcopy(self.catalog); d['lessons'][0]['issues']=['beauty']
        with self.assertRaises(ValueError): bridge.validate_catalog(d,self.registry)

    def test_invalid_catalog_subject(self):
        d=deepcopy(self.catalog); d['lessons'][0]['subjects']=['dragon']
        with self.assertRaises(ValueError): bridge.validate_catalog(d,self.registry)

    def test_invalid_baseline(self):
        with self.assertRaises(ValueError): bridge.validate_catalog(self.catalog,self.registry,{'techniques':[]})

    def test_duplicate_lesson(self):
        d=deepcopy(self.catalog); d['lessons'].append(deepcopy(d['lessons'][0]))
        with self.assertRaises(ValueError): bridge.validate_catalog(d,self.registry)

    def test_metadata_does_not_support_lesson(self):
        s=deepcopy(self.registry)
        for row in s['sources']:
            row['body_reviewed']=False; row['media_reviewed']=False; row['access']='metadata-only'
        with self.assertRaises(ValueError): bridge.validate_catalog(self.catalog,s)

    def test_exercise_never_accepts(self):
        r=bridge.exercise_plan(self.catalog['lessons'][0],self.registry)
        self.assertEqual(r['review']['result'],'not-reviewed')
        self.assertFalse(r['review']['browser_observed'])
        self.assertIsNone(r['hypothesis']['observed_symptom'])

    def test_scale_arithmetic(self):
        self.assertEqual(bridge.scale_contract(470,240,4)['rendered'],[1880,960])

    def test_scale_target(self):
        self.assertTrue(bridge.scale_contract(480,270,4,1920,1080)['exact'])

    def test_scale_rejects_bool(self):
        with self.assertRaises(ValueError): bridge.scale_contract(True,240,4)

    def test_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x.json'; p.write_text('{"observed":[],"observed":["noise"]}')
            with self.assertRaises(ValueError): bridge.load_json(p)

    def test_cli_bad_context(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x.json'; p.write_text('{"obseved":[]}')
            r=subprocess.run([sys.executable,str(HERE/'tutorial_bridge.py'),'diagnose','--context',str(p)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2); self.assertNotIn('Traceback',r.stderr)

    def test_cli_exclusive_exercise(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'exercise.json'
            args=[sys.executable,str(HERE/'tutorial_bridge.py'),'exercise','canopy-overlap-repair','--output',str(p)]
            a=subprocess.run(args,capture_output=True); b=subprocess.run(args,capture_output=True)
            self.assertEqual(a.returncode,0); self.assertEqual(b.returncode,2)

    def test_all_issues_have_real_method_routes(self):
        self.assertEqual(set(ip.PATTERNS),set(ip.BASE_ROUTES))
        self.assertTrue(all(t in ip.BASE_CONTEXT for ids in ip.BASE_ROUTES.values() for t in ids))

    def test_machine_silhouette_route(self):
        r=self.call('silueta confusa',subject='machine',stage='block')
        self.assertEqual(r['techniques'][0]['id'],'functional-machines')

    def test_architecture_silhouette_route(self):
        r=self.call('silueta confusa',subject='architecture',stage='block')
        self.assertEqual(r['techniques'][0]['id'],'constructive-architecture')

    def test_prop_silhouette_route(self):
        r=self.call('silueta confusa',subject='prop',stage='block')
        self.assertEqual(r['techniques'][0]['id'],'icon-affordance')

class MetadataTests(unittest.TestCase):
    def test_six_masters_have_unchanged_pixels(self):
        evidence=json.loads((ROOT/'evals/interpretation-metadata.json').read_text())
        for row in evidence:
            with self.subTest(file=row['file']):
                value=json.loads((ROOT/'examples/construction-repair'/row['file']).read_text())
                pixel={k:value[k] for k in ('width','height','background','palette','grid')}
                digest=hashlib.sha256(json.dumps(pixel,sort_keys=True,separators=(',',':')).encode()).hexdigest()
                self.assertEqual(digest,row['pixel_payload_sha256'])
                self.assertNotIn('lantern interiors',value['art_direction']['light'])
                self.assertEqual(value['evidence_tier'],'draft')

class AdditionalBoundaryTests(unittest.TestCase):
    def test_missing_value_separation_is_a_defect(self):
        self.assertEqual(ip.interpret('sin separación de valores')['active_issues'],['palette-separation'])

    def test_mirror_without_relight_is_a_defect(self):
        self.assertEqual(ip.interpret('espejado sin relight')['active_issues'],['mirror-light'])

    def test_negated_resolution_es(self):
        r=ip.interpret('el ruido no está corregido')
        self.assertEqual(r['active_issues'],[])
        self.assertEqual(r['ruled_out_issues'],[])
        self.assertEqual(r['uncertain_issues'],['texture-noise'])

    def test_negated_resolution_en(self):
        self.assertEqual(ip.interpret('noise is not fixed')['ruled_out_issues'],[])

    def test_unresolved_noise_is_not_absence(self):
        self.assertEqual(ip.interpret('ruido sin corregir')['ruled_out_issues'],[])

    def test_missing_noise_is_not_excess_noise(self):
        self.assertEqual(ip.interpret('falta ruido')['active_issues'],[])

    def test_motion_does_not_fall_back_to_landscape(self):
        self.assertEqual(ip.BASE_ROUTES['motion-contract'],())

    def test_scale_does_not_fall_back_to_redesign(self):
        self.assertEqual(ip.BASE_ROUTES['scale-mapping'],())

    def test_empty_template_never_diagnoses(self):
        r=ip.interpret(context=bridge.load_json(ROOT/'assets/interpretation-input.json'))
        self.assertEqual(r['active_issues'],[])

    def test_eval_results_remain_unexecuted(self):
        plan=bridge.load_json(ROOT/'evals/interpretation-evals.json')
        self.assertEqual(plan['pilot']['completed_outputs'],0)
        self.assertIsNone(plan['results'])
        self.assertEqual(plan['pilot']['planned_outputs'],48)

    def test_public_briefs_are_not_hidden_holdout(self):
        plan=bridge.load_json(ROOT/'evals/tutorial-transfer-evals.json')
        self.assertIn('not a claim of hidden',plan['visibility'])

    def test_all_catalog_routes_checked_against_base(self):
        catalog,registry=bridge.load_catalog(ROOT)
        incomplete=deepcopy(BASE)
        incomplete['techniques']=[t for t in incomplete['techniques'] if t['id']!='functional-machines']
        with self.assertRaises(ValueError): bridge.validate_catalog(catalog,registry,incomplete)


class RunnerIntegrationTests(unittest.TestCase):
    def runner(self):
        path=ROOT.parents[1]/'scripts/run-pixel-art-tests.py'
        spec=importlib.util.spec_from_file_location('interpretation_runner_smoke',path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def fake_suite(self):
        import types
        class Mechanics(unittest.TestCase):
            def test_pass(self):
                self.assertTrue(True)
            def test_image(self):
                self.assertTrue(True)
        Mechanics.test_image.requires_pillow=True
        module=types.ModuleType('runner_fixture')
        module.Mechanics=Mechanics
        return module

    def execute(self, profile, pillow, gate=0):
        import contextlib, io
        from types import SimpleNamespace
        from unittest.mock import patch
        runner=self.runner()
        output=io.StringIO()
        with patch.object(runner,'load_test_module',return_value=self.fake_suite()) as load, \
             patch.object(runner,'pillow_available',return_value=pillow), \
             patch.object(runner.subprocess,'run',return_value=SimpleNamespace(returncode=gate)) as check, \
             patch.object(sys,'argv',['runner','--profile',profile]), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result=runner.main()
        return result,load.call_count,check.call_args,output.getvalue()

    def test_both_suites_are_included(self):
        result,loads,check,output=self.execute('core',True)
        self.assertEqual(result,0)
        self.assertEqual(loads,2)
        self.assertIn('2 selected; 2 Pillow',output)
        self.assertEqual(check.args[0][-1],'validate')

    def test_full_keeps_pillow_required(self):
        result,_,check,output=self.execute('full',False)
        self.assertEqual(result,2)
        self.assertIsNone(check)
        self.assertIn('Pillow is not installed',output)

    def test_real_catalog_failure_blocks_runner(self):
        result,_,_,output=self.execute('core',False,gate=2)
        self.assertEqual(result,1)
        self.assertNotIn('profile passed',output)

    def test_full_selects_every_case(self):
        result,_,_,output=self.execute('full',True)
        self.assertEqual(result,0)
        self.assertIn('4 selected; 2 Pillow',output)


if __name__ == '__main__':
    unittest.main()
