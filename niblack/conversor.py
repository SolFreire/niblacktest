import serial
import time

PORTA = 'debug/console'
BAUDRATE = 38400
TIMEOUT = 1
OUT_FILE = 'out_stm.pgm'

try:
    uart = serial.Serial(PORTA, BAUDRATE, timeout=TIMEOUT)
    print(f"Conectado a porta {PORTA} a {BAUDRATE} bps.")

    time.sleep(2)

    with open(OUT_FILE, 'w', encoding='utf-8') as arquivo:
        print("Comecando a leitura da serial (Ctrl+C para parar)...")

        while True:
            linha = uart.readline().decode('utf-8', errors='ignore').strip()
            if linha:
                print(linha)
                arquivo.write(linha + '\n')
                arquivo.flush()

except KeyboardInterrupt:
    print("\nLeitura interrompida pelo usuário.")

except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")

finally:
    if 'uart' in locals() and uart.is_open:
        uart.close()
        print("Porta serial fechada.")