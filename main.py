# auto_ip_changer.py на телефоне
import time
import subprocess
import re
import requests


class AutoIPChanger:
    def __init__(self):
        pass
    
    def toggle_mobile_data(self):
        """Перезагрузка мобильных данных (работает без root)"""
        try:
            print("📡 Перезагружаем мобильные данные...")
            
            # Отключаем мобильные данные
            subprocess.run([
                'svc', 'data', 'disable'
            ], check=False, timeout=10)
            
            time.sleep(3)
            
            # Включаем мобильные данные
            subprocess.run([
                'svc', 'data', 'enable'
            ], check=False, timeout=10)
            
            time.sleep(5)
            print("✅ Мобильные данные перезагружены")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка перезагрузки данных: {e}")
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
            """Быстрое получение внешнего IP"""
            fast_services = [
                'https://api.ipify.org',
            ]
            
            for service in fast_services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        ip = response.text.strip()
                        if self.is_valid_ip(ip):
                            return ip
                except:
                    continue
            
            return "Не удалось получить IP"
            

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