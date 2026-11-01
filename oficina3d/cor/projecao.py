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

Alinhamento otimizado (COR-08/A1): o IoU v1 e apenas REPORTADO, nunca
otimizado. ``otimizar_alinhamento`` parte do alinhamento por caixas
robustas (percentis, sem outliers) e busca em grade deterministica
grossa -> fina (escala uniforme, depois afim com trava de aspecto) o
transform que MAXIMIZA o IoU entre as mascaras. O bake usa o transform
otimizado quando o pedido o pede (``_blender_cor``: ``alinhamento``);
sem override, usa o alinhamento v1 por caixas.
COR-08/A0 (fix anterior a busca, sem o qual ela nao transferiria para o
bake): a amostragem por texel subtrai o centro (``rel = p3d - centro``),
como ``projetar``; antes, o centro z = 0,5 do Orc deslocava a amostra
vertical em ~0,45 * altura da imagem. A partir da A0, a ancora da COR-05
(textura ebd744a9...) esta SUPERADA como baseline: o bake corrigido tem
de diferir dela, e a comparacao passa a ser contra a nova baseline
(fix + bbox), nao contra a ancora.

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


def bbox_robusta_mascara(mascara: np.ndarray, percentil: float = 0.5) -> tuple[int, int, int, int] | None:
    """(x0, y0, x1, y1) exclusivo a partir dos percentis dos pixels True.

    A caixa por extremos e refem de pontas finas: um machado fora de pose,
    uma mecha de pelo ou um pe deslocado esticam a caixa inteira, e o
    alinhamento v1 herda o erro. O percentil corta as caudas: com 0,5, cada
    lado descarta os 0,5% externos da distribuicao de pixels (nao 0,5% da
    largura), o que remove pontas de 1 px de largura sem tocar no corpo.
    percentil = 0 reproduz exatamente ``bbox_mascara``. Mascara vazia -> None.
    A caixa nunca sai degenerada: se o percentil colapsar um eixo (mascara
    de 1 px de largura, por exemplo), o lado colapsado ganha 1 px.
    """
    ys, xs = np.nonzero(mascara)
    if len(xs) == 0:
        return None
    if not 0.0 <= percentil < 50.0:
        raise ValueError(f"percentil fora de [0, 50): {percentil}")
    x0 = int(np.percentile(xs, percentil))
    x1 = int(np.percentile(xs, 100.0 - percentil)) + 1
    y0 = int(np.percentile(ys, percentil))
    y1 = int(np.percentile(ys, 100.0 - percentil)) + 1
    x1 = max(x1, x0 + 1)
    y1 = max(y1, y0 + 1)
    return (x0, y0, x1, y1)


def aplicar_alinhamento(mascara_malha: np.ndarray, ax: float, bx: float,
                        ay: float, by: float) -> np.ndarray:
    """Mascara da malha deformada pela afinidade para o espaco da arte.

    Pixel da arte (x, y) amostra a malha em ((x - bx) / ax, (y - by) / ay),
    com o MESMO mapeamento inverso do IoU v1 (``_blender_cor``): truncamento
    para int (nao floor), e fora da grade = False. O truncamento e um
    artefato de 1 px na borda, herdado de proposito: o IoU otimizado e o
    IoU v1 tem de ser comparaveis numero a numero, e mudar o mapeamento
    aqui mudaria o v1 junto. Escalas zero levantam erro (divisao).
    """
    if ax == 0 or ay == 0:
        raise ValueError(f"escala zero no alinhamento: ax={ax} ay={ay}")
    h, w = mascara_malha.shape
    xs, ys = np.meshgrid(np.arange(w), np.arange(h))
    mx = ((xs - bx) / ax).astype(int)
    my = ((ys - by) / ay).astype(int)
    dentro = (mx >= 0) & (mx < w) & (my >= 0) & (my < h)
    alinhada = np.zeros((h, w), dtype=bool)
    alinhada[dentro] = mascara_malha[my[dentro], mx[dentro]]
    return alinhada


