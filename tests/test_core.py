import tempfile,unittest
from pathlib import Path
from motion_center.core import connect,add_resource,transition,reserve_test,finish_test,usage
class MotionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.db=connect(Path(self.tmp.name))
  self.rid=add_resource(self.db,{'title':'Test','url':'https://example.com/motion','source_pool':'daily','category':'UI-01'})
 def tearDown(self):self.db.close();self.tmp.cleanup()
 def test_duplicate(self):
  with self.assertRaises(Exception):
   add_resource(self.db,{'title':'Dup','url':'https://example.com/motion','source_pool':'daily','category':'UI-01'})
 def test_transition(self):
  with self.assertRaises(ValueError):transition(self.db,self.rid,'REPRODUCED')
  transition(self.db,self.rid,'VERIFIED');transition(self.db,self.rid,'PREVIEWED')
 def test_budget(self):
  transition(self.db,self.rid,'VERIFIED');transition(self.db,self.rid,'PREVIEWED')
  aid=reserve_test(self.db,self.rid,budget={'max_tests':1,'daily_test_seconds':300})
  with self.assertRaises(ValueError):reserve_test(self.db,self.rid,budget={'max_tests':1,'daily_test_seconds':300})
  with self.assertRaises(ValueError):finish_test(self.db,aid,'REPRODUCED',20)
  finish_test(self.db,aid,'REPRODUCED',20,evidence_path='evidence/test.mp4')
  self.assertEqual(usage(self.db)['count'],1)
 def test_invalid_pool(self):
  with self.assertRaises(ValueError):
   add_resource(self.db,{'title':'x','url':'https://example.com/2','source_pool':'unknown','category':'UI'})
if __name__=='__main__':unittest.main()
