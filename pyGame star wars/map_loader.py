def harita_yukle(dosya_adı):
    
    harita = []
    kotu_karakterler = []
    
    try:
        with open(dosya_adı, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()
        
        
        for satir in satirlar:
            satir = satir.strip()
            if satir.startswith("Karakter:"):
                parcalar = satir[9:].split(",")  
                if len(parcalar) == 2:
                    karakter_bilgi = parcalar[0]
                    kapi_bilgi = parcalar[1]
                    
                    
                    if karakter_bilgi.startswith("Stormtrooper"):
                        karakter_ad = "Stormtrooper"
                    elif karakter_bilgi.startswith("Darth Vader"):
                        karakter_ad = "Darth Vader"
                    elif karakter_bilgi.startswith("Kylo Ren"):
                        karakter_ad = "Kylo Ren"
                    else:
                        print(f"Bilinmeyen karakter: {karakter_bilgi}")
                        continue
                    
                    
                    if kapi_bilgi.startswith("Kapi:"):
                        kapi = kapi_bilgi[5:].strip()
                    else:
                        print(f"Geçersiz kapı bilgisi: {kapi_bilgi}")
                        continue
                    
                    kotu_karakterler.append((karakter_ad, kapi))
                    print(f"Karakter yüklendi: {karakter_ad}, Kapı: {kapi}")
        
        
        harita_basladi = False
        for satir in satirlar:
            satir = satir.strip()
            if not satir.startswith("Karakter:") and "\t" in satir:
                try:
                    
                    sayilar = [int(x) for x in satir.split("\t")]
                    harita.append(sayilar)
                    harita_basladi = True
                except ValueError:
                    if harita_basladi:
                        
                        print(f"Harita satırı geçersiz: {satir}")
        
        print(f"Harita boyutu: {len(harita)} satır x {len(harita[0])} sütun")
        print(f"Yüklenen düşman karakterler: {kotu_karakterler}")
        
        return harita, kotu_karakterler
    
    except Exception as e:
        print(f"Harita yükleme hatası: {e}")
        
        return [[1, 1], [1, 1]], []

if __name__ == "__main__":
    harita, dusmanlar = harita_yukle("maps/Star wars harita.txt")
    print("Harita:", harita)
    print("Düşmanlar:", dusmanlar)