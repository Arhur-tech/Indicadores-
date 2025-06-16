import http.server
import socketserver
import webbrowser
import os
import sys
from urllib.parse import urlparse, parse_qs
import json
import threading
import time

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Adicionar headers CORS para resolver problemas de API
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Responder a requisições OPTIONS para CORS
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        # Redirecionar a raiz para a página de segmentos
        if self.path == '/':
            self.path = '/segmentos.html'
        
        # Servir arquivos normalmente
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Log personalizado
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def start_server(port=8000):
    """Inicia o servidor HTTP na porta especificada"""
    
    # Verificar se a porta está disponível
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("🚀 SERVIDOR DASHBOARD DE INDICADORES INICIADO")
            print("=" * 60)
            print(f"📍 Servidor rodando em: http://localhost:{port}")
            print(f"📂 Diretório: {os.path.dirname(os.path.abspath(__file__))}")
            print()
            print("📱 PÁGINAS DISPONÍVEIS:")
            print(f"   🏠 Página Inicial: http://localhost:{port}/")
            print(f"   📊 Segmentos: http://localhost:{port}/segmentos.html")
            print(f"   📈 Dashboard: http://localhost:{port}/Index.html")
            print(f"   📋 Indicadores: http://localhost:{port}/indicadores-segmento.html")
            print()
            print("💡 DICAS:")
            print("   • O servidor resolve problemas de CORS automaticamente")
            print("   • Suas páginas serão atualizadas automaticamente")
            print("   • Pressione Ctrl+C para parar o servidor")
            print("=" * 60)
            
            # Abrir navegador automaticamente após 2 segundos
            def open_browser():
                time.sleep(2)
                try:
                    webbrowser.open(f'http://localhost:{port}/')
                    print(f"🌐 Navegador aberto automaticamente!")
                except:
                    print("⚠️ Não foi possível abrir o navegador automaticamente")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48 or e.errno == 10048:  # Address already in use
            print(f"❌ Erro: A porta {port} já está em uso!")
            print(f"💡 Tentando porta {port + 1}...")
            start_server(port + 1)
        else:
            print(f"❌ Erro ao iniciar servidor: {e}")
            sys.exit(1)

def main():
    """Função principal"""
    port = 8000
    
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Porta inválida! Usando porta padrão 8000")
            port = 8000
    
    try:
        start_server(port)
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("🛑 SERVIDOR PARADO PELO USUÁRIO")
        print("=" * 60)
        print("✅ Servidor encerrado com sucesso!")
        print("🙏 Obrigado por usar o Dashboard de Indicadores!")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
