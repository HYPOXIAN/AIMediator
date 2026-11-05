"""Installable Linux CLI; argparse only, structured operational results."""
import argparse
import json
from pathlib import Path
import sys
from . import __version__
from .common import Failure, new_path, write
from .config import defaults, resolve

CODES = {1:'internal_error',2:'invalid_input',3:'service_unavailable',4:'identity_or_output_conflict',5:'partial_processing',130:'interrupted'}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Failure(2, 'Unrecognized arguments; see --help' if message.startswith('unrecognized arguments:') else message)


def parser():
    p = Parser(prog='aimediator', description='Evidence-linked bilingual SF6 collected-sample feedback analysis.')
    p.add_argument('--version',action='version',version='aimediator ' + __version__)
    sub = p.add_subparsers(dest='command',required=True,parser_class=Parser)
    def leaf(container, name, **kwargs):
        item = container.add_parser(name,**kwargs)
        item.add_argument('--json',action='store_true',help='Emit one structured result on stdout')
        item.add_argument('--quiet',action='store_true',help='Suppress routine progress')
        return item
    init = leaf(sub,'init')
    init.add_argument('--out',type=Path,required=True)
    doctor = leaf(sub,'doctor')
    doctor.add_argument('--config',type=Path)
    doctor.add_argument('--input',type=Path)
    doctor.add_argument('--out',type=Path)
    doctor.add_argument('--offline',action='store_true')
    doctor.add_argument('--env-file',type=Path)
    analyze = leaf(sub,'analyze')
    for name in ('input','out','resume','config','env-file'):
        analyze.add_argument('--'+name,type=Path)
    analyze.add_argument('--evidence-quality',choices=['off','shadow','enforce'])
    analyze.add_argument('--stop-after',choices=['relevance','quality','full'])
    analyze.add_argument('--embedding-provider',choices=['ollama','configured'])
    analyze.add_argument('--embedding-model')
    analyze.add_argument('--base-url')
    analyze.add_argument('--num-gpu',type=int)
    analyze.add_argument('--max-parallel-requests',type=int)
    status = leaf(sub,'status')
    status.add_argument('--run',type=Path,required=True)
    review = sub.add_parser('review')
    review_sub = review.add_subparsers(dest='review_command',required=True,parser_class=Parser)
    for command in ('export','import'):
        item = leaf(review_sub,command)
        item.add_argument('--run',type=Path,required=True)
        item.add_argument('--out',type=Path,required=True)
        if command=='import':
            item.add_argument('--decisions',type=Path,required=True)
    report = leaf(sub,'report')
    report.add_argument('--run',type=Path,required=True)
    report.add_argument('--review',type=Path)
    report.add_argument('--out',type=Path,required=True)
    evaluate = sub.add_parser('evaluate')
    evaluation_sub=evaluate.add_subparsers(dest='evaluate_command',required=True,parser_class=Parser)
    quality=leaf(evaluation_sub,'quality')
    quality.add_argument('--run',type=Path,required=True)
    quality.add_argument('--labels',type=Path,required=True)
    quality.add_argument('--out',type=Path,required=True)
    demo = leaf(sub,'demo')
    demo.add_argument('--out',type=Path,required=True)
    return p


def dispatch(args):
    command = args.command
    artifacts, counts, warnings, details = {}, {}, [], {}
    if command == 'init':
        out=new_path(args.out)
        out.parent.mkdir(parents=True,exist_ok=True)
        # Exclusive creation closes the preflight race for this standalone file.
        with out.open('x',encoding='utf-8') as f:
            f.write(json.dumps(defaults(),ensure_ascii=False,indent=2)+'\n')
        artifacts={'config':str(out)}
    elif command == 'doctor':
        from .operations import doctor
        details=doctor(resolve(args.config,env_file=args.env_file),args.input,args.out,args.offline,args.env_file)
        if details['input_comments'] is not None:
            counts={'input_comments':details['input_comments']}
    elif command == 'analyze':
        from .operations import analyze
        keys=('evidence_quality','stop_after','embedding_provider','embedding_model','base_url','num_gpu',
              'max_parallel_requests')
        overrides={k:getattr(args,k) for k in keys}
        if args.resume:
            if args.input or args.out or args.config or any(v is not None for v in overrides.values()):
                raise Failure(2,'--resume allows only output controls and credential-only --env-file')
            cfg=None
        else:
            if not args.input or not args.out:
                raise Failure(2,'New analysis requires explicit --input and --out')
            cfg=resolve(args.config,overrides,args.env_file)
        out,details,warnings=analyze(args.input,args.out,cfg,args.resume,args.env_file,quiet=args.quiet)
        artifacts={'run':str(out)}
        counts=details['counts']
    elif command=='status':
        from .operations import status
        details=status(args.run)
        counts=details['counts']
        artifacts={'run':str(args.run.resolve())}
    elif command=='review':
        from .review import export_review,import_review
        if args.review_command=='export':
            out,count=export_review(args.run,args.out)
            counts={'exported_proposals':count}
        else:
            out,counts=import_review(args.run,args.decisions,args.out)
        artifacts={'review':str(out)}
    elif command=='report':
        from .reporting import export_report
        out,counts=export_report(args.run,args.out,args.review)
        artifacts={'markdown':str(out/'report.md'),'json':str(out/'report.json')}
    elif command=='evaluate':
        from .evaluation import evaluate_quality
        out,counts=evaluate_quality(args.run,args.labels,args.out)
        artifacts={'evaluation':str(out/'evaluation.json')}
    elif command=='demo':
        from .demo import demo
        out=demo(args.out,args.quiet)
        artifacts={'demo':str(out),'example_report':str(out/'example-report/report.md'), 'review_template':str(out/'review-template/decisions.json')}
        counts={'quality_modes':3}
        warnings=['Synthetic fixture transports; semantic accuracy is not established']
    return artifacts,counts,warnings,details


def main(argv=None):
    argv=list(sys.argv[1:] if argv is None else argv)
    structured='--json' in argv
    command=' '.join(x for x in argv[:2] if x in ('init','doctor','analyze','status','review','export','import','report','evaluate','quality','demo')) or 'aimediator'
    result={'command':command,'status':'ok','artifacts':{},'counts':{},'warnings':[],'error_code':None,'error_message':None}
    code=0
    args=None
    try:
        args=parser().parse_args(argv)
        artifacts,counts,warnings,details=dispatch(args)
        result.update(artifacts=artifacts,counts=counts,warnings=warnings,details=details)
    except Failure as exc:
        code=exc.code
        message=exc.message
    except (FileExistsError,) as exc:
        code=4
        message='Output already exists'
    except ModuleNotFoundError as exc:
        code=3
        message='Required dependency unavailable: ' + str(exc.name)
    except (ValueError,TypeError,KeyError,UnicodeError,OSError) as exc:
        code=2
        message='Invalid or unavailable file/configuration ('+type(exc).__name__+')'
    except KeyboardInterrupt:
        code=130
        message='Interrupted'
    except Exception as exc:
        code=1
        message='Unexpected internal error ('+type(exc).__name__+')'
    if code:
        result.update(status='partial' if code==5 else 'error',error_code=CODES[code],error_message=message)
        if args and code in (1,5,130):
            path=getattr(args,'out',None) or getattr(args,'resume',None)
            if path and path.exists():
                result['artifacts']={'saved_output':str(path.resolve())}
    if structured:
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
    elif code:
        print('aimediator: '+result['error_message'],file=sys.stderr)
    elif not getattr(args,'quiet',False):
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return code
