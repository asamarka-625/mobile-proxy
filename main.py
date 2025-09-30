# auto_ip_changer.py на телефоне
import time
import subprocess
import re
import requests


class AutoIPChanger:
    def __init__(self):
        pass
    
    def toggle_mobile_data(self):
        """Управление мобильными данными через Termux:API"""
        try:
            print("📡 Управляем мобильными данными через Termux API...")
            
            # Проверяем доступность Termux:API
            result = subprocess.run(
                ['termux-telephony-deviceinfo'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print("❌ Termux:API не установлен")
                return self.fallback_method()
            
            # Отключаем мобильные данные
            print("🔴 Отключаем мобильные данные...")
            subprocess.run([
                'termux-telephony-call', '##4636##'
            ], check=False, timeout=10)
            
            time.sleep(5)
            
            # Включаем мобильные данные
            print("🟢 Включаем мобильные данные...")
            subprocess.run([
                'termux-telephony-call', '*#*#4636#*#*'
            ], check=False, timeout=10)
            
            time.sleep(8)
            print("✅ Мобильные данные перезагружены")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка Termux API: {e}")
            return self.fallback_method()
    
    
    def check_ip_change(self):
        """Проверяем, изменился ли IP"""
        try:
            old_ip = self.get_current_ip()
            print(f"📱 Старый IP: {old_ip}")
            
            while True:
                time.sleep(5)
                # Пытаемся сменить IP
                if self.toggle_mobile_data():
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