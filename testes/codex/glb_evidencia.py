"""Leitura independente dos acessores GLB das provas (nao usa o codigo do app)."""
import hashlib
import json
from pathlib import Path
import struct
import numpy as np

def ler_glb(path):
    data=Path(path).read_bytes()
    magic,version,total=struct.unpack_from('<III',data)
    assert magic==0x46546c67 and version==2 and total==len(data)
    offset=12;doc=None;binary=None
    while offset<len(data):
        size,kind=struct.unpack_from('<II',data,offset);offset+=8
        chunk=data[offset:offset+size];offset+=size
        if kind==0x4e4f534a:doc=json.loads(chunk)
        if kind==0x004e4942:binary=chunk
    assert doc is not None and binary is not None
    def accessor(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']]
        dtype={5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']]
        n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
        d=np.dtype(dtype);start=v.get('byteOffset',0)+a.get('byteOffset',0)
        values=np.ndarray((a['count'],n),dtype=d,buffer=binary,offset=start,
                          strides=(v.get('byteStride',n*d.itemsize),d.itemsize)).copy()
        if a.get('normalized'):
            values=values.astype(float)/np.iinfo(d).max
        return values
    primitives=[]
    for mesh in doc['meshes']:
        for prim in mesh['primitives']:
            row={name:accessor(i) for name,i in prim['attributes'].items()}
            if 'indices' in prim:row['indices']=accessor(prim['indices'])
            primitives.append(row)
    return doc,primitives

def geometria_sha(path):
    _,prims=ler_glb(path);h=hashlib.sha256()
    for p in prims:
        for key in ['POSITION','NORMAL','TEXCOORD_0','indices']:
            if key in p:h.update(key.encode());h.update(p[key].tobytes())
    return h.hexdigest()
