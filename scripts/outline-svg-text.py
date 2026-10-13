from pathlib import Path
import argparse, copy, os, subprocess, tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
parser=argparse.ArgumentParser(description='Outline profile SVG text using Inkscape; preserve animations.')
parser.add_argument('--font-dir', type=Path, required=True, help='Directory containing Poppins and JetBrains Mono font files')
args=parser.parse_args()
if not args.font_dir.is_dir():
 parser.error('--font-dir must be an existing directory')
root=Path(__file__).resolve().parents[1]/'assets'
ns='http://www.w3.org/2000/svg'
ET.register_namespace('',ns)
workspace=tempfile.TemporaryDirectory(prefix='profile-fonts-')
tmp=Path(workspace.name)
config=tmp/'fonts.conf'
config.write_text('<fontconfig><include>/etc/fonts/fonts.conf</include><dir>'+escape(str(args.font_dir.resolve()))+'</dir><cachedir>'+str(tmp/'cache')+'</cachedir></fontconfig>')
env=dict(os.environ,FONTCONFIG_FILE=str(config),XDG_CACHE_HOME=str(tmp/'cache'),INKSCAPE_PROFILE_DIR=str(tmp/'inkscape'))
for family in ['Poppins', 'JetBrains Mono']:
 match=subprocess.check_output(['fc-match','--format=%{family}',family],env=env,text=True)
 if family not in match:
  raise RuntimeError(f'Missing font: {family}; found {match}')
for source in sorted((root/'sources').rglob('*.svg')):
 tree=ET.parse(source)
 nodes=list(tree.iter('{'+ns+'}text'))
 for i,node in enumerate(nodes): node.set('id',f'font-text-{i}')
 staged=tmp/'source.svg';out=tmp/'outlined.svg'
 tree.write(staged,encoding='unicode')
 p=subprocess.run(['inkscape',str(staged),'--export-text-to-path','--export-plain-svg',f'--export-filename={out}'],env=env,capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr)
 converted=ET.parse(out)
 by_id={node.get('id'):node for node in converted.iter() if node.get('id')}
 for parent in list(tree.iter()):
  for child in list(parent):
   if child.tag!='{'+ns+'}text': continue
   replacement=copy.deepcopy(by_id[child.get('id')])
   assert replacement.tag!='{'+ns+'}text',source
   replacement.set('aria-label',''.join(child.itertext()))
   index=list(parent).index(child)
   parent.remove(child);parent.insert(index,replacement)
 dest=root/source.relative_to(root/'sources')
 tree.write(dest,encoding='unicode')
 assert not list(tree.iter('{'+ns+'}text'))
 print(source.relative_to(root/'sources'),len(nodes),'text elements outlined')

workspace.cleanup()
