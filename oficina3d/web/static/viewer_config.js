// Configuração global do <model-viewer>, lida por ele ao carregar (tem de vir antes do script dele).
// Decodificador Draco local (static/vendor/draco/): sem isso o model-viewer buscaria na internet.
self.ModelViewerElement = self.ModelViewerElement || {};
self.ModelViewerElement.dracoDecoderLocation = "/static/vendor/draco/";
