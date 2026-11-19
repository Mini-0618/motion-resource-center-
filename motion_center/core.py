"""Local-first motion catalog. Does not execute untrusted source code."""
import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS resources(
 id TEXT PRIMARY KEY,title TEXT NOT NULL,url TEXT NOT NULL UNIQUE,
 source_pool TEXT NOT NULL CHECK(source_pool IN ('daily','evergreen')),
 category TEXT NOT NULL,styles TEXT NOT NULL DEFAULT '[]',
 description TEXT NOT NULL DEFAULT '',prompt TEXT NOT NULL DEFAULT '',
 preview_url TEXT,license TEXT,source_url TEXT,source_commit TEXT,
 status TEXT NOT NULL DEFAULT 'DISCOVERED',created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS attempts(
 id TEXT PRIMARY KEY,resource_id TEXT NOT NULL REFERENCES resources(id),
 kind TEXT NOT NULL CHECK(kind IN ('quick','deep')),
 status TEXT NOT NULL DEFAULT 'QUEUED',duration_seconds INTEGER NOT NULL DEFAULT 0,
 evidence_path TEXT,started_at TEXT,ended_at TEXT,result TEXT);
"""
ALLOWED={
 'DISCOVERED':{'VERIFIED','REJECTED'},
 'VERIFIED':{'PREVIEWED','REJECTED'},
 'PREVIEWED':{'QUEUED','REJECTED'},
 'QUEUED':{'RUNNING','REJECTED'},
 'RUNNING':{'REPRODUCED','FAILED','TIMED_OUT','REVIEW_REQUIRED'},
 'REPRODUCED':{'PACKAGED'},
 'FAILED':{'QUEUED'},'TIMED_OUT':{'QUEUED'},
 'REVIEW_REQUIRED':{'QUEUED','REJECTED'},
 'PACKAGED':set(),'REJECTED':set()}
DEFAULTS={'daily_discovery':48,'evergreen_discovery':24,'max_tests':10,
 'quick_seconds':300,'deep_seconds':1800,'daily_test_seconds':6000,
 'daily_new_bytes':30*1024**3,'minimum_free_bytes':100*1024**3}
def now(): return datetime.now(timezone.utc).isoformat()
def connect(root):
 root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
 for name in ('projects','previews','evidence','cache','exports','quarantine'):
  (root/name).mkdir(exist_ok=True)
 db=sqlite3.connect(root/'motion.db')
 db.execute('PRAGMA foreign_keys=ON');db.executescript(SCHEMA)
 return db
def add_resource(db,data):
 for key in ('title','url','source_pool','category'):
  if not data.get(key):raise ValueError('Missing '+key)
 if data['source_pool'] not in ('daily','evergreen'):raise ValueError('Invalid source_pool')
 rid=str(uuid.uuid4())
 with db:
  db.execute("""INSERT INTO resources
   (id,title,url,source_pool,category,styles,description,prompt,
    preview_url,license,source_url,source_commit,created_at)
   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
   (rid,data['title'],data['url'],data['source_pool'],data['category'],
    json.dumps(data.get('styles',[]),ensure_ascii=False),
    data.get('description',''),data.get('prompt',''),data.get('preview_url'),
    data.get('license'),data.get('source_url'),data.get('source_commit'),now()))
 return rid
def transition(db,rid,target):
 row=db.execute('SELECT status FROM resources WHERE id=?',(rid,)).fetchone()
 if not row:raise ValueError('Resource not found')
 if target not in ALLOWED[row[0]]:raise ValueError(f'Invalid transition: {row[0]} -> {target}')
 with db:db.execute('UPDATE resources SET status=? WHERE id=?',(target,rid))
def usage(db,day=None):
 day=day or now()[:10]
 count,seconds=db.execute("""SELECT COUNT(*),COALESCE(SUM(duration_seconds),0)
 FROM attempts WHERE substr(started_at,1,10)=? AND status!='CANCELLED'""",(day,)).fetchone()
 return {'count':count,'seconds':seconds}
def reserve_test(db,rid,kind='quick',budget=None):
 limits={**DEFAULTS,**(budget or {})}
 if kind not in ('quick','deep'):raise ValueError('Invalid kind')
 cap=limits['quick_seconds'] if kind=='quick' else limits['deep_seconds']
 with db:
  row=db.execute('SELECT status FROM resources WHERE id=?',(rid,)).fetchone()
  if not row or row[0] not in ('PREVIEWED','QUEUED','FAILED','TIMED_OUT','REVIEW_REQUIRED'):
   raise ValueError('Resource not ready')
  day=now()[:10]
  count=usage(db,day)['count']
  reserved=db.execute("""SELECT COALESCE(SUM(CASE WHEN kind='deep' THEN ? ELSE ? END),0)
   FROM attempts WHERE substr(started_at,1,10)=? AND status!='CANCELLED'""",
   (limits['deep_seconds'],limits['quick_seconds'],day)).fetchone()[0]
  if count>=limits['max_tests'] or reserved+cap>limits['daily_test_seconds']:
   raise ValueError('Daily budget exhausted')
  aid=str(uuid.uuid4())
  db.execute('INSERT INTO attempts(id,resource_id,kind,started_at) VALUES(?,?,?,?)',
   (aid,rid,kind,now()))
  db.execute("UPDATE resources SET status='QUEUED' WHERE id=?",(rid,))
 return aid
def finish_test(db,aid,status,seconds,evidence_path=None,result=None):
 if status not in ('REPRODUCED','FAILED','TIMED_OUT','REVIEW_REQUIRED'):
  raise ValueError('Invalid result')
 row=db.execute('SELECT resource_id,kind,status FROM attempts WHERE id=?',(aid,)).fetchone()
 if not row or row[2] not in ('QUEUED','RUNNING'):raise ValueError('Attempt not active')
 cap=DEFAULTS['quick_seconds'] if row[1]=='quick' else DEFAULTS['deep_seconds']
 if seconds<0 or seconds>cap:raise ValueError('Duration out of bounds')
 if status=='REPRODUCED' and not evidence_path:raise ValueError('Evidence path required')
 with db:
  db.execute("""UPDATE attempts SET status=?,duration_seconds=?,evidence_path=?,
   result=?,ended_at=? WHERE id=?""",(status,seconds,evidence_path,result,now(),aid))
  db.execute('UPDATE resources SET status=? WHERE id=?',(status,row[0]))
