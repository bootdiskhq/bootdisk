import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
from unittest.mock import patch
import unittest

spec = importlib.util.spec_from_file_location('intake', Path(__file__).parents[1]/'tools/intake.py')
i = importlib.util.module_from_spec(spec);spec.loader.exec_module(i)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'run';self.plan={'source':'original'}

    def test_resume_keeps_completed_bytes_and_retries_only_interrupted_step(self):
        calls=[]
        def first(p):
            calls.append('first');(p/'data').write_text('preserved')
        def interrupted(p):
            calls.append('broken');(p/'partial').write_text('incomplete');raise KeyboardInterrupt
        with i.Run(self.root,self.plan) as run:
            run.stage('first',first)
            with self.assertRaises(KeyboardInterrupt):run.stage('second',interrupted)
        original=i.tree(self.root/'first')
        with i.Run(self.root,self.plan) as run:
            run.stage('first',first)
            def finish(p):
                self.assertFalse((p/'partial').exists());calls.append('finish');(p/'data').write_text('done')
            run.stage('second',finish)
        self.assertEqual(calls,['first','broken','finish']);self.assertEqual(i.tree(self.root/'first'),original)

    def test_crash_after_commit_before_next_stage_is_idempotent(self):
        with self.assertRaises(KeyboardInterrupt):
            with i.Run(self.root,self.plan,stop_after='first') as run:
                run.stage('first',lambda p:(p/'data').write_text('done'))
        with i.Run(self.root,self.plan) as run:
            run.stage('first',lambda p:self.fail('completed action repeated'))

    def test_changed_config_refused_without_overwriting(self):
        with i.Run(self.root,self.plan):pass
        before=i.tree(self.root)
        with self.assertRaises(i.IntakeError):
            with i.Run(self.root,{'source':'different'}):pass
        self.assertEqual(i.tree(self.root),before)

    def test_modified_completed_result_is_preserved_and_refused(self):
        with i.Run(self.root,self.plan) as run:run.stage('first',lambda p:(p/'data').write_text('done'))
        (self.root/'first/data').write_text('manual note')
        with i.Run(self.root,self.plan) as run:
            with self.assertRaises(i.IntakeError):run.stage('first',lambda p:self.fail('must not run'))
        self.assertEqual((self.root/'first/data').read_text(),'manual note')

    def test_unowned_review_workspace_is_never_touched(self):
        self.root.mkdir();(self.root/'review-state.json').write_text('human decisions')
        before=i.tree(self.root)
        with self.assertRaises(i.IntakeError):
            with i.Run(self.root,self.plan):pass
        self.assertEqual(i.tree(self.root),before)

    def test_concurrent_owner_and_symlink_are_refused(self):
        with i.Run(self.root,self.plan):
            with self.assertRaises(BlockingIOError):
                with i.Run(self.root,self.plan):pass
        other=Path(self.tmp.name)/'link';other.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(i.IntakeError):
            with i.Run(other,self.plan):pass

    def test_partial_symlink_is_not_deleted(self):
        outside=Path(self.tmp.name)/'outside';outside.mkdir();(outside/'keep').write_text('safe')
        with i.Run(self.root,self.plan) as run:
            (self.root/'.first.partial').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(i.IntakeError):run.stage('first',lambda p:None)
        self.assertEqual((outside/'keep').read_text(),'safe')


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

    def source(self,name,mid,route,order=0):
        p=self.root/name;p.mkdir();i.write(p/'index.json',{'schema':'bootdisk-web-collection-1','media':[{'id':mid}],
            'entries':[{'entry':route,'source_order':order}]})
        # Deliberately noncanonical formatting to prove preservation of old documents.
        (p/(route.lower()+'.json')).write_text('{"source_order": '+str(order)+', "human_decision": "preserve"}\n')
        return p

    def test_existing_decisions_are_byte_identical_and_new_order_is_appended(self):
        old=self.source('old','first','K1');new=self.source('new','second','second--K1')
        dest=self.root/'merged';i.merge_data([old,new],dest)
        self.assertEqual((old/'k1.json').read_bytes(),(dest/'k1.json').read_bytes())
        self.assertEqual(i.read(dest/'second--k1.json')['source_order'],1)
        self.assertEqual(len(i.read(dest/'index.json')['entries']),2)

    def test_duplicate_medium_and_casefold_route_are_refused(self):
        a=self.source('a','same','K1');b=self.source('b','same','K2')
        with self.assertRaises(i.IntakeError):i.merge_data([a,b],self.root/'dup')
        b=self.source('c','other','k1')
        with self.assertRaises(i.IntakeError):i.merge_data([a,b],self.root/'collision')

    def test_inconsistent_baseline_order_is_refused(self):
        a=self.source('old','first','K1',order=3)
        with self.assertRaises(i.IntakeError):i.merge_data([a],self.root/'out')

    def test_store_conflict_is_refused(self):
        a=self.root/'a';a.mkdir();(a/'object').write_text('original')
        b=self.root/'b';b.mkdir();(b/'object').write_text('changed')
        with self.assertRaises(i.IntakeError):i.union_store([a,b],self.root/'store')


class InputTests(unittest.TestCase):
    def test_untracked_tool_module_changes_are_pinned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            subprocess.run(['git','init','-q',str(root)],check=True)
            (root/'tool.py').write_text('original')
            subprocess.run(['git','-C',str(root),'add','tool.py'],check=True)
            subprocess.run(['git','-C',str(root),'-c','user.name=Test','-c','user.email=test@example.com','commit','-qm','fixture'],check=True)
            (root/'new_module.py').write_text('first')
            before=i.pin_repo(root)
            (root/'new_module.py').write_text('changed')
            self.assertNotEqual(before,i.pin_repo(root))
            self.assertEqual(before['head'],i.pin_repo(root)['head'])

    def test_blocked_member_does_not_stop_other_disc_or_allow_aggregate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'
            plan={'media':[{'id':'bad'},{'id':'good'}],'repositories':{'web':tmp,'ingest':tmp,'catalog':tmp,'publish':tmp}}
            def disc(pipeline, medium):
                if medium['id']=='bad':raise i.IntakeError('Unknown metadata')
                return root,{'id':'good','status':'ready_for_review','entries':1,'rtf_documents':0,'source_issues':[],'unreadable_rtf':[]}
            with patch.object(i,'load_plan',return_value=plan), patch.object(i.Pipeline,'disc',disc), patch.object(i.Pipeline,'aggregate') as aggregate:
                self.assertEqual(i.execute('config',root),2)
                aggregate.assert_not_called()
            result=i.read(root/'report.json')
            self.assertEqual([r['status'] for r in result['media']],['blocked','ready_for_review'])
            self.assertFalse(result['ready_for_review']);self.assertFalse(result['published'])

    def test_input_mutation_blocks_assembly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'
            plan={'media':[{'id':'good'}],'repositories':{'web':tmp,'ingest':tmp,'catalog':tmp,'publish':tmp}}
            with patch.object(i,'load_plan',side_effect=[plan,{'changed':True}]), patch.object(i.Pipeline,'disc',return_value=(root,{'id':'good','status':'ready_for_review','entries':1,'rtf_documents':0,'source_issues':[],'unreadable_rtf':[]})), patch.object(i.Pipeline,'aggregate') as aggregate:
                self.assertEqual(i.execute('config',root),2)
                aggregate.assert_not_called()
            self.assertIn('Inputs changed',i.read(root/'report.json')['media'][-1]['error'])


if __name__=='__main__':unittest.main()
