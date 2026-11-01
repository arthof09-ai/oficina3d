"""Etapa COR (T1): projecao das vistas canonicas sobre a malha, com bake de textura.

Modulo PURO (sem bpy): roda no .venv_app e nos testes de unidade. O script
``_blender_cor.py`` (mesmo pacote) alimenta este modulo com os dados da malha
e executa o bake dentro do Blender headless.

Convecao de vistas (identica a ``oficina3d.refino.previa``):
- GLB: Y para cima, frente em +Z. No Blender (Z para cima): frente em -Y,
  lado ESQUERDO do personagem em +X.
- Vista ``frente``: camera em -Y olhando +Y; ``esquerda``: camera em +X;
  ``costas``: +Y; ``direita``: -X. Angulos na tabela ANGULOS.
- Camera ortografica: ``ortho_scale`` = extensao VERTICAL coberta (unidades
  Blender); a extensao horizontal = ortho_scale * (largura / altura), a mesma
  regra usada pelas previas do refino.

Alinhamento por silhueta (v1): a arte 2D nao e um render da malha gerada,
entao o enquadramento ingenuo desalinharia as regioes. Para cada vista, a
caixa da silhueta da arte (mascara alfa ou fundo estimado) e mapeada por
afinidade (escala + translacao, sem rotacao) sobre a caixa da silhueta da
malha projetada na mesma vista. O IoU residual entre as duas mascaras e
medido e reportado: ele diz o quanto o alinhamento v1 conseguiu aproximar.

Regras anti-defeito (do ESTUDO_MELHORIAS, secao T1):
- peso por angulo de facing: texel pintado pela vista de maior facing;
  facing <= 0.05 nao pinta (evita o "esticamento" das vistas de raspao);
- teste de profundidade: so pinta a face se o raio da face ate a camera nao
  bater em outra parte da malha antes (oclusao calculada no Blender, via BVH);
- dilatacao: texels sem fonte (zonas cegas, costuras) sao preenchidos pela
  cor vizinha mais proxima, em passes de 1 px; o percentual preenchido por
  dilatacao e reportado, nunca escondido.
"""
from __future__ import annotations

import math

import numpy as np

ANGULOS = {
    "frente": 0, "frente-esquerda": 45, "esquerda": 90, "costas-esquerda": 135,
    "costas": 180, "costas-direita": 225, "direita": 270, "frente-direita": 315,
}

# Facing minimo para pintar: abaixo disso a vista ve a face "de raspao" e a
# cor sai esticada. 0.05 e conservador (quase perpendicular); o peso em si
# ja prioriza a vista mais frontal.
FACING_MIN = 0.05


# ----------------------------------------------------------------------------
# Cameras
# ----------------------------------------------------------------------------
def direcao_camera(vista: str) -> tuple[float, float, float]:
    """Vetor unitario do centro do modelo ate a camera (coords Blender, Z-up)."""
    if vista == "cima":
        return (0.0, 0.0, 1.0)
    if vista not in ANGULOS:
        raise ValueError(f"vista sem camera definida: {vista!r}")
    a = math.radians(ANGULOS[vista])
    # Mesmo arredondamento de oficina3d.refino.previa.direcao_camera.
    return tuple(round(c, 6) + 0.0 for c in (math.sin(a), -math.cos(a), 0.0))


