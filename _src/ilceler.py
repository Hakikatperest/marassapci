# Kahramanmaraş ilçe verisi — ilçe sayfalarının ilçeye özel bölümleri.
# tip: merkez | ova | yayla | dag  → şap uygulamasında iklim notlarını seçer.
# Doğrulanmamış rakam (km, rakım, nüfus) YAZILMADI; yalnız genel bilinen olgular.

ILCELER = [
 dict(ad="Onikişubat", de="Onikişubat'ta", slug="onikisubat-sapci", tip="merkez", komsu=["dulkadiroglu-sapci", "turkoglu-sapci", "andirin-sapci"],
  giris=["Onikişubat, Kahramanmaraş merkezinin kuzey ve batı yakasını kapsıyor. 6 Şubat depreminden sonra şehrin en çok "
         "yeni bina yükselen bölgelerinden biri burası; kalıcı konut alanları, yeni siteler ve yeniden yapılan apartmanlar "
         "şap işinin büyük kısmını oluşturuyor.",
         "Apartman işlerinde şapı pompayla katlara basıyoruz. Pompa aşağıda kalıyor, hortum merdiven boşluğundan ya da "
         "pencereden kata çıkıyor; malzeme kova kova taşınmadığı için katlar arasında süre farkı oluşmuyor."],
  dikkat=["Yeni sitelerde birden fazla blok aynı hafta şap bekliyor; blok sırasını ve kat sırasını baştan konuşuyoruz.",
          "Kot farkını kapı eşiğine göre değil, dairenin en yüksek noktasına göre alıyoruz; seramik ve parke aynı seviyede biter.",
          "Yerden ısıtma döşenen dairelerde borunun üstünde yeterli şap kalınlığı bırakıyoruz."],
  sss=[("Onikişubat'ta yeni sitelere toplu şap yapıyor musunuz?",
        "Evet. Blok ve kat sayısını, toplam metrekareyi bildirin; iş sırasını ve teklifinizi buna göre hazırlayalım."),
       ("Kat yüksekliği fiyatı değiştirir mi?",
        "Pompa ile basıldığı için katlar arasında işçilik farkı çoğu zaman olmuyor. Hortumun ulaşamayacağı özel bir "
        "durum varsa keşifte söylüyoruz.")]),
 dict(ad="Dulkadiroğlu", de="Dulkadiroğlu'nda", slug="dulkadiroglu-sapci", tip="merkez", komsu=["onikisubat-sapci", "pazarcik-sapci", "turkoglu-sapci"],
  giris=["Dulkadiroğlu, merkezin doğu ve güney yakası. Burada yeni yapılan binaların yanında depremde hasar alıp "
         "güçlendirilen, iç tadilata giren daire ve dükkanlar da çok. Şap işi bazen boş bir betonarme katta, bazen eski "
         "zemini sökülmüş bir dükkanda başlıyor.",
         "Tadilat işlerinde önce eski zeminin durumuna bakıyoruz: kırılan, kabaran ya da kot farkı olan yerler varsa şaptan "
         "önce söylüyoruz. Eski zeminin üstüne körlemesine şap dökmüyoruz."],
  dikkat=["Dükkan ve iş yerlerinde zemin vitrin ve kapı kotuna göre ayarlanır; dışarıdan su girmeyecek eğimi baştan alırız.",
          "Tadilatta tesisat ve elektrik boruları şaptan ÖNCE yerine oturmalı; sonradan kırmak hem işi hem zemini bozar.",
          "Eski şapın üstüne ince katman gerekiyorsa aderans (yapışma) için yüzey hazırlığını ayrıca yapıyoruz."],
  sss=[("Eski zemini sökülen dairede şap atılır mı?",
        "Atılır. Önce kalan zeminin sağlamlığına ve kot farkına bakıyoruz; gevşek kısımlar alınıp temizlendikten sonra şap atılır."),
       ("Dükkan zemini için şap uygun mu?",
        "Seramik, parke ya da epoksi altına şap uygun bir alt zemindir. Üst kaplamayı söylerseniz kalınlığı ona göre ayarlarız.")]),
 dict(ad="Pazarcık", de="Pazarcık'ta", slug="pazarcik-sapci", tip="ova", komsu=["dulkadiroglu-sapci", "turkoglu-sapci", "caglayancerit-sapci"],
  giris=["Pazarcık, 6 Şubat 2023'teki ilk büyük depremin merkez üssü. İlçe merkezinde ve köylerde yıkılan evlerin yerine "
         "yenileri yapılıyor; kalıcı konutlar, müstakil köy evleri ve tek katlı yapılar burada şap işlerinin çoğunu oluşturuyor.",
         "Müstakil ve tek katlı evlerde şapı zemin betonunun üstüne atıyoruz. Toprağa oturan zeminlerde nem yalıtımının "
         "yapılıp yapılmadığını soruyoruz; yapılmadıysa şaptan önce yapılmasını öneriyoruz."],
  dikkat=["Toprağa oturan zeminde nem yalıtımı yoksa üst kaplama zamanla kabarabilir; şaptan önce konuşuyoruz.",
          "Ova ilçesi olduğu için yazın sıcak ve kuru geçiyor; şapı ilk günlerde sulayarak çatlamadan kurutuyoruz.",
          "Köy evlerinde ahır, depo ve garaj zeminleri de şapla düzeltilebilir; ağır yük gelecekse kalınlığı artırıyoruz."],
  sss=[("Pazarcık köylerine geliyor musunuz?",
        "Pazarcık merkezine ve köylerine geliyoruz. Köy adını ve yaklaşık metrekareyi yazın, gün planlayalım."),
       ("Kalıcı konutta şap kalınlığı ne olmalı?",
        "Yaygın uygulama 5 cm civarıdır. Tesisat, yalıtım ya da yerden ısıtma varsa kalınlık yerinde ölçülerek belirlenir.")]),
 dict(ad="Elbistan", de="Elbistan'da", slug="elbistan-sapci", tip="yayla", komsu=["afsin-sapci", "ekinozu-sapci", "nurhak-sapci", "goksun-sapci"],
  giris=["Elbistan, Kahramanmaraş'ın merkezden sonraki en büyük ilçesi ve 6 Şubat'taki ikinci büyük depremin merkez üssü. "
         "Depremden sonra ilçe merkezinde ve ovadaki köylerde çok sayıda yeni konut yapılıyor.",
         "Elbistan yüksek bir ova üzerinde; kışlar uzun ve soğuk geçiyor. Bu yüzden burada şap takvimi merkezden farklı "
         "işliyor: dondan korunmayan şap yüzeyden dağılır, bunu bildiğimiz için soğuk havada döküm yapmıyoruz."],
  dikkat=["Gece donu beklenen günlerde şap dökmüyoruz; pencere ve kapısı takılmamış binada şap korunamaz.",
          "Kışa yetişmesi gereken işlerde sonbahar başında takvim çıkarıyoruz; geç kalan iş bahara kalabiliyor.",
          "Kaloriferli ya da yerden ısıtmalı binalarda şap kuruyana kadar ısıtmayı yüksek açmayın; ani kuruma çatlatır."],
  sss=[("Elbistan'da kışın şap atılır mı?",
        "Hava sıcaklığı ve bina kapalılığı uygunsa atılır. Gece donu varsa ve bina açıksa beklemenizi öneriyoruz; "
        "donan şap sonradan düzelmiyor."),
       ("Elbistan köylerine geliyor musunuz?",
        "Geliyoruz. Uzak köylerde işi tek güne toplamak için metrekare ve adres bilgisini önceden alıyoruz.")]),
 dict(ad="Afşin", de="Afşin'de", slug="afsin-sapci", tip="yayla", komsu=["elbistan-sapci", "goksun-sapci", "ekinozu-sapci"],
  giris=["Afşin, Elbistan ovasının batı ucunda, Afşin-Elbistan termik santrallerinin bulunduğu ilçe. Depremden etkilenen "
         "ilçelerden biri; merkezde apartman, köylerde müstakil ev yapımı sürüyor.",
         "Afşin'in iklimi Elbistan'a benziyor: kış soğuk ve uzun. Şapı bahar, yaz ve sonbahar başında yoğun yapıyoruz; "
         "kışın ancak kapalı ve ısıtılabilen binalarda çalışıyoruz."],
  dikkat=["Soğuk havada kum ve su da soğuk olur; malzemenin donmuş ya da buzlu olmamasına dikkat ediyoruz.",
          "Rüzgârlı günlerde açık balkon ve terasları naylonla örtüyoruz; şapın yüzeyi hızlı kurursa tozlanır.",
          "Müstakil evlerde garaj ve depo zeminleri için şap kalınlığını gelecek yüke göre seçiyoruz."],
  sss=[("Afşin'de hangi aylarda şap yapıyorsunuz?",
        "Hava uygun olduğu sürece her ay çalışıyoruz. Kış aylarında yalnızca kapalı, camı takılmış binalarda döküm yapıyoruz."),
       ("Afşin'de fiyat merkezle aynı mı?",
        "Metrekare fiyat aralığımız bütün ilçelerde aynı. Kesin rakamı metrekare ve iş koşullarını öğrenince veriyoruz.")]),
 dict(ad="Göksun", de="Göksun'da", slug="goksun-sapci", tip="yayla", komsu=["afsin-sapci", "andirin-sapci", "elbistan-sapci"],
  giris=["Göksun, Kahramanmaraş'ın yayla ilçelerinden biri; kış erken gelir, kar uzun süre kalır. Şap sezonu burada "
         "merkeze göre daha kısa, bu yüzden yaz aylarında işler sıkışıyor.",
         "Göksun'da yazlık ev, yayla evi ve köy evi işleri çok. Bu tip işlerde şapın kuruma süresini sezonun bitişine göre "
         "planlıyoruz; üst kaplama da kış gelmeden bitebilsin."],
  dikkat=["Sonbaharın son haftalarına kalan işlerde gece sıcaklığını takip ediyoruz; risk varsa işi erteliyoruz.",
          "Yayla evlerinde şaptan önce zemin yalıtımı konuşulmalı; soğuk zemin hem enerjiyi hem kaplamayı etkiler.",
          "Yaz sezonu kısa olduğu için iş gününü erken ayırmanızı öneriyoruz."],
  sss=[("Göksun'da sezon ne zaman başlıyor?",
        "Don riski kalktıktan sonra başlıyor ve sonbaharda gece donları başlayana kadar sürüyor. Kesin tarih yıla göre değişiyor."),
       ("Yayla evine şap atıyor musunuz?",
        "Evet. Yol durumunu ve evin konumunu yazın; pompa ve hortumun ulaşıp ulaşamayacağını önceden konuşalım.")]),
 dict(ad="Andırın", de="Andırın'da", slug="andirin-sapci", tip="dag", komsu=["goksun-sapci", "onikisubat-sapci", "caglayancerit-sapci"],
  giris=["Andırın, ormanlık ve dağlık bir ilçe; köyleri yamaçlara dağılmış. Yolu dar ya da eğimli olan köylerde şap işi "
         "makinenin nereye kadar yaklaşabileceğine göre planlanıyor.",
         "Pompayı yola en yakın noktaya kuruyoruz, hortumu evin içine kadar uzatıyoruz. Hortumun ulaşmadığı nadir durumlarda "
         "bunu iş gününden önce söylüyoruz."],
  dikkat=["Köy yolunun genişliğini ve son kısımda araç girip girmediğini önceden sorun; kum ve pompa aracı oraya gelecek.",
          "Yağışlı günlerde açık alanda şap dökülmez; çatısı ve doğraması bitmiş binada çalışıyoruz.",
          "Rutubetli bölgelerde şapın kuruması uzar; üst kaplamadan önce nemin düşmesini bekleyin."],
  sss=[("Dar yollu köylere geliyor musunuz?",
        "Geliyoruz. Aracın yaklaşabileceği son noktayı ve oradan eve mesafeyi yazın; hortumla ulaşılıyor mu birlikte bakalım."),
       ("Rutubetli evde şap ne kadar sürede kurur?",
        "Kalınlığa ve havalandırmaya göre değişir. Üstüne parke gibi neme hassas kaplama yapılacaksa ölçerek karar verilmelidir.")]),
 dict(ad="Türkoğlu", de="Türkoğlu'nda", slug="turkoglu-sapci", tip="ova", komsu=["onikisubat-sapci", "dulkadiroglu-sapci", "pazarcik-sapci"],
  giris=["Türkoğlu, Kahramanmaraş merkezinin güneyinde, Gaziantep yolu üzerinde. Merkeze yakın olduğu için burada konut "
         "işlerinin yanında depo, atölye ve iş yeri zeminleri de sık çıkıyor.",
         "İş yeri zeminlerinde düzgünlük kadar dayanım da önemli. Forklift ya da ağır raf gelecek zeminlerde şap tek başına "
         "yetmeyebilir; bunu baştan söylüyor, gerekiyorsa beton zemin önerisi yapıyoruz."],
  dikkat=["Ağır yük gelecek zeminde şap kalınlığını ve dayanım beklentisini önceden konuşuyoruz.",
          "Geniş alanlarda derz (genleşme boşluğu) planlanmazsa şap kendi çizgisini çatlak olarak açar.",
          "Ova sıcağında ilk 3 gün sulama ve gölgeleme çatlak riskini düşürür."],
  sss=[("Depo ve atölye zeminine şap atıyor musunuz?",
        "Atıyoruz. Zemine ne tür yük geleceğini yazın; şapın uygun olup olmadığını ve kalınlığı buna göre söyleyelim."),
       ("Türkoğlu köylerine de geliyor musunuz?",
        "Türkoğlu merkezine ve köylerine geliyoruz. Mahalle ya da köy adını yazmanız yeterli.")]),
 dict(ad="Çağlayancerit", de="Çağlayancerit'te", slug="caglayancerit-sapci", tip="dag", komsu=["pazarcik-sapci", "andirin-sapci", "nurhak-sapci"],
  giris=["Çağlayancerit, il merkezinin doğusunda dağlık bir ilçe. Mahalle sayısı az ama dağınık; işlerin çoğu müstakil "
         "ev, köy evi ve tek katlı yapı.",
         "Küçük metrajlı işlerde de makineyle çalışıyoruz. Metrekare az olsa bile kalınlık ve düzgünlük aynı kurala göre yapılıyor."],
  dikkat=["Küçük işlerde pompanın kurulum süresi metrekareye göre büyük yer tutar; bunu teklifte açıkça söylüyoruz.",
          "Eğimli arsalarda ön ve arka cephe arasında kot farkı olur; kapı eşiklerini önceden belirleyin.",
          "Kış aylarında yüksek kesimlerde don riski vardır; döküm günü havaya göre seçilir."],
  sss=[("Küçük metrajlı işe geliyor musunuz?",
        "Geliyoruz. Çok küçük işlerde fiyat metrekare yerine iş bazında konuşulabilir; bunu baştan söylüyoruz."),
       ("Çağlayancerit'te hangi mahallelere gidiyorsunuz?",
        "Aşağıdaki listedeki bütün mahallelere gidiyoruz.")]),
 dict(ad="Ekinözü", de="Ekinözü'nde", slug="ekinozu-sapci", tip="yayla", komsu=["elbistan-sapci", "afsin-sapci", "nurhak-sapci"],
  giris=["Ekinözü, Elbistan'ın komşusu, küçük ve yüksek bir ilçe. Burada işler çoğunlukla müstakil ev ve köy evi; "
         "kışlar Elbistan gibi sert geçiyor.",
         "Ekinözü işlerini Elbistan ve Afşin işleriyle aynı takvimde planlıyoruz. Bu sayede uzak bir ilçe için ayrı bir gün "
         "beklemeniz gerekmiyor; iş gününüzü önceden ayırmanız yeterli."],
  dikkat=["Don riskli günlerde şap dökülmez; yazın ve sonbahar başında takvim daha uygun.",
          "Müstakil evlerde zemin yalıtımı şaptan önce bitmiş olmalı.",
          "Isıtma sistemi şap kuruduktan sonra kademeli açılmalı."],
  sss=[("Ekinözü'ne ne zaman gelebilirsiniz?",
        "Bölgedeki diğer işlerle aynı haftaya planlıyoruz. Metrekare ve adresi yazın, size uygun günü söyleyelim."),
       ("Ekinözü'nde fiyat farklı mı?",
        "Metrekare fiyat aralığımız aynı. Kesin rakamı iş koşullarını öğrendikten sonra veriyoruz.")]),
 dict(ad="Nurhak", de="Nurhak'ta", slug="nurhak-sapci", tip="dag", komsu=["elbistan-sapci", "ekinozu-sapci", "caglayancerit-sapci"],
  giris=["Nurhak, Malatya sınırındaki dağlık ve yüksek bir ilçe; mahalle sayısı az. Burada şap işleri çoğunlukla yeni "
         "yapılan ya da yenilenen müstakil evlerde çıkıyor.",
         "Yüksek ve soğuk bir bölge olduğu için şap sezonu kısa. İşleri Elbistan tarafındaki işlerle birlikte planlıyoruz."],
  dikkat=["Kış koşullarında yola ve hava durumuna göre iş günü değişebilir; bunu önceden haber veriyoruz.",
          "Don riski olan dönemde açık binaya şap dökmüyoruz.",
          "Kuruma süresi soğukta uzar; üst kaplama için acele etmeyin."],
  sss=[("Nurhak'a geliyor musunuz?",
        "Geliyoruz. Mahalle adını ve yaklaşık metrekareyi yazın, gün planlayalım."),
       ("Soğukta kuruma ne kadar uzar?",
        "Sıcaklık düştükçe kuruma yavaşlar. Üst kaplama öncesinde zeminin gerçekten kuruduğundan emin olunmalı.")]),
]

# veri dosyasındaki yazım hataları
DUZELT = {"Akif Inan": "Akif İnan", "Akcakoyunlu": "Akçakoyunlu"}
