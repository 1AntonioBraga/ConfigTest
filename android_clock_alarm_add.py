import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta

ADB_PACKAGE = "com.sec.android.app.clockpackage"

def nowlog(level: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

def run_adb(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    adb = shutil.which("adb")
    if not adb:
        raise RuntimeError("ADB não encontrado no PATH.")

    result = subprocess.run([adb, *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Erro no ADB: {result.stderr or result.stdout}")
    return result

def test_alarm_flow_qa() -> str:
    nowlog("INFO", "Iniciando caso de teste de automação de alarme (Sem Root)")
    try:
        # PASSO 1: Parar o app
        nowlog("INFO", "Passo 1: Cancelando instruções anteriores e fechando o Clock...")
        run_adb("shell", "am", "force-stop", ADB_PACKAGE)
        time.sleep(1)

        # PASSO 2: Ler a hora atual do aparelho e calcular o alarme
        nowlog("INFO", "Passo 2: Calculando horário do alarme baseado na hora atual...")
        hora_celular = run_adb("shell", "date", '+"%H %M"').stdout.strip()
        hora_str, min_str = hora_celular.split()
        
        # O Python converte o texto em horas e soma 1 minuto com segurança
        hora_obj = datetime.strptime(f"{hora_str}:{min_str}", "%H:%M")
        alarme_obj = hora_obj + timedelta(minutes=1)
        
        ALARM_HOUR = alarme_obj.hour
        ALARM_MINUTE = alarme_obj.minute
        nowlog("INFO", f"Hora atual do aparelho: {hora_str}:{min_str} -> Alarme configurado para: {ALARM_HOUR:02d}:{ALARM_MINUTE:02d}")

        # PASSO 3: Enviar o comando
        nowlog("INFO", f"Passo 3: Configurando o novo alarme para as {ALARM_HOUR:02d}:{ALARM_MINUTE:02d}...")
        run_adb(
            "shell", "am", "start", "-a", "android.intent.action.SET_ALARM",
            "--ei", "android.intent.extra.alarm.HOUR", str(ALARM_HOUR),
            "--ei", "android.intent.extra.alarm.MINUTES", str(ALARM_MINUTE),
            "--es", "android.intent.extra.alarm.MESSAGE", "Teste_QA", # <-- A MÁGICA ESTÁ AQUI (Sem espaços)
            "--ez", "android.intent.extra.alarm.SKIP_UI", "true"
        )
        
        # PASSO 4: Esperar o disparo físico (1 minuto + margem de erro)
        nowlog("INFO", "Passo 4: Aguardando 65 segundos em tempo real para o disparo do alarme...")
        time.sleep(65)

        # PASSO 5: Validar o hardware
        nowlog("INFO", "Passo 5: Validando logs de hardware (Áudio)...")
        audio_dump = run_adb("shell", "dumpsys", "audio").stdout.lower()
        is_ringing = "streamtype:4" in audio_dump or "stream type:4" in audio_dump or "stream_alarm" in audio_dump

        if not is_ringing:
            nowlog("ERROR", "Validação falhou: Áudio do alarme não foi detectado no hardware.")
            return "FAIL: O alarme não disparou"

        nowlog("SUCCESS", "Todas as etapas concluídas! O Alarme tocou com sucesso.")
        return "PASS"

    except Exception as e:
        nowlog("ERROR", f"Exceção capturada: {str(e)}")
        return f"FAIL: Erro durante a execução: {str(e)}"

    finally:
        nowlog("INFO", "Teardown: Parando o alarme que está tocando e limpando o app...")
        try:
            run_adb("shell", "am", "force-stop", ADB_PACKAGE)
            run_adb("shell", "pm", "clear", ADB_PACKAGE)
        except Exception as ex:
            nowlog("WARN", f"Falha no teardown: {ex}")

if __name__ == "__main__":
    resultado_teste = test_alarm_flow_qa()
    print("\n=======================================")
    print(f" RESULTADO FINAL DO LOG: {resultado_teste}")
    print("=======================================")
    if resultado_teste.startswith("FAIL"):
        sys.exit(1)
    sys.exit(0)