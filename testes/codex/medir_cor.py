"""Compara renders unlit nas mesmas cameras; ROIs fixas antes da medicao."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import binary_erosion
from skimage.color import rgb2lab,deltaE_ciede2000
from skimage.metrics import structural_similarity
from glb_evidencia import geometria_sha,ler_glb
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/t2'
ROIS={'rosto':(.40,.07,.62,.21),'peito':(.30,.26,.70,.43),'pernas':(.25,.64,.86,.94)}
a=Image.open(OUT/'flat_antes/frente.png').convert('RGBA')
b=Image.open(OUT/'flat_depois/frente.png').convert('RGBA')
ref=Image.open(OUT/'entrada_orc/frente.png').convert('RGBA')
bb=a.getchannel('A').getbbox();rb=ref.getchannel('A').getbbox()
aligned=Image.new('RGBA',a.size)
aligned.paste(ref.crop(rb).resize((bb[2]-bb[0],bb[3]-bb[1]),Image.Resampling.LANCZOS),bb[:2])
aligned.save(OUT/'referencia_alinhada.png')
arr=[np.array(x)/255 for x in [aligned,a,b]]
common=(arr[0][...,3]>.9)&(arr[1][...,3]>.9)&(arr[2][...,3]>.9)
common=binary_erosion(common,iterations=3)
report={'metodo':'Emission/Cycles CPU/Standard; referencia redimensionada por bbox sem otimizar IoU; ROIs anatomicas aproximadas fixas; SSIM medio do mapa no interior comum erodido 3 px; DeltaE2000 nos mesmos pixels. Nao mede identidade nem detalhe alinhado semanticamente.',
        'bbox_referencia':rb,'bbox_render':bb,'rois_normalizadas':ROIS,'regioes':{}}
for region,coords in ROIS.items():
    x0,y0,x1,y1=[round(bb[0]+coords[0]*(bb[2]-bb[0])),round(bb[1]+coords[1]*(bb[3]-bb[1])),round(bb[0]+coords[2]*(bb[2]-bb[0])),round(bb[1]+coords[3]*(bb[3]-bb[1]))]
    mask=common[y0:y1,x0:x1];rr=arr[0][y0:y1,x0:x1,:3]
    row={'bbox':[x0,y0,x1,y1],'pixels_comuns':int(mask.sum()),'referencia_mediana_rgb':np.rint(np.median(rr[mask],axis=0)*255).astype(int).tolist()}
    for label,idx in [('antes',1),('depois',2)]:
        render=arr[idx][y0:y1,x0:x1,:3]
        _,ssim_map=structural_similarity(rr,render,data_range=1.,channel_axis=2,full=True)
        de=deltaE_ciede2000(rgb2lab(rr),rgb2lab(render))
        row[label]={'ssim':float(ssim_map.mean(axis=2)[mask].mean()),'deltaE2000_media':float(de[mask].mean()),'deltaE2000_mediana':float(np.median(de[mask])),
                    'mediana_rgb':np.rint(np.median(render[mask],axis=0)*255).astype(int).tolist()}
    report['regioes'][region]=row
paths=[OUT/f'{phase}_A/cor/modelo_cor.glb' for phase in ['antes','depois']]
report['geometria_normal_uv_indices_sha256']={phase:geometria_sha(path) for phase,path in zip(['antes','depois'],paths)}
report['glb_bytes']={phase:path.stat().st_size for phase,path in zip(['antes','depois'],paths)}
report['alpha_identico']=bool(np.array_equal(arr[1][...,3],arr[2][...,3]))
(OUT/'metricas_cor.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
except OSError:font=ImageFont.load_default()
def panel(im,label):
    bg=Image.new('RGB',(640,850),(30,32,36));bg.paste(im,(0,50),im.getchannel('A'))
    ImageDraw.Draw(bg).text((18,12),label,fill='white',font=font);return bg
board=Image.new('RGB',(1920,850))
for i,(im,label) in enumerate([(aligned,'Referencia (bbox)'),(a,'Antes: sRGB gravado como linear'),(b,'Depois: conversao corrigida')]):board.paste(panel(im,label),(i*640,0))
board.save(OUT/'comparacao_frente.png')
# Zooms iguais das mesmas areas; sem retoque ou correcao das imagens.
zooms=Image.new('RGB',(960,1080),(30,32,36));draw=ImageDraw.Draw(zooms)
for row,region in enumerate(['rosto','peito','pernas']):
    box=report['regioes'][region]['bbox']
    for col,im in enumerate([aligned,a,b]):
        crop=im.crop(box);crop.thumbnail((310,300))
        xx=col*320+(320-crop.width)//2;yy=row*360+45
        zooms.paste(crop,(xx,yy),crop.getchannel('A'))
        draw.text((col*320+8,row*360+8),region+' / '+['ref','antes','depois'][col],fill='white',font=font)
zooms.save(OUT/'comparacao_regioes.png')
views=['frente','frente-esquerda','esquerda','costas-esquerda','costas','costas-direita','direita','frente-direita']
contact=Image.new('RGB',(8*240,2*340),(30,32,36));draw=ImageDraw.Draw(contact)
for row,phase in enumerate(['antes','depois']):
    for col,view in enumerate(views):
        im=Image.open(OUT/f'flat_{phase}/{view}.png').convert('RGBA');im.thumbnail((240,300))
        contact.paste(im,(col*240,row*340+35),im.getchannel('A'))
        draw.text((col*240+3,row*340+3),phase+' '+view,fill='white')
contact.save(OUT/'comparacao_8_angulos.png')
print(json.dumps(report,indent=2))
