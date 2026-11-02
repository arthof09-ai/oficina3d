"""Regua congelada da Entrega 2; mesmos pixels, inclusive falhas de silhueta."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_erosion
from skimage.color import rgb2lab,deltaE_ciede2000
from skimage.metrics import structural_similarity
BASE=Path(__file__).resolve().parents[3]
OLD=BASE/'evidencias/t2';OUT=BASE/'evidencias/frente_b'
ROI={'rosto':(279,143,369,227),'peito':(239,256,401,358),'pernas':(218,484,466,663)}
def medir(paths,out):
    ref=np.asarray(Image.open(OLD/'referencia_alinhada.png').convert('RGBA'))/255.
    baseline=np.asarray(Image.open(OLD/'flat_depois/frente.png').convert('RGBA'))/255.
    mask=binary_erosion((ref[...,3]>.9)&(baseline[...,3]>.9),iterations=3)
    report={'metodo':'Regua Entrega 2 FIXA: referencia bbox [117,101,523,699], ROI e mascara sem reotimizacao. Pixels fora da silhueta candidata nao sao excluidos.',
            'rois':ROI,'casos':{}}
    for label,path in paths.items():
        ar=np.asarray(Image.open(path).convert('RGBA'))/255.
        row={}
        for nome,(x0,y0,x1,y1) in ROI.items():
            r=ref[y0:y1,x0:x1,:3];c=ar[y0:y1,x0:x1,:3];m=mask[y0:y1,x0:x1]
            de=deltaE_ciede2000(rgb2lab(r),rgb2lab(c))
            _,ss=structural_similarity(r,c,channel_axis=2,data_range=1.,full=True)
            row[nome]={'deltaE2000_media':float(de[m].mean()),'ssim':float(ss.mean(axis=2)[m].mean()),
                'n':int(m.sum()),'fora_silhueta':int((m&(ar[y0:y1,x0:x1,3]<=.9)).sum())}
        report['casos'][label]=row
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
if __name__=='__main__':
    paths={p.parent.parent.name:p for p in OUT.glob('*/flat/frente.png')}
    paths={'baseline_171007':OLD/'flat_depois/frente.png',**paths}
    r=medir(paths,OUT/'metricas.json')
    print(json.dumps(r,indent=2))
    board=Image.new('RGB',(320*len(paths),460),(30,32,36))
    for i,(label,p) in enumerate(paths.items()):
        im=Image.open(p).convert('RGBA');im.thumbnail((320,400))
        board.paste(im,(i*320,40),im.getchannel('A'))
        ImageDraw.Draw(board).text((i*320+5,5),label,fill='white')
        ImageDraw.Draw(board).text((i*320+5,425),'Face DE %.5f'%r['casos'][label]['rosto']['deltaE2000_media'],fill='white')
    board.save(OUT/'comparacao.png')
