"""Substituto do torchmcubes (CPU, via scikit-image) para o TripoSR neste PC.

O torchmcubes original não compila aqui: com o PyTorch CUDA, o CMake exige o
CUDA Toolkit, que ficou fora da instalação (disco C: pequeno). Esta versão segue
a mesma convenção de saída: vértices em ordem (x, y, z) = (dim2, dim1, dim0)
e faces como LongTensor.
"""
import numpy as np
import torch
from skimage import measure


def marching_cubes(vol: torch.Tensor, thresh: float):
    v = vol.detach().float().cpu().numpy()
    verts, faces, _, _ = measure.marching_cubes(v, level=thresh)
    verts = np.ascontiguousarray(verts[:, ::-1])
    # Inverter os eixos espelha a malha; trocar a ordem dos vértices da face mantém a orientação.
    faces = np.ascontiguousarray(faces[:, ::-1])
    return torch.from_numpy(verts.copy()).float(), torch.from_numpy(faces.astype(np.int64))