def base_camera(vista: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(direita, cima, frente) da camera, em coords Blender.

    ``frente`` = direcao do olhar (da camera para o modelo). Para as vistas
    laterais, cima = +Z; para ``cima``, o alto da imagem = +Y (costas), como
    nas previas do refino.
    """
    d = np.array(direcao_camera(vista), dtype=np.float64)
    frente = -d
    if vista == "cima":
        direita = np.array([1.0, 0.0, 0.0])
        cima = np.array([0.0, 1.0, 0.0])
        return direita, cima, frente
    mundo_cima = np.array([0.0, 0.0, 1.0])
    direita = np.cross(frente, mundo_cima)
    direita = direita / (np.linalg.norm(direita) or 1.0)
    cima = np.cross(direita, frente)
    return direita, cima, frente


def enquadramento(dim: tuple[float, float, float], largura: int, altura: int,
                  margem: float = 1.1) -> float:
    """ortho_scale (extensao vertical) que cobre a malha com ``margem``.

    ``dim`` = (dx, dy, dz) Blender. Igual as previas: vertical cobre dz, e a
    horizontal cobre hypot(dx, dy) (pior caso entre as vistas giradas).
    """
    dx, dy, dz = dim
    escala_v = dz
    escala_h = math.hypot(dx, dy) * (altura / largura)
    return max(escala_v, escala_h) * margem


def projetar(pontos: np.ndarray, centro: np.ndarray, vista: str, ortho_scale: float,
             largura: int, altura: int) -> tuple[np.ndarray, np.ndarray]:
    """Projeta pontos Blender para pixels da vista. Retorna (px, py).

    px cresce para a direita da imagem; py cresce para baixo (origem no topo).
    """
    direita, cima, _ = base_camera(vista)
    rel = np.asarray(pontos, dtype=np.float64) - np.asarray(centro, dtype=np.float64)
    u = rel @ direita
    v = rel @ cima
    ext_h = ortho_scale * (largura / altura)
    px = (u / ext_h + 0.5) * largura
    py = (0.5 - v / ortho_scale) * altura
    return px, py


def peso_facing(normal: np.ndarray, vista: str) -> float:
    """cos entre a normal e a direcao da camera, cortado em [0, 1]."""
    d = np.array(direcao_camera(vista), dtype=np.float64)
    n = np.asarray(normal, dtype=np.float64)
    norma = np.linalg.norm(n)
    if norma == 0:
        return 0.0
    return float(max(0.0, min(1.0, float(n @ d) / norma)))


# ----------------------------------------------------------------------------
# Mascaras e alinhamento por silhueta
# ----------------------------------------------------------------------------
def bbox_mascara(mascara: np.ndarray) -> tuple[int, int, int, int] | None:
    """(x0, y0, x1, y1) exclusivo da mascara, ou None se vazia."""
    ys, xs = np.nonzero(mascara)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def alinhamento_silhueta(bbox_arte: tuple[int, int, int, int],
                         bbox_malha: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    """(ax, bx, ay, by): pixel da arte = ax * pixel_da_malha + bx (idem y).

    Mapeia a caixa da silhueta da arte sobre a caixa da silhueta da malha
    projetada, por afinidade sem rotacao. Caixas degeneradas levantam erro
    em vez de produzir um mapeamento silenciosamente errado.
    """
    ax0, ay0, ax1, ay1 = bbox_arte
    mx0, my0, mx1, my1 = bbox_malha
    if ax1 <= ax0 or ay1 <= ay0 or mx1 <= mx0 or my1 <= my0:
        raise ValueError(f"caixa degenerada: arte={bbox_arte} malha={bbox_malha}")
    ax = (ax1 - ax0) / (mx1 - mx0)
    bx = ax0 - ax * mx0
    ay = (ay1 - ay0) / (my1 - my0)
    by = ay0 - ay * my0
    return (ax, bx, ay, by)


def iou(a: np.ndarray, b: np.ndarray) -> float:
    """IoU entre duas mascaras booleanas do mesmo formato.

    Uniao vazia (duas mascaras sem nenhum pixel) retorna 0,0: nao ha acordo
    mensuravel, e 1,0 seria "acordo perfeito" sobre nada (D8 do Critico T1).
    """
    if a.shape != b.shape:
        raise ValueError(f"mascaras de formatos diferentes: {a.shape} x {b.shape}")
    uniao = bool(np.logical_or(a, b).sum())
    if uniao == 0:
        return 0.0
    return float(np.logical_and(a, b).sum() / np.logical_or(a, b).sum())


def rasterizar_mascara_2d(pontos2d: np.ndarray, faces: np.ndarray,
                          largura: int, altura: int) -> np.ndarray:
    """Mascara bool (altura, largura) coberta pelos triangulos 2D dados."""
    masc = np.zeros((altura, largura), dtype=bool)
    for tri in faces:
        p = pontos2d[tri]  # (3, 2)
        x0 = max(0, int(math.floor(p[:, 0].min())))
        x1 = min(largura, int(math.ceil(p[:, 0].max())) + 1)
        y0 = max(0, int(math.floor(p[:, 1].min())))
        y1 = min(altura, int(math.ceil(p[:, 1].max())) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
        px = xs.ravel().astype(np.float64) + 0.5
        py = ys.ravel().astype(np.float64) + 0.5
        res = _baricentricas(p, px, py)
        if res is not None:
            masc[y0:y1, x0:x1] |= res[0].reshape(ys.shape)
    return masc


def _baricentricas(p: np.ndarray, px: np.ndarray, py: np.ndarray):
    """Mascara de dentro-do-triangulo + pesos baricentricos, ou None se degenerado."""
    (x0, y0), (x1, y1), (x2, y2) = p
    den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(den) < 1e-12:
        return None
    w0 = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) / den
    w1 = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) / den
    w2 = 1.0 - w0 - w1
    dentro = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
    return dentro, w0, w1, w2


# ----------------------------------------------------------------------------
# Bake por projecao
# ----------------------------------------------------------------------------
def rasterizar_textura(verts: np.ndarray, faces: np.ndarray, normais: np.ndarray,
                       faces_uv: np.ndarray, vistas: list[dict], tamanho: int,
                       centro: np.ndarray, dim: tuple[float, float, float],
                       ortho_scale: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """Pinta a textura por projecao das vistas.

    ``vistas``: lista de dicts com ``vista`` (nome), ``imagem`` (HxWx3 float
    0..1, linha 0 = topo), ``mascara`` (HxW bool), ``visivel`` (F,) bool e
    ``peso_face`` (F,) float (facing por face, pre-calculado).
    Retorna (textura TxTx3, pintado TxT bool, melhor_peso TxT float, info).
    """
    tex = np.zeros((tamanho, tamanho, 3), dtype=np.float64)
    pintado = np.zeros((tamanho, tamanho), dtype=bool)
    melhor = np.zeros((tamanho, tamanho), dtype=np.float64)
    info = {"faces_pintadas_por_vista": {}, "texels_por_vista": {}}
    for v in vistas:
        nome = v["vista"]
        imagem = v["imagem"]
        mascara = v["mascara"]
        visivel = v["visivel"]
        peso_face = v["peso_face"]
        hi, wi = mascara.shape
        # Caixa da malha projetada nesta vista, em pixels da imagem.
        px_all, py_all = projetar(verts, centro, nome, ortho_scale, wi, hi)
        bbox_m = (int(math.floor(px_all.min())), int(math.floor(py_all.min())),
                  int(math.ceil(px_all.max())), int(math.ceil(py_all.max())))
        bbox_a = bbox_mascara(mascara)
        if bbox_a is None:
            info["faces_pintadas_por_vista"][nome] = 0
            info["texels_por_vista"][nome] = 0
            continue
        ax, bx, ay, by = alinhamento_silhueta(bbox_a, bbox_m)
        direita, cima, _ = base_camera(nome)
        dcam = np.array(direcao_camera(nome), dtype=np.float64)
        texels = 0
        faces_ok = 0
        for fi in range(len(faces)):
            if not visivel[fi] or peso_face[fi] <= FACING_MIN:
                continue
            tri = faces[fi]
            uv = faces_uv[fi]  # (3, 2)
            if abs((uv[1, 0] - uv[0, 0]) * (uv[2, 1] - uv[0, 1])
                   - (uv[2, 0] - uv[0, 0]) * (uv[1, 1] - uv[0, 1])) < 1e-12:
                continue
            ux = uv[:, 0] * tamanho
            uy = (1.0 - uv[:, 1]) * tamanho  # linha 0 = topo (v=1)
            x0 = max(0, int(math.floor(ux.min())))
            x1 = min(tamanho, int(math.ceil(ux.max())) + 1)
            y0 = max(0, int(math.floor(uy.min())))
            y1 = min(tamanho, int(math.ceil(uy.max())) + 1)
            if x1 <= x0 or y1 <= y0:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
            px = xs.ravel().astype(np.float64) + 0.5
            py = ys.ravel().astype(np.float64) + 0.5
            res = _baricentricas(np.stack([ux, uy], axis=1), px, py)
            if res is None:
                continue
            dentro, w0, w1, w2 = res
            if not dentro.any():
                continue
            faces_ok += 1
            idx = np.nonzero(dentro)[0]
            w = np.stack([w0[idx], w1[idx], w2[idx]], axis=1)
            p3d = w @ verts[tri]
            nrm = w @ normais[tri]
            nn = np.linalg.norm(nrm, axis=1, keepdims=True)
            nn[nn == 0] = 1.0
            facing = np.maximum(0.0, (nrm / nn) @ dcam)
            qx = p3d @ direita
            qy = p3d @ cima
            ext_h = ortho_scale * (wi / hi)
            spx = (qx / ext_h + 0.5) * wi
            spy = (0.5 - qy / ortho_scale) * hi
            ipx = np.clip((ax * spx + bx).astype(int), 0, wi - 1)
            ipy = np.clip((ay * spy + by).astype(int), 0, hi - 1)
            amostra_ok = mascara[ipy, ipx] & (facing > FACING_MIN)
            if not amostra_ok.any():
                continue
            sel = idx[amostra_ok]
            tx = xs.ravel()[sel]
            ty = ys.ravel()[sel]
            pes = facing[amostra_ok]
            cor = imagem[ipy[amostra_ok], ipx[amostra_ok]]
            ganha = pes > melhor[ty, tx]
            if ganha.any():
                g = np.nonzero(ganha)[0]
                melhor[ty[g], tx[g]] = pes[g]
                tex[ty[g], tx[g]] = cor[g]
                pintado[ty[g], tx[g]] = True
                texels += int(ganha.sum())
        info["faces_pintadas_por_vista"][nome] = faces_ok
        info["texels_por_vista"][nome] = texels
    return tex, pintado, melhor, info


def dilatar(textura: np.ndarray, pintado: np.ndarray, iteracoes: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Preenche texels sem fonte com a cor vizinha mais proxima, 1 px por passe.

    Retorna (textura, pintado_final, n_preenchidos). Ordem de vizinhos fixa
    (cima, baixo, esquerda, direita) para determinismo.
    """
    tex = textura.copy()
    pin = pintado.copy()
    preenchidos = 0
    for _ in range(int(iteracoes)):
        falta = ~pin
        if not falta.any():
            break
        novo = pin.copy()
        nova_cor = tex.copy()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            desloc = np.roll(pin, shift=(dy, dx), axis=(0, 1))
            cor_desloc = np.roll(tex, shift=(dy, dx), axis=(0, 1))
            # roll atravessa a borda: anula a faixa que "vazou" do outro lado.
            if dy == -1:
                desloc[-1, :] = False
            elif dy == 1:
                desloc[0, :] = False
            if dx == -1:
                desloc[:, -1] = False
            elif dx == 1:
                desloc[:, 0] = False
            alvo = falta & desloc & ~novo
            if alvo.any():
                nova_cor[alvo] = cor_desloc[alvo]
                novo[alvo] = True
        ganho = int((novo & ~pin).sum())
        if ganho == 0:
            break
        tex, pin = nova_cor, novo
        preenchidos += ganho
    return tex, pin, preenchidos


# ----------------------------------------------------------------------------
# Metricas de UV (T5)
# ----------------------------------------------------------------------------
def metricas_uv(faces_uv: np.ndarray, areas_3d: np.ndarray, tamanho: int) -> dict:
    """Distorcao, ocupacao, ilhas e margem minima entre ilhas (em px)."""
    faces_uv = np.asarray(faces_uv, dtype=np.float64)
    areas_3d = np.asarray(areas_3d, dtype=np.float64)
    auv = np.abs((faces_uv[:, 1, 0] - faces_uv[:, 0, 0]) * (faces_uv[:, 2, 1] - faces_uv[:, 0, 1])
                 - (faces_uv[:, 2, 0] - faces_uv[:, 0, 0]) * (faces_uv[:, 1, 1] - faces_uv[:, 0, 1])) * 0.5
    tot_uv = float(auv.sum()) or 1.0
    tot_3d = float(areas_3d.sum()) or 1.0
    razao = (auv / tot_uv) / (areas_3d / tot_3d)
    distorcao = float((areas_3d * np.abs(razao - 1.0)).sum() / tot_3d)
    # Ocupacao: fracao de texels dentro de algum triangulo UV.
    masc = rasterizar_mascara_2d(_uv_para_pixels(faces_uv, tamanho).reshape(-1, 2),
                                 _faces_index(len(faces_uv)),
                                 tamanho, tamanho)
    ocupacao = float(masc.mean())
    ilhas, ilha_por_face = _ilhas_uv(faces_uv)
    margem = _margem_ilhas(faces_uv, ilha_por_face, tamanho)
    return {"distorcao_media": round(distorcao, 5), "ocupacao": round(ocupacao, 5),
            "ilhas": int(ilhas), "margem_min_px": margem}


def _uv_para_pixels(faces_uv: np.ndarray, tamanho: int) -> np.ndarray:
    """Vertices UV (F,3,2) -> pixels (F,3,2), linha 0 = topo."""
    px = np.empty_like(faces_uv)
    px[..., 0] = faces_uv[..., 0] * tamanho
    px[..., 1] = (1.0 - faces_uv[..., 1]) * tamanho
    return px


def _faces_index(n: int) -> np.ndarray:
    return np.arange(n * 3).reshape(n, 3)


def _ilhas_uv(faces_uv: np.ndarray) -> tuple[int, np.ndarray]:
    """Ilhas por arestas compartilhadas com UV igual nas duas pontas.

    Sem informacao de vertices da malha aqui: duas faces sao vizinhas de ilha
    se compartilham uma aresta UV-UV (mesmo par de pontos UV, tolerancia 1e-6).
    Aproximacao conservadora para o Smart UV (ilhas nao se tocam): arestas
    UV coincidentes sao raras fora da mesma ilha, e o numero reportado e o
    de componentes por aresta UV. O script do Blender refina com arestas da
    malha quando disponivel (mesma funcao, ver _blender_cor).
    """
    n = len(faces_uv)
    pai = list(range(n))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    aresta_para_faces: dict = {}
    for fi in range(n):
        uv = faces_uv[fi]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            p, q = tuple(np.round(uv[a], 6)), tuple(np.round(uv[b], 6))
            chave = (p, q) if p <= q else (q, p)
            if chave in aresta_para_faces:
                outro = aresta_para_faces[chave]
                ra, rb = raiz(fi), raiz(outro)
                if ra != rb:
                    pai[ra] = rb
            else:
                aresta_para_faces[chave] = fi
    rotulos = {}
    ilha_por_face = np.zeros(n, dtype=int)
    for fi in range(n):
        r = raiz(fi)
        if r not in rotulos:
            rotulos[r] = len(rotulos)
        ilha_por_face[fi] = rotulos[r]
    return len(rotulos), ilha_por_face


def _margem_ilhas(faces_uv: np.ndarray, ilha_por_face: np.ndarray, tamanho: int) -> int | None:
    """Menor faixa de texels vazios entre duas ilhas diferentes, por linha/coluna.

    None quando ha 0 ou 1 ilha (margem indefinida). Limitacao v1: ilhas que
    so se aproximam na diagonal (sem compartilhar nenhuma linha ou coluna)
    nao sao medidas por esta varredura; o Smart UV com margem 0.003 as afasta
    em UV, e a dilatacao do bake cobre costuras, mas a margem diagonal exata
    fica fora desta metrica.
    """
    if len(set(ilha_por_face.tolist())) < 2:
        return None
    # Imagem de ids: rasteriza cada face com seu id+1 (0 = vazio).
    img = np.zeros((tamanho, tamanho), dtype=np.int32)
    pts = _uv_para_pixels(faces_uv, tamanho)
    for fi in range(len(faces_uv)):
        p = pts[fi]
        x0 = max(0, int(math.floor(p[:, 0].min())))
        x1 = min(tamanho, int(math.ceil(p[:, 0].max())) + 1)
        y0 = max(0, int(math.floor(p[:, 1].min())))
        y1 = min(tamanho, int(math.ceil(p[:, 1].max())) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
        res = _baricentricas(p, xs.ravel().astype(float) + 0.5, ys.ravel().astype(float) + 0.5)
        if res is None:
            continue
        dentro = res[0].reshape(ys.shape)
        # Atribuicao por indices explicitos: img[a:b, c:d][mask] = v perderia
        # a escrita (o segundo indice devolve copia, nao vista).
        yy, xx = np.nonzero(dentro)
        img[y0 + yy, x0 + xx] = int(ilha_por_face[fi]) + 1
    menor = None
    for linha in list(img) + list(img.T):
        ids = linha
        # Percorre runs: vazio entre dois ids diferentes conta como faixa.
        atual = 0
        vazios = 0
        ultimo = 0
        for v in ids:
            if v == 0:
                if ultimo != 0:
                    vazios += 1
                continue
            if ultimo != 0 and v != ultimo and vazios > 0:
                menor = vazios if menor is None else min(menor, vazios)
            ultimo = v
            vazios = 0
    return menor
