# auto_ip_changer.py на телефоне
import time
import subprocess
import re


class AutoIPChanger:
    def __init__(self):
        pass
    
    def toggle_flight_mode_adb(self):
        """Режим полета через ADB (работает без root)"""
        try:
            # Включаем режим полета
            subprocess.run(['adb', 'shell', 'settings', 'put', 'global', 'airplane_mode_on', '1'], check=True)
            subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'android.intent.action.AIRPLANE_MODE'], check=True)
            time.sleep(3)
            
            # Выключаем режим полета
            subprocess.run(['adb', 'shell', 'settings', 'put', 'global', 'airplane_mode_on', '0'], check=True)
            subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'android.intent.action.AIRPLANE_MODE'], check=True)
            time.sleep(5)
            print("✅ Режим полета переключен")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка ADB: {e}")
            return False
    
    
    def check_ip_change(self):
        """Проверяем, изменился ли IP"""
        try:
            old_ip = self.get_current_ip()
            print(f"📱 Старый IP: {old_ip}")
            
            while True:
            time.sleep(5)
            # Пытаемся сменить IP
            if self.toggle_flight_mode_adb():
                break
            
            time.sleep(10)  # Ждем получения нового IP
            new_ip = self.get_current_ip()
            print(f"📱 Новый IP: {new_ip}")
            
            return old_ip != new_ip
            
        except Exception as e:
            print(f"❌ Ошибка проверки IP: {e}")
            return False
    
    def get_current_ip(self):
        """Простой способ получить мобильный IP"""
        try:
            # Пробуем несколько команд
            commands = [
                ['ip', 'route', 'get', '8.8.8.8'],
                ['netstat', '-rn'],
                ['ifconfig']
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        # Ищем IP в выводе
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
                        if ip_match:
                            return ip_match.group(1)
                except:
                    continue
            
            return "IP не определен"
            
        except Exception as e:
            return f"Ошибка: {e}"
            

if __name__ == "__main__":
    mobile_changer = AutoIPChanger()
    mobile_changer
    
    while True:
        try:
            print("Ждем 10 секунд")
            time.sleep(10)
            mobile_changer.check_ip_change()
        
        except Exception as err:
            print(err)
            break