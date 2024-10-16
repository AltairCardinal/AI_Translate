import pysrt
import ai_trans
import utility

f = '鼹鼠 El.Topo.1970.FS.REMASTERED.1080p.BluRay.X264-AMIABLE.eng.导评.srt'
f_out = '鼹鼠 El.Topo.1970.FS.REMASTERED.1080p.BluRay.X264-AMIABLE.chs.导评.srt'

_encoding = utility.detect_encoding(f)
subs = pysrt.open(f, encoding = _encoding)


for i, sub in enumerate(subs):
    chs = ai_trans.translate(sub.text)
    print(f'[{i}/{len(subs)}]{sub.text} -> {chs}')
    subs[i].text = chs

subs.save(f_out, encoding=_encoding)