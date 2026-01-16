"""
Verificador de compatibilidade do Python
Execute este arquivo para verificar se sua versão do Python é compatível
"""

import sys
import platform

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("=" * 50)
    print("PCBBR - Verificação de Compatibilidade Python")
    print("=" * 50)
    print()
    
    # Versão do Python
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"🐍 Python detectado: {version_str}")
    print(f"📦 Implementação: {platform.python_implementation()}")
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🏗️  Arquitetura: {platform.machine()}")
    print()
    
    # Verificar versão mínima (3.10)
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ ERRO: Python 3.10 ou superior é necessário!")
        print(f"   Versão atual: {version_str}")
        print(f"   Versão mínima: 3.10.0")
        print()
        print("📥 Baixe Python 3.10+ de:")
        print("   https://www.python.org/downloads/")
        return False
    
    print(f"✅ Versão do Python compatível: {version_str} >= 3.10.0")
    print()
    
    # Verificar módulos essenciais
    print("Verificando módulos essenciais do Python:")
    
    required_modules = ['venv', 'pip', 'sqlite3']
    all_ok = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} não encontrado!")
            all_ok = False
    
    print()
    
    if not all_ok:
        print("⚠️  Alguns módulos essenciais não foram encontrados.")
        print("   Reinstale o Python marcando 'Install pip' e 'Install for all users'")
        return False
    
    # Verificar pip
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip: {result.stdout.strip()}")
        else:
            print("❌ pip não está funcionando corretamente")
            all_ok = False
    except Exception as e:
        print(f"❌ Erro ao verificar pip: {e}")
        all_ok = False
    
    print()
    print("=" * 50)
    
    if all_ok:
        print("✅ Sistema pronto para instalar o PCBBR!")
        print()
        print("Próximos passos:")
        print("  1. Execute: setup.bat (Windows) ou python -m venv .venv (Linux/Mac)")
        print("  2. Ative o ambiente virtual")
        print("  3. Instale dependências: pip install -r backend/requirements.txt")
        return True
    else:
        print("❌ Problemas encontrados. Consulte TROUBLESHOOTING.md")
        return False

if __name__ == "__main__":
    try:
        success = check_python_version()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
