import importlib.util
import io
import tarfile
import tempfile
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('intake',Path(__file__).parents[1]/'tools/intake.py')
i=importlib.util.module_from_spec(spec);spec.loader.exec_module(i)

@unittest.skipUnless(shutil.which('tar'),'tar required')
class SerialSourceTests(unittest.TestCase):
 def run_source(self,name='menu.html',kind=None,fail=False):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);archive=root/'disc.tar'
   with tarfile.open(archive,'w') as tar:
    info=tarfile.TarInfo(name);info.size=4
    if kind:info.type=kind;info.linkname='/tmp/outside';info.size=0
    tar.addfile(info,io.BytesIO(b'menu') if not kind else None)
   work=root/'work';work.mkdir()
   plan={'bsdtar':shutil.which('tar'),'repositories':{k:str(root) for k in ['web','ingest','catalog','publish']}}
   run=i.Run(work,plan);p=i.Pipeline(run);seen=[]
   def consume(m,source):
    self.assertEqual((source/'menu.html').read_bytes(),b'menu');seen.append(str(source))
    if fail:raise i.IntakeError('blocked source')
    return 'done'
   with patch.object(p,'disc_source',side_effect=consume):
    if kind or name.startswith('..') or name.startswith('/') or fail:
     with self.assertRaises(i.IntakeError):p.disc({'iso':str(archive),'archive_driver':'bsdtar'})
    else:self.assertEqual(p.disc({'iso':str(archive),'archive_driver':'bsdtar'}),'done')
   self.assertEqual(list(work.iterdir()),[])
   self.assertTrue(archive.exists())
   if kind or name.startswith('..') or name.startswith('/'):self.assertFalse(seen)
 def test_source_read_and_disposed_after_success(self):self.run_source()
 def test_source_disposed_after_pipeline_failure(self):self.run_source(fail=True)
 def test_parent_escape_rejected_before_extraction(self):self.run_source('../escape')
 def test_absolute_path_rejected_before_extraction(self):self.run_source('/escape')
 def test_symlink_rejected_before_extraction(self):self.run_source(kind=tarfile.SYMTYPE)
