import argparse,json,sqlite3
from .core import connect,add_resource,reserve_test,finish_test,usage,DEFAULTS
def main():
 p=argparse.ArgumentParser(description='Motion Center Phase 1')
 p.add_argument('--root',default='./motion-data')
 sub=p.add_subparsers(dest='command',required=True)
 a=sub.add_parser('add');a.add_argument('json_file')
 sub.add_parser('list');sub.add_parser('budget')
 r=sub.add_parser('reserve');r.add_argument('resource_id');r.add_argument('--kind',choices=['quick','deep'],default='quick')
 f=sub.add_parser('finish');f.add_argument('attempt_id');f.add_argument('--status',required=True,choices=['REPRODUCED','FAILED','TIMED_OUT','REVIEW_REQUIRED']);f.add_argument('--seconds',type=int,required=True);f.add_argument('--evidence');f.add_argument('--result')
 args=p.parse_args();db=connect(args.root)
 try:
  if args.command=='add':
   with open(args.json_file,encoding='utf-8') as file:print(add_resource(db,json.load(file)))
  elif args.command=='list':
   for row in db.execute('SELECT id,title,source_pool,category,status FROM resources ORDER BY created_at DESC'):print(*row,sep='\t')
  elif args.command=='budget':print(json.dumps({'limits':DEFAULTS,'today':usage(db)},indent=2))
  elif args.command=='reserve':print(reserve_test(db,args.resource_id,args.kind))
  elif args.command=='finish':
   finish_test(db,args.attempt_id,args.status,args.seconds,args.evidence,args.result);print('Recorded (not independently verified)')
 except (ValueError,sqlite3.Error) as exc:p.exit(2,f'ERROR: {exc}\n')
 finally:db.close()
if __name__=='__main__':main()