def iou_alinhado(mascara_malha: np.ndarray, mascara_arte: np.ndarray,
                 ax: float, bx: float, ay: float, by: float) -> float:
    """IoU entre a mascara da malha deformada pela afinidade e a da arte."""
    return iou(aplicar_alinhamento(mascara_malha, ax, bx, ay, by), mascara_arte)


def deformar_mascara(mascara: np.ndarray, ax: float, bx: float,
                     ay: float, by: float) -> np.ndarray:
    """Alias legivel de ``aplicar_alinhamento`` (COR-08/A1).

    Deforma a mascara pela afinidade (ax, bx, ay, by) com o mesmo
    mapeamento inverso do IoU v1: o pixel (x, y) do destino amostra a
    origem em ((x - bx) / ax, (y - by) / ay), com truncamento para int.
    """
    return aplicar_alinhamento(mascara, ax, bx, ay, by)


def alinhamento_otimizado(mascara_malha: np.ndarray,
                          mascara_arte: np.ndarray):
    """(ax, bx, ay, by, iou_inicial, iou_final) ou None (COR-08/A1).

    Conveniencia sobre ``otimizar_alinhamento``: parte do alinhamento
    por caixas ROBUSTAS (percentis) e devolve direto o transform
    otimizado com os IoUs antes/depois. Mascara vazia (malha ou arte)
    -> None (o chamador cai para o bbox, nunca falha o bake por isso);
    formatos diferentes -> ValueError (entrada malformada e recusada).
    """
    if mascara_malha.shape != mascara_arte.shape:
        raise ValueError(f"mascaras de formatos diferentes: {mascara_malha.shape} x {mascara_arte.shape}")
    if not mascara_malha.any() or not mascara_arte.any():
        return None
    bbox_m = bbox_robusta_mascara(mascara_malha)
    bbox_a = bbox_robusta_mascara(mascara_arte)
    if bbox_m is None or bbox_a is None:
        return None
    inicial = alinhamento_silhueta(bbox_a, bbox_m)
    ax, bx, ay, by, info = otimizar_alinhamento(
        mascara_malha, mascara_arte, inicial)
    return (ax, bx, ay, by, info["iou_inicial"], info["iou_final"])


