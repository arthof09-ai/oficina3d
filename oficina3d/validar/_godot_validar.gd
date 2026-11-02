# Validador headless do Godot (Fase 2, item 1 do plano v2).
#
# Uso (o Python chama assim; ver oficina3d/validar/godot.py):
#   Godot_v4.7.2-stable_win64_console.exe --headless --script _godot_validar.gd -- <arquivo.glb>
# (sem --quiet: o --quiet do Godot cala tambem o print desta linha)
#
# Carrega o GLB pelo mesmo caminho do jogo em tempo de execucao
# (GLTFDocument.append_from_file + generate_scene) e imprime UMA linha
# "VALIDACAO_JSON {...}". Codigo de saida: 0 = carregou, 2 = argumento
# faltando, 3 = o Godot nao conseguiu abrir/gerar a cena.
# Medido em 01/11/2026: no --headless (renderizador dummy) a malha sai como
# ImporterMeshInstance3D/ImporterMesh, nao MeshInstance3D; por isso as duas
# formas sao contadas e a caixa envolvente sai dos vertices, nao do AABB do no.
# Nao grava nada em disco e nao abre janela (nao renderiza: capturas de tela
# ficam com as previas do Blender, ver docstring do pacote).
extends SceneTree


func _superficies(m) -> Array:
	# [[arrays, material], ...] para Mesh (ArrayMesh) ou ImporterMesh.
	var out := []
	if m == null:
		return out
	if m is ImporterMesh:
		for s in m.get_surface_count():
			out.append([m.get_surface_arrays(s), m.get_surface_material(s)])
	elif m is Mesh:
		for s in m.get_surface_count():
			out.append([m.surface_get_arrays(s), m.surface_get_material(s)])
	return out


func _contar(no: Node, xf: Transform3D, r: Dictionary) -> void:
	var xf_no := xf
	if no is Node3D:
		xf_no = xf * no.transform
	var malha = null
	if no is MeshInstance3D or no is ImporterMeshInstance3D:
		malha = no.mesh
		r["mesh_instances"] += 1
	for sup in _superficies(malha):
		var arr: Array = sup[0]
		var mat = sup[1]
		r["superficies"] += 1
		var pos = arr[Mesh.ARRAY_VERTEX]
		var idx = arr[Mesh.ARRAY_INDEX]
		var nv: int = 0 if pos == null else pos.size()
		r["vertices"] += nv
		r["triangulos"] += (idx.size() / 3) if (idx != null and idx.size() > 0) else (nv / 3)
		if arr[Mesh.ARRAY_TEX_UV] != null and arr[Mesh.ARRAY_TEX_UV].size() == nv and nv > 0:
			r["superficies_com_uv"] += 1
		if arr[Mesh.ARRAY_COLOR] != null and arr[Mesh.ARRAY_COLOR].size() == nv and nv > 0:
			r["superficies_com_cor_vertice"] += 1
		if arr[Mesh.ARRAY_BONES] != null and arr[Mesh.ARRAY_BONES].size() > 0:
			r["superficies_com_pesos"] += 1
		for p in pos if pos != null else []:
			var w: Vector3 = xf_no * p
			if r["_vazio"]:
				r["_min"] = w
				r["_max"] = w
				r["_vazio"] = false
			else:
				r["_min"] = r["_min"].min(w)
				r["_max"] = r["_max"].max(w)
		if mat != null:
			r["_mats"][mat.get_instance_id()] = true
			if mat is BaseMaterial3D and mat.albedo_texture != null:
				r["superficies_com_albedo"] += 1
				var img: Image = mat.albedo_texture.get_image()
				if img != null:
					r["albedo_px"] = max(r["albedo_px"], max(img.get_width(), img.get_height()))
	if no is Skeleton3D:
		r["esqueletos"] += 1
		r["ossos"] += no.get_bone_count()
	if no is AnimationPlayer:
		for nome in no.get_animation_list():
			r["animacoes"].append(str(nome))
	for filho in no.get_children():
		_contar(filho, xf_no, r)


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() < 1:
		print("VALIDACAO_JSON ", JSON.stringify({"ok": false, "erro": "faltou o caminho do GLB"}))
		quit(2)
		return
	var doc := GLTFDocument.new()
	var estado := GLTFState.new()
	# 3 = HANDLE_BINARY_IMAGE_EMBED_AS_UNCOMPRESSED. O padrao (1, extrair texturas)
	# derruba o Godot 4.7.2 com 0xC0000005 em GLB com textura fora do editor
	# (medido em 01/11/2026 com o modelo_cor.glb da COR-08; modos 0, 2 e 3 carregam).
	estado.handle_binary_image = 3
	var t0 := Time.get_ticks_msec()
	var err := doc.append_from_file(args[0], estado)
	if err != OK:
		print("VALIDACAO_JSON ", JSON.stringify({"ok": false, "erro": "append_from_file falhou: " + error_string(err)}))
		quit(3)
		return
	var cena: Node = doc.generate_scene(estado)
	if cena == null:
		print("VALIDACAO_JSON ", JSON.stringify({"ok": false, "erro": "generate_scene devolveu null"}))
		quit(3)
		return
	var r := {
		"ok": true, "mesh_instances": 0, "superficies": 0, "vertices": 0, "triangulos": 0,
		"superficies_com_uv": 0, "superficies_com_cor_vertice": 0, "superficies_com_pesos": 0, "superficies_com_albedo": 0,
		"albedo_px": 0, "esqueletos": 0, "ossos": 0, "animacoes": [],
		"_mats": {}, "_vazio": true, "_min": Vector3.ZERO, "_max": Vector3.ZERO,
	}
	_contar(cena, Transform3D.IDENTITY, r)
	r["materiais"] = r["_mats"].size()
	r["caixa_min"] = [r["_min"].x, r["_min"].y, r["_min"].z]
	r["caixa_max"] = [r["_max"].x, r["_max"].y, r["_max"].z]
	for k in ["_mats", "_vazio", "_min", "_max"]:
		r.erase(k)
	r["gltf"] = {"malhas": estado.get_meshes().size(), "nos": estado.get_nodes().size(),
		"materiais": estado.get_materials().size(), "texturas": estado.get_textures().size(),
		"imagens": estado.get_images().size(), "skins": estado.get_skins().size(),
		"animacoes": estado.get_animations().size()}
	r["tempo_ms"] = Time.get_ticks_msec() - t0
	r["godot"] = Engine.get_version_info()["string"]
	print("VALIDACAO_JSON ", JSON.stringify(r))
	cena.free()
	quit(0)
