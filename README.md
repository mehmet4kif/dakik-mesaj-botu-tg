# dakik-mesaj-botu-tg
Belirlediğiniz periyotlarla belirlediğiniz telegram gruplarına mesaj gönderen bir telegram botu.

# Telegram Bot Kullanım Kılavuzu

Bu bot, belirli gruplara belirli aralıklarla mesaj veya resim göndermenizi sağlar. İşte botu kullanırken ihtiyaç duyacağınız tüm komutlar ve örnekler:
## 1. Botu Başlatma

Komut: /start
Açıklama: Botu başlatır ve kullanım kılavuzunu gösterir.
## 2. Grup Ekleme

Komut: /add_group <kısa_id> <grup_id> <grup_ismi>
Açıklama: Bir grubu listeye ekler. Kısa ID, grup ID'sini daha kolay kullanmanız için oluşturulan bir kısayoldur.
Örnek: /add_group k1 123456789 Grup İsmi
Açıklama: k1 kısa ID'siyle 123456789 grup ID'sine sahip "Grup İsmi" adında bir grup ekler.
## 3. Metin Mesajı Zamanlama

Komut: /schedule <kısa_id> <dakika> <mesaj>
Açıklama: Belirli bir gruba belirli aralıklarla metin mesajı gönderir.
Örnek: /schedule k1 30 Merhaba Grup
Açıklama: k1 kısa ID'li gruba her 30 dakikada bir "Merhaba Grup" mesajı gönderir.
## 4. Resim Mesajı Zamanlama

Komut: /schedule_photo <kısa_id> <dakika> <resim_url>
Açıklama: Belirli bir gruba belirli aralıklarla resim gönderir.
Örnek: /schedule_photo k1 45 https://example.com/image.jpg
Açıklama: k1 kısa ID'li gruba her 45 dakikada bir "https://example.com/image.jpg" adresindeki resmi gönderir.
## 5. Zamanlanmış Görevleri Listeleme

Komut: /list_scheduled
Açıklama: Zamanlanmış tüm görevleri listeler.
## 6. Bilinen Grupları Listeleme

Komut: /list_groups
Açıklama: Botun bildiği tüm grupları listeler.
## 7. Bilinen Gruplara Mesaj Gönderme

Komut: /send_message <kısa_id> <mesaj>
Açıklama: Belirli bir gruba anında metin mesajı gönderir.
Örnek: /send_message k1 Anlık Mesaj
Açıklama: k1 kısa ID'li gruba "Anlık Mesaj" gönderir.
## 8. Bilinen Gruplara Resim Gönderme

Komut: /send_photo <kısa_id> <resim_url>
Açıklama: Belirli bir gruba anında resim gönderir.
Örnek: /send_photo k1 https://example.com/image.jpg
Açıklama: k1 kısa ID'li gruba "https://example.com/image.jpg" adresindeki resmi gönderir.
## Notlar:
#### Grup ID'si Nasıl Bulunur?: Bot bir gruba eklendiğinde, grup ID'sini otomatik olarak tespit eder ve bilinen gruplar listesine ekler.
#### Kısa ID Kullanımı: Kısa ID, uzun grup ID'si yerine kullanılabilir. Örneğin, k1 kısa ID'si 123456789 grup ID'sini temsil edebilir.
#### Admin Bilgilendirmesi: Mesaj veya resim gönderimi başarılı veya başarısız olduğunda, admin kullanıcıya bilgilendirme mesajı gönderilir.