def otimizar_alinhamento(mascara_malha: np.ndarray, mascara_arte: np.ndarray,
                         alinhamento_inicial: tuple[float, float, float, float]
                         ) -> tuple[float, float, float, float, dict]:
    """Busca deterministica do alinhamento que maximiza o IoU (COR-08/A1).

    ``alinhamento_inicial`` = (ax, bx, ay, by) do alinhamento por caixas
    (o chamador usa as caixas robustas; a busca parte dali). Tres estagios,
    em grade FIXA, na mesma ordem sempre; empate mantem o primeiro
    candidato (``>`` estrito), logo o resultado e deterministico:

    1. escala uniforme grossa: s em 0,80..1,25 passo 0,05, dx/dy em
       -24..24 passo 4 (grade da mascara de trabalho, em px);
    2. escala uniforme fina ao redor do melhor: s +-0,04 passo 0,01,
       dx/dy +-3 passo 1;
    3. afim com trava de aspecto: sx/sy independentes em +-0,06 passo
       0,02 ao redor do melhor corrente, com |sx/sy - 1| <= 0,15 (a trava
       do estudo: sem ela, uma vista genuinamente anisotropica seria
       "corrigida" por um esticamento que destroi as proporcoes internas),
       dx/dy +-2. Nos estagios 2 e 3, o centro da busca acompanha o melhor
       corrente (hill-climbing em grade fixa, ainda deterministico).

    Em cada estagio, o candidato e o inicial composto com (s, dx, dy) ao
    redor do centro da caixa da arte: ax' = s*ax0, bx' = s*bx0 + (1-s)*cx
    + dx (idem y, com sy no estagio afim). Se o IoU inicial ja for >=
    0,999, retorna o inicial sem buscar (nada a ganhar; 0 candidatos).

    Devolve (ax, bx, ay, by, info), com info = iou_inicial, iou_final,
    modo ("inicial" | "uniforme" | "afim": o estagio que produziu o melhor
    final), escala_x, escala_y (relativas ao inicial), deslocamento_px
    (dx, dy finais, na grade de trabalho) e candidatos_avaliados.
    Mascaras de formatos diferentes ou vazias levantam ValueError (a
    entrada malformada e recusada, nunca alinhada em silencio).
    """
    if mascara_malha.shape != mascara_arte.shape:
        raise ValueError(f"mascaras de formatos diferentes: {mascara_malha.shape} x {mascara_arte.shape}")
    if not mascara_malha.any() or not mascara_arte.any():
        raise ValueError("otimizar_alinhamento: mascara vazia (malha ou arte)")
    ax0, bx0, ay0, by0 = (float(v) for v in alinhamento_inicial)
    if ax0 == 0 or ay0 == 0:
        raise ValueError(f"escala zero no alinhamento inicial: ax={ax0} ay={ay0}")
    bbox_a = bbox_mascara(mascara_arte)
    cx = (bbox_a[0] + bbox_a[2]) / 2.0
    cy = (bbox_a[1] + bbox_a[3]) / 2.0
    h, w = mascara_malha.shape
    xs, ys = np.meshgrid(np.arange(w), np.arange(h))

    def _iou_de(ax, bx, ay, by):
        mx = ((xs - bx) / ax).astype(int)
        my = ((ys - by) / ay).astype(int)
        dentro = (mx >= 0) & (mx < w) & (my >= 0) & (my < h)
        alinhada = np.zeros((h, w), dtype=bool)
        alinhada[dentro] = mascara_malha[my[dentro], mx[dentro]]
        return iou(alinhada, mascara_arte)

    def _composto(sx, sy, dx, dy):
        return (sx * ax0, sx * bx0 + (1.0 - sx) * cx + dx,
                sy * ay0, sy * by0 + (1.0 - sy) * cy + dy)

    iou_ini = _iou_de(ax0, bx0, ay0, by0)
    info_base = {"iou_inicial": round(float(iou_ini), 4)}
    if iou_ini >= 0.999:
        return (ax0, bx0, ay0, by0,
                {**info_base, "iou_final": round(float(iou_ini), 4), "modo": "inicial",
                 "escala_x": 1.0, "escala_y": 1.0, "deslocamento_px": [0, 0],
                 "candidatos_avaliados": 0})
    melhor = (ax0, bx0, ay0, by0)
    melhor_iou = iou_ini
    modo = "inicial"
    bs, bdx, bdy = 1.0, 0, 0
    n = 0
    # Estagio 1: escala uniforme grossa.
    for s in [0.80 + 0.05 * i for i in range(10)]:
        for dx in range(-24, 25, 4):
            for dy in range(-24, 25, 4):
                cand = _composto(s, s, dx, dy)
                v = _iou_de(*cand)
                n += 1
                if v > melhor_iou:
                    melhor, melhor_iou, modo = cand, v, "uniforme"
                    bs, bdx, bdy = s, dx, dy
    # Estagio 2: escala uniforme fina ao redor do melhor.
    for ds in [-0.04 + 0.01 * i for i in range(9)]:
        s = bs + ds
        if s <= 0:
            continue
        for dx in range(bdx - 3, bdx + 4):
            for dy in range(bdy - 3, bdy + 4):
                cand = _composto(s, s, dx, dy)
                v = _iou_de(*cand)
                n += 1
                if v > melhor_iou:
                    melhor, melhor_iou, modo = cand, v, "uniforme"
                    bs, bdx, bdy = s, dx, dy
    # Estagio 3: afim com trava de aspecto, ao redor do melhor uniforme.
    bsx, bsy = bs, bs
    for dsx in [-0.06 + 0.02 * i for i in range(7)]:
        for dsy in [-0.06 + 0.02 * i for i in range(7)]:
            sx, sy = bsx + dsx, bsy + dsy
            if sx <= 0 or sy <= 0 or abs(sx / sy - 1.0) > 0.15:
                continue
            for dx in range(bdx - 2, bdx + 3):
                for dy in range(bdy - 2, bdy + 3):
                    cand = _composto(sx, sy, dx, dy)
                    v = _iou_de(*cand)
                    n += 1
                    if v > melhor_iou:
                        melhor, melhor_iou, modo = cand, v, "afim"
                        bsx, bsy, bdx, bdy = sx, sy, dx, dy
    ax, bx, ay, by = melhor
    return (ax, bx, ay, by,
            {**info_base, "iou_final": round(float(melhor_iou), 4), "modo": modo,
             "escala_x": round(float(ax / ax0), 4), "escala_y": round(float(ay / ay0), 4),
             "deslocamento_px": [int(bdx), int(bdy)], "candidatos_avaliados": int(n)})


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
    ``peso_face`` (F,) float (facing por face, pre-calculado). Uma vista
    pode trazer ``alinhamento`` = (ax, bx, ay, by) ja calculado (COR-08/A1,
    pelo ``_blender_cor``): nesse caso o override SUBSTITUI o alinhamento
    por caixas dessa vista, e ``info["alinhamento_usado"][nome]`` registra
    "otimizado"; sem a chave, o caminho v1 e mantido byte a byte.
    Retorna (textura TxTx3, pintado TxT bool, melhor_peso TxT float, info).
    """
    tex = np.zeros((tamanho, tamanho, 3), dtype=np.float64)
    pintado = np.zeros((tamanho, tamanho), dtype=bool)
    melhor = np.zeros((tamanho, tamanho), dtype=np.float64)
    info = {"faces_pintadas_por_vista": {}, "texels_por_vista": {},
            "alinhamento_usado": {}}
    for v in vistas:
        nome = v["vista"]
        imagem = v["imagem"]
        mascara = v["mascara"]
        visivel = v["visivel"]
        peso_face = v["peso_face"]
        hi, wi = mascara.shape
        bbox_a = bbox_mascara(mascara)
        if bbox_a is None:
            info["faces_pintadas_por_vista"][nome] = 0
            info["texels_por_vista"][nome] = 0
            info["alinhamento_usado"][nome] = "nenhum (mascara vazia)"
            continue
        if v.get("alinhamento") is not None:
            ax, bx, ay, by = (float(c) for c in v["alinhamento"])
            info["alinhamento_usado"][nome] = "otimizado"
        else:
            # Caixa da malha projetada nesta vista, em pixels da imagem.
            px_all, py_all = projetar(verts, centro, nome, ortho_scale, wi, hi)
            bbox_m = (int(math.floor(px_all.min())), int(math.floor(py_all.min())),
                      int(math.ceil(px_all.max())), int(math.ceil(py_all.max())))
            ax, bx, ay, by = alinhamento_silhueta(bbox_a, bbox_m)
            info["alinhamento_usado"][nome] = "bbox"
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
            # COR-08/A0: a amostragem subtrai o centro, como ``projetar``
            # faz. Antes, p3d absoluto era projetado direto: com o centro
            # real do Orc (z = 0,5, ortho 1,1), a amostra vertical caia
            # ~0,45 * altura da imagem acima do ponto certo - a base
            # amostrando o meio, o topo amostrando o fundo. O teste de
            # cor solida do T1 nao via o deslocamento (cor uniforme); o
            # teste de faixas (test_amostragem_usa_centro_faixas) o trava.
            rel = p3d - np.asarray(centro, dtype=np.float64)
            qx = rel @ direita
            qy = rel @ cima
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


def dilatar(textura: np.ndarray, pintado: np.ndarray, iteracoes: int,
            dominio: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray, int]:
    """Preenche texels sem fonte com a cor vizinha mais proxima, 1 px por passe.

    Retorna (textura, pintado_final, n_preenchidos). Ordem de vizinhos fixa
    (cima, baixo, esquerda, direita) para determinismo.

    COR-08/A3: ``dominio`` (bool, mesmo formato) restringe ONDE a dilatacao
    pode pintar; sem ele, o comportamento v1 (tudo) e mantido. A dilatacao
    restrita e o ultimo recurso anti-halo da A3: o preenchimento das zonas
    cegas e 3D (``preenchimento``), e a dilatacao so cobre a faixa em
    torno da UV que o dominio delimita.
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
            if dominio is not None:
                alvo &= dominio
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
