#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NRB
import cv2
import os
import random
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
dictinoary = {"dento-gingival fibriller":"bağlantı epiteli - Bag dokusu",
              "Alveolo-gingival fibriller":"Alveol kreti - Bağ dokusu",
              "interpapiller Fibriller":"Papil - Papil",
              "Transgingival Fibriller":"Proksimal kök yüzündeki embrasür - Vestibül ve oraql yüzdeki fibriller",
              "Sirküler fibriller":"Serbest diş eti içerisinde seyrederek dişin servikal bölgesini çevreler.",
              "Dento-Periosteal fibriller":"Oral ve vesstibül yüzdeki sement",
              "Transseptal fibrlller":"Epitelyal bağlantının apikalindeki kök yüzeyi - Eptelyal bağlantının apikalindeki kök yüzeyi",
              "Periosto-Gingival fibriller":"Periost - Dişeti",
              "Semisirküller Fibriller":"Dişin mesial yüzü - Dişin distal yüzü",
              "İntegingival fibriller":"Vestibül ve oral yüzlerde diş dizisine paralel uzanır.",
              "çiğneyici mukoza":"Alveol çıkıntınıın bir kısmı\n Sert damak mukozası",
              "Özel mukoza":"dil sırtını örten mukoza",
              "Örtücü mukoza":"oral müköz mebran",
              "periodonsiyum":"dişi çevreleyen ve destekleyen dişeti,sement,periodontal ligament ve alveoler kemikten meydana gelmiş bir doku ünitesidir",
              "peridonsiyumum anlamı":"peri(çevre) , odont(diş) demektir",
              "gingiva":"Ağız boşluğunu döşeyen müköz membranın alveoler kemiği ve dişlerin servikal kısımlarını çevreleyen doku bölümüne dişeti adı verilir.\nGingiva(dişeti) çok katlı yassı epitel ve altındaki bağ dokusundan oluşmaktadır.",
              "dişeti bölümleri":"-Yapışık dişeti(Attached Gingiva\n-Dişeti papilli(İnterdental Gingiva)\n-Serbest dişeti(Free Gingiva)",
              "interdental dişeti":"Alveol kreti ile dişlerin temas noktaları arasındaki ÜÇGEN boşluğu doldurur",
              "mukogingival bağlantı":"Yapışık dişeti ile hareketli alveol mukozası arsındaki sınırdır. Palatinada yoktur.",
              "COL":"iki diş arasında kalan dişeti bölümüdür.",
              "Vaskülarite":"Damarlanma",
              "Pigmentasyon":"Melanin pigmenti",
              "Stippling":"Pürtüklülük",
              "lamina propria":"Dişeti bağdokusu",
              "junctional epitel(ataçman epiteli)":"bağlantı epitelidir.",
              "Staratum basale (Oral gingiva epitel) tabakası":"Oral gingival epitelin en içteki semente yakın ve genç kısmıdır. Mitoz bölünme hızı yüksektir. Oluşan hücreler sırassıyla Stratum spinosum, stratum granulosum, startum corneum adı verilen tabaklaardan ilerlerler (içten dışa). En dışta en yaşlı hücreler bulunur.",
              "bazal tabaka hücrelerinin 2 önemli görevi":"1)Bölünme yoluyla yeni hücreler oluşturup epitelin yenilenmesini sağlarlar.\n2) Bazal laminayı oluşturan maddeyi sağlarlar.",
              "bazal laminanın 2 tabakası":"1.Lamina densa; bağ dokusuna komşudur.\n2. Lamina Lusida; hücreye komşudur.",
              "sulkular cep epiteli":"-Birleşim epitelinin koronal sınırından gingival marjin kretine kadar uzanır.\n-İnce ve genellikle non_keratinize çok katlı yassı epiteldir.\n-Yarı geçirgen bir yapıdadır.",
              "baglantı epitelinin yukarısı ve aşağısındaki hücre sayıları":"koronal kısmında 10-30 hücre kadar bulunurken, servikal bölgesinde 1-2 kadar hücre barındırır.",
              "bağlantı epiteline epitelyal ataşman denmesinin sebebi":"Bağlantı epiteli diş ile dişeti arasındaki bağlantıyısağlar. Bu yüzden bağlantı epiteline epitelyal ataşman denir.",
              "parakeratinize, ortokeratinize ve keratinize":"Epitelin en üstteki tabakada hücreler hücreler çekirdekleriyle gözleniyorlarsa epitel parakeratinize,nukleus ve organel kalıntılarına hücre dışında rastlanıldığında epitel ortokeratinizasyon adını alır. Çekirdekler tamamen kayıp olmuşsa keratinize olarak adlandırılırlar.",
              "desmosom":"iki hücre zarı, iki ataşman plak ve hücre arası yoğun maddeden oluşan hücreler arası bağlantı bölgesidir.",
              "hemidesmosom":"bir hücrenin bir sert dokuya ataşman plakla bağlanmasıdır.",
              "junction":"bağlantı demektir.",
              "Hemidesmosom ve desmosom dışındaki diğer hücre bağlantı tipleri":"1)Sıkı bağlantılar(Tight junctions)\n2) Gevşek bağlantılar(Gap junctions)",
              "epitel hücrelerinde %90 oranda bulunan hücre tipi":"Keratonositler",
              "epitel hücrelerinde %10 oranda bulunan diğer hücre tipleri":"2)Melanositler\n3)Langerhans hücreleri\n4)Non-spesifik hücreler",
              "Keratonositler":"oral gingival epitelde keratin yapımıyla ilgili ve bildirilen tabakalarıı oluşturan epitelyal hücrelere genel olrak keratonosit adı verilmektedir.",
              "melanositler":"bu hücreler dişetinin rengini veren pigmenti yani melainin üretirler.",
              "langerhans hücreleri":"bu hücreler mononükleer fagositioz sistemine dahildirler ve immün reaksiyonlarda lenfositler için antijen tanıtıcı hücreler olarak önemligörevleri vardır.",
              "non-spesifik veya merkel hücreleri":"bu hücreler basal ve supra-basal tabakalarda sinir uçları bölgesinde dağılmışlardır ve impuls iletiminde rol oynadıkları sanılmaktadır.",
              "bağ dokusunu %60 oranında oluşturan yapı":"bağ dokusunu %60 oranda lifler oluşturur. Hücreler %5 ayrıca ara madde ve sinirler %35 lik kısmı oluşturur.",
              "tip I kolagen":"deri,mukoza,kemik,dentin,sement ve bağ dokusunda bulunur.",
              "tip III kollagen":"epitel altındaki perivasküler bölgede bulunur.",
              "tip IV kollagen":"bazal mebranda bulunur.",
              "tip V kollagen":"bazal membranda bulunur.",
              "tip VIII kollagen":"Çapa fibrillerinde bulunur.",
              "diş eti bağdokusunun en öenmli hücresi":"fibroblastılardır. Tüm hücrelerin %65 inin oluştururlar. İğ şeklindedir ve bağ dokusunun devamlılığını sağlayan maddeler salgılar.",
              "bağ dokusundaki mast hücreleri":"-Perivasküler oalrak yerleşirler.\n-Histamin => enflamasyonun erken devresinde enflamasyonu arttırıp azaltır.\n-Heparin => Kemik rezorpsiyon hızını kontrol eder.",
              "hemidesmosom-basal lamina kavramını kim ne zaman ortaya attı ? ":"Lisgtarten ve schroeder(1971) de ortaya attı bu teoriyi ve günümüzde hâlen bu teori geçerlidir.",
              "periodontal ligament":"Fibröz bir bağ dokusu olan periodontal ligament, dişi alveol kemiğine bağlar ve diş kökü ile alveoler kemik arasında kalan periodontal aralığı doldurur. Damarlar, sinirler ve hücreler ihtiva eder.",
              "periodontal ligamentinin 11-26 yaş aralığındaki kalınlığı":"0.21 mm dir.",
              "periodontal ligamentin 56-67 yaş aralığındaki kalınlığı":"0.15 mm dir.",
              "periodontal ligamentin fonksiyonları":"1)Destekleyici\n2)Koruyucu\n3)Yapılandırıcı\n+)Besleyici\n5)Duyum",
              "sharpey fibrilleri":"sharpey fibrilleri, periodontal ligamentin esas fibrilleri sement ve alveoler kemik içine gömüldüklerinde minerilazasyon gösterirler ve sharpey lifleri adını alırlar.",
              "periodontal ligamentin damarları":"kök ucu damarları\nİnteraseptal arterler\nMarginal grup arterler",
              "sement":"sement anatomik diş kökünün üzerini örten ve diş kökünün üzerini örten ve dşi alveol boşluğuna bağlayan periodontal mebran fibirllerinin bağlandığı kalsifiye bir periodonsiyum dokusudr.",
              "mine mi sementi örter yoksa sement mi mineyi örter ? Cevabı":"Vakaların %60-65'inde sement mineyi örter, %30'unda kenar kenara ilişki vardır. Vakaların %5-10'unda ise sement ve mine birleşim yeri açıktadır.",
              "hipersementoz":"Tek dişte veya tüm dişerde meydana gelen kalınlaşmadır.\nGenellikle kökün 1/3 apikal kısmında nödüler bir büyüme\n olarak ortaya çıkar.",
              "sementikel":"periodontal membran içinde serbest bulunan veya kök\nyüzeyine tutunan globiler sement kütlesidir.",
              "sementoma":"Genellikle dişerin apikainde yer alan dişlere tutunan veya serbest halde bulunan sement kitlesidir.",
              "ankiloz":"Periodontal membran ortadan kalkması, sement ile alveol kemiğinin birleşmesidir.",
              "tek cümlede alveoler kemik":"Alveoler kemik, maksiller ve mandibular kemiklerin diş yuvalarını oluşturan ve dişi destekleyen kısmıdır.",
              "Alveoler kemiğin iki bölümü":"1.Alveoler kısım\2.Destek kemik",
              "Alveol kreti ile mine-sement sınırı arasındaki mesafe":"0.75-1.49 mm arasında değişir.",
              "spongiyoz":"Yumuşak kemik",
              "LAMİNA DURANA":"Soketi örten kompakt kemiğin radyografideki görünümüne LAMİNA DURANA denir. Alveoler kemikten,periodontal ligamente kan damarları ve sinirler lamina duradaki WOLKMANN KANALLARI aracılığıyla ulaşırlar.",
              "bundle bone":"Soketin,sharpey fibril demetlerinin girdiği iç kısmı bundle bone(demtesi kemik) adını alır.",
              "Kemiğin içindeki boşlukları dolduran zarın ismi":"endosteum",
              "Fenetrasyon":"Alveol kemiğinde oluşan pencere şeklindeki açıklıktır.",
              "Dehiscence":"Dişlerin kökleri üzerinde yer alan ve marjinal kemiğ de içine alan açıklıklardır.",
              "mikrop ekolojisi":"mikroorganizmaların birbirleri ve çevre ile ilişkisini inceler. Çevre, yaşam yeri olrarak canlıların içinde bulunduklarıfiziksel, kimyasal ve biyolojik özelliklerin toplamıdır.",
              "ekolojik ardıllık":"Organizmaların değişen çevrede birbirleri ardına yerleşmesi olayına ekolojik ardıllık denir. ekolojik ardıllığın en iyi örneği diş biyofilmi oalrak tanımlanan diş plağıdır.",
              "mikroflora":"Mikfroflora ve yaşadığı çevre ile birlikte ekosistem olarak adlandırılır. Ağız boşluğu da bir ekosistemdir.",
              "endojen-yerleşik-normal-kommensal flora":"Normal olarak daima yüksek sayıda bulunan m.o. topluluğudur. Mikrofloralar çok sayıda bakteri az sayıda mayalardan oluşur.",
              "ek(suplementer) flora":"Bunlar da endojendir fakat sayıca azdır. Çevre kendilerine uygun değiştiğinde endojen olabilirler. Diş çürüğü ve periodontal hastalıklar.",
              "Geçici mikroflora":"Ağız boşluğuna yerleşmeyen kısa sürede kaybolan m.o. . Örn., gıdalardan laktik asit bakterileri, unit suyundan psödomanaslar, deri ve barsaktan stafilokoklar: Vücut direnci düştüğünde ağız içinde hastalık yaparlar, fırsatçı enfeksiyonlara neden olurlar.",
              "oksijen basınıcın havada, dil üzerinde, periodontal cepte ve supragingival plakta basıncı":"havada %21, dil üzerinde %12-14, periodontal cepte %1-2, supragingival plakta %1-20.",
              "Redoks(oksidasyon redüksiyon) potansiyeli":"Simgesi Eh'dir. Ortamdaki elektron alma ve verme potansiyelidir. Volt,milivolt olarak ifade edilir.",
              "Eksojen besinler":"Diyetle gelen gıdalar, karbonhidratlar, sukroz.",
              "Endojen besinler":"Esas kaynağı tükrüktür. Tükrük, karbonhidrat, aminoasitleri, peptitleri, proteinleri, dökülen epitel hücreleri içerir.",
              "Proteolitik bakteriler":"azotlu bileşikleri parçalayarak(peptidleri aminoasitlere) kullanır.",
              "retansiyon":"tutunmadır.",
              "glikokaliks":"Bakterilerin çoğu glikokaliks olarak adlandırılan hidrofilik özellikte bir matriksle çevrilidir.",
              "adhezin":"Bakteri yüzeyinde bulunan ve yapışmada rol alan yapılara adhezin denir. \nAdhezinler, fimbriaların üzerinde bulunur.\nBakteri hücresinin yapışacağı reseptörler ligand olarak adlandırılır.",
              "mikroorganizmaların yapışma mekanizmaları":"1- A-Nonspesifik bağlanma\n   Elektrostatik bağlanma\n   Wand der Waals kuvvetleri\n   Hidrofilik bağlar\n2-Spesifik etkileşimler",
              "Diş plak biyofilminin yapısı":"-Biyofilm, heterojendir.\n-Biyofilm interaktif mikroorganizma topluluklarından oluşur.\n-Biyofilm içinde çok sayıda ve çeşitte mikroorganizmaların gen expresyonları bozulur ve tek başına olduklarından\nfarklı bir fenotip kazanırlar.",
              "intersellüler matrix":"Tükrük, dişeti oluğu sıvısı ve bakteriyel ürünlerden oluşan organik ve inorganik maddeler içerir.",
              "dental plak":"İntraoral yüzeylere sıkı balanabilen, başlıca tükrük glikoproteinleri ve extrasellüler polisakkarit matrixi içindeki bakterilerden oluşan sarımsı-gri bir yapıdır. Su spreyi ve gargara ile uzaklaştırılamaz.",
              "Materia alba":"Beyaz peynirimsi birikimdir. Tükrük proteinleri, bazı bakteriler, desquame epitel hücreleri mevcuttur. Organize bir yapı değil, sprey ile kolayca yerd eğiştirir.",
              "1 gr plaktaki yaklaşık bakteri sayısı":"1 gr plak yaklaşık 10^11 bakteri içermektedir.",
              "Periodonsiyumun görevleri nelerdir?":"-Dişi çevresindeki kemiğe bağlamak\n-Çiğneme, konuşma ve yutkunma sırasında oluşan kuvvetleri karşılamak ve eşit olarak dağıtmak.\n-İç ve dış ortamlar arasında bir bariyer oluşturarak vücut yüzeyinin devamlılığını sağlmak\n-Ağız boşluğu içindeki dış ortama ait zararlı etkilere karşı savunma görevi yapmak.\n-Aşınma ve yaşlanma ile meydana gelen değişiklikleri remodelasyon ve rejenerasyon ile telafi etmek.",
              "Yapışık deiş etinin sınırlarını ve öözellikleri yazınız.":"-Mukogingival birleşimden dişeti yivine kadar uzanır.\n-Periost ve alveol kemiğine, dişeti kollagen lifleri ile semente yapışır.\n-Keratinizedir.\n-Hareketsizdir. Dişin stabilitesini sağlar.\n-Anterior kesici bölgede en geniş, posterior mandibular kısımda en azdır.\n-Pürtüklü portakal kabuğuna benzer.",
              "Diş eti nedir anatomik olarak kaça ayrılır sınırlarını yazınız ?":"-Ağız boşluğunu döşeyen mükoz membranın alveolar kemiği ve dişlerin servikal kısımlarını çevreleyen doku bölümüne dişeti denir.\nAnatomik oalrak 3'e ayrılır:\n   -Yapışık dişeti (Attached gingiva) --> Mukogingival birleşimden dişeti yivine kadar uzanır.\n   -Dişeti papilli(interdental gingiva) --> Alveol kret ile dişlerin temas noktaları arasındaki üçgen boşluktur.\n   -Serbest dişeti(Free gingiva) --> Dişlerin servikal bölümlerini saran dişeti kısmı.",
              "Dişetini rengini etkileyen faktörler nelerdir?":"Vaskülarite, pigmentasyon, epitelin keratinizasyonu, epitelin kalınlığı",
              "Dişeti epitelinin bölümleri nelerdir ?":"Oral gingival epitel,sulkular epitel(cep epiteli), junctional epitel(bağlantı epiteli)",
              "Oral epitelin tabakaları nelerdir ?":"Stratum basale(Lamina densa Lusida), stratum spinosum, stratum granulosum, stratum corneom",
              "Epitel hücreler nelerdir açıklayınız.":"Keratonositler:Oral gingival epitelde keratin yapımııyla epitel tabakalarını oluştururlar\nMelanositler: Dişetinin rengini veren pigment olan melanin üretirler.\nLangerhans hücreleri: İmmün reaksiyonlarda lenfositler için antijen tanıtıcı hücrelerdir.\nNon-spesifik hücreler: Sinir uçları bölgesinde dağılmışlardır ve impuls iletiminde rol oynarlar.",
              "Gingival fibriller nelerdir ?":"-Dento-Gingival\n-Alveolo-Gingival\nİnterpapiller\nTransgingival\nSirküler\nDento-periostal\nTransseptal\nPeriosto-gingival\nSemisürküler\nİntergingival",
              "Periodontal ligamentin hücreleri nelerdir ?":"Fibroblastlar\nSemntoblastlar\nSementoklastlar\nOsteoblastlar\nOsteoklastlar\nMakrofajlar, nötrofiller, monositler vemast hücreleri\nEpitelyal kalıntı hücreleri\nNörovasküler elementler(damar ve sinir hücreleri)",
              "Esas fibrillerin seyir yönlerini yazınız.":"Transeptal,alveolar kret,horizontal,oblik,apikal, inter-radiküler",
              "PDL'nin fonksiyonlarını yazıp açıklayınız.":"Destekleyici:Dişi alveol kemiği içinde desktekler.\nKoruyucu: Okluzal kuvvetleri karşılamak ve sement ile alveolar kemik arasındaki fizyolojik ilişkiyi sağlamaktır.\nYapılandırıcı: Peirodontal ligament sement ve kemik için periost görevi görür. Kemik formasyonunu görüldüğü alanlarda osteoblastlar, fibroblastlar, sementoblastlar gözlenir.\nBesleyici: Kan damarları yoluyla kemik ve sementin beslenmesini sağlar\nDuyum: Çeşitli duyuların algılanmasından(ağrı, basınç vb.) nöral elemanları ile işlev görür. ",
              "Sementte oluşan patolojik oalylar nelerdir açıklayınız ?":"Hipersementoz: Tek dişte veya dişlerde meydana gelen kalınlaşmadır\nSementikel: Periodontal membran içinde serbest bulunan veya kök yüzeyine tutunan globüler semen kütlesidir.\nSementoma: Dişlerin apikalinde yer alan, dişlere tutunan veya serbest halde bulunan semen kitlesidir.\nAnkiloz: Periodontal membranın ortadan kalkması, sement ile alveol kemiğin birleşmesidir.",
              "Çiğneyici mukozanın bulunduğu yerler":"Çiğneyici mukoza şuralarda bulunur. Alveol çıkıntının bir kısmı ve sert damak mukozası",
              "Özel mukozanın bulunuğu yerler":"Özel mukoza. Dil sırtını örter.",
              "Örtücü mukozanın bulunduğu yerler":"Örtücü mukoza. Oral müköz mebranda bulunur.",
              "Periodonsiyumda bulunan yapılar":"Dişeti. Sement. Periodontal ligament ve Alveol kemiği",
              "Periodonsiyumun görevleri":"Dişi, çevresindeki kemiğe bağlamak. Çiğneme,konuşma ve yutkunma sırasında oluşan kuvvetleri karşılamak ve eşit olarak dağıtmak. İç ve dış ortamlar arasında bir bariyer oluşturarak vücut yüzeyinin devamlılığını sağlamak. Ağız boşluğu içindeki dış ortama ait zararlı etkilere karşı savunma görevi yapmak. Aşınma ve yaşlanma ile meydana gelen değişiklikleri remodelasyon ve rejenerasyon ile telafi etmek.,",
              "Ağız boşluğunu döşeyen müköz membranın alveoler kemiği ve dişlerin servikal kısımlarını çevreleyen doku bölümüne verilen ad":"Dişeti",
              "Gingivanın içerdiği yapılar":"Gigiva çok katlı yassı epitel ve altındaki bağ dokusundan oluşmaktadır.",
              "Dişetinin anatomik olarak ayrıldığı bölgeler":"Dişeti anatomik olarak üç bölgeye ayrılmaktadır. Yapışık dişeti. Dişeti papili. Serbest dişeti.,",
              "Yapışık dişetinin periost ile bağlandığı yapı":"Alveol kemğidir.",
              "Yapışık dişeti kollagen lifleri ile bağlandığı yapı":"Dişeti kollagen lifleri ile supraalveoler semente yapışır.",
              "Yapışık dişetinin kertinize durumu":"Yapışık dişeti kertinizedir.",
              "Mukogingival birleşimden dişeti yivine kadar olan bölüm":"Yapışık dişetidir.",
              "Yapışık dişetinin sağlık için önemi":"Yapışık dişeti ağız sağlığı için önemlidir.",
              "Yapışık dişetinin en geniş olduğu yer ve en az olduğu yer":"Yapışık dişeti anterior kesici bölgede en geniş oluğ, yaklaşık maxillada 3.5-4.5 milimetre, mandibulada ise 3.3-3.9 milimetredir. En az olduğu bölge ise mandibular posterior bölgedir.",
              "Sağlıklı ve hastalıklı dişeti arasındaki belirgin farklar":"Sağlıklı dişetinde pembe,pütürtüklü bir yapı gösterirken \nhastalıklı dişetinde ise kırmızı,kanlı ve pürtüksüz bir yapı söz konusudur.",
              "İnterdental dişeti":"Alveol kret ile dişlerin temas noktaları arasındaki ÜÇGEN boşluğu doldurur.",
              "İnterdental dişeti kesiciler bölgesinde ve molar bölgesinde nasıl bir yapı gösterir":"Kesiciler bölgesinde SİVRİ;molar bölgesinde KÜT PİRAMİT şeklindedir.",
              "Serbest dişetinin kısaca tanımı":"Dişlerin servikal bölümlerini bir yaka şeklinde saran terminal dişeti kısmına denir.",
              "Serbest dişetinin genişliği":"Genişliği 0.5-2 mm olup periodontal sond ile hafifçe dişten ayrılır.",
              "Dişeti oluğu":"Serbest dişeti ile diş arasında kalan boşluktur.",
              "Mukogingival bağlantı sınırı hakkında bildiklerin":"Yapışık dişeti hareketli alveol mukozası arasındaki sınırdır.",
              "Mukogingival bağlantı palatinada varlık durumu":"Palatinada yoktur.",
              "Alveolar mukoza ve yapışık dişeti'nin renk durumları":"Alveolar mukoza kırmızı iken yapışık dişeti pembedir.",
              "Alveolar mukoza ve yapışık dişeti'nin yüzey özelliği":"Alveolar mukoza pürüzsüz parlak bir görünümde iken yapışık dişeti portakal kabuğu şeklindedir.",
              "Alveolar mukoza ve yapışık dişeti'nin epitel özelliği(keratinize - non-keratinize)":"Alveolar mukoza non_keratinize iken yapışık dişeti keratinize veya parakeratinizedir.",
              "Alveolar mukoza ve yapışık dişeti'nin retepeg durumu":"Alveolar mukoza retepeg değilken yapışıkdişeti retepeg durumdadır.",
              "Alveolar mukoza ve yapışık dişeti'nin bağ dokuus özellikleri":"Alveolar mukoza'nın bağ dokusu gevşek yapıda ve kan damarları fazla iken yapışık dişetinin bağ dokusu sıkı yapıda ve damarlanma orta durumdadır.",
              "COL'un bulunduğu yer":"İki diş rasındaki dişeti dokusudur",
              "Dişetinin fiziksel özellikleri":"Renk\nPapiller kontur\nMarginal kontur\nYüzey yapısı\nBoyut ve kıvamı",
              "Dişetini rengini etkileyen faktörler":"Vaskülarite\nPigmentasyon\nEpitelin keratinizasyonu\nEpitelin kalınlığı",
              "Dişetini en önemli özelliği":"Dişetinin en önemli özelliği matlığı ve pürtüklülük(Stippling) yapısıdır.",
              "Yapışık dişetinin üzerinde bulunan portakal kabuğu görünümünde girinti ve çıkıntıların olayı":"Bunlar, bağ dokusunun epitel içine yaptığı uzantıların yüzeye yansımasıdır.",
              "Dişeti boyutunun ifade ettiği şey":"Dişetinin boyutu tüm hücresel ve hücreler arası elemanlarının ve kanlanmalarının toplam kitlesini ifade eder.",
              "Dişeti kıvamı":"Dişeti sıkı ve serbest dişeti hariç alttaki kemiğe sıkıca tutunduğu için dış etkenlere karşı dirençli bir yapısı vardır.",
              "Serbest dişeti ve yapışık dişetinin vestibüldeki kalınlığı":"Serbest dişetinin vestibüldeki kalınlığı 1.56 mm, yapışık dişeti kalınlığı ise 1.25 mm, ortalama kalınlık bütün alanlar için 1.41 mm olarak bulunmuştur.",
              "Dişeti histolojik oalrak incelendiğinde olutuğu iki tabaka":"Dişeti epiteli ve Lamina propria(Dişeti bağ dokusu)",
              "Dişeti epitelinin meydana getirdiği üç epitel kısım":"1-Oral gingiva epitel\n2-Sulkular epitel(Cep epiteli)\n3-Junctional epitel(Bağlantı epiteli)",
              "Oral epitelin damar içerme durumu":"Damar içermez",
              "Oral epitelin beslenmesini gerçekleştirme şekli":"Beslenmesini bağ dokusu içine uzattığı parmaksı uzantılar(rete-peg) ile diffüzyon veya aktif transport ile yapmaktadır.",
              "Oral gingival epitel tabakaları":"Stratum basale\nStratum spinosum\nStratum granulosum\nStratum corneum\nadı verilen 4 tabakdan oluşur.",
              "Oral gingival epiteldeki bazal tabakanın önemli iki görevi":"1)Bölünme yoluyla yeni hücreler oluşturup epitelin yenilenmesini sağlarlar.\n\n2)Bazal laminayı oluşturan maddeyi salgılarlar.",
              "Bazal lamina 2 tabakadan oluşur. Bunlar":"1-Lamina Densa; bağ dokusunua komşudur.\n2-Lamina Lusida;hücreye komşudur.",
              "Birleşim epitelinin sınırları":"Birleşim epitelin koronal sınırından gingival marjin kretine kadar uzanır.",
              "Sulkular(cep) epitelinin keratinize durumu":"Non-keratinizedir ve cok katlı yassı epiteldir.",
              "Sulkular(cep) epiteli tam geçirgen bir yapıda mıdır":"Yarı geçirgen bir yapıdadır.",
              "Bağlantı epitelinin üst kısımlarındaki hücre sayısı ve en aşağıdaki semente doğru olan kısısmda hücre sayıları":"Üst kısımlarda 10-30 hücre bulunuyorken en alttaki kısımlarda 1-2 hücre bulunuyordur.",
              "Bağlantı epiteinde savunma hücrelerinin geçişine izin verebilmesinin sebebi":"Bağlantı epiteli(junctional) hücreler arası boşluklar \noral gingival epitele oranla daha geniştir. Buda savunma hücrelerinin geçişine izin verir.",
              "Bağlantı epitelinin dişyüzeyine ve bağdokusuna bağlandığı yapılar":"Bağlantı epiteli diş yüzeyine internal bazal lamina ile bağ dokusuna ise Eksteral bazal lamina ile tutunurlar.",
              "Bağlantı epiteline epitelyal ataçman denmesinin sebebi":"Bağlantı epiteli diş ile dişeti arasındaki bağlantıyı sağlar.\nBu yüzden bağlantı epiteline epitelyal ataçaman denir.",
              "Periodontal hastalıklarda bağlantı epitelinin durumu":"Periodontal hastalıklarda bağlantı epiteli apikale doğru göç eder ve periodontal cep oluşur.",
              "Bağ dokusunun en önemli hücresi":"BNağ dokusunun en önemli hücresi %65 lik oranı ile FİBROBLASTLARDIR.\nİğ şeklindedir.\nBağ dokusunun devamlılığını sağlayan maddeler salgılar.",
              "Bağ dokusu hücreleri":"1)Fibroblastlar\n2)Mast hücreleri\n3)Savunma hücreleri\n4)Osteoblastlar ve osteokastlar\n5)Sementoblastlar ve sementoklastlar",
              "Dişeti kan desteğini sağladığı yapılar":"1-Peripst\n2-Alveol kemik\n3-Periodontal ligament",
              "Periodontal ligamentin kısaca tanımı":"Fibröz bağ dokusu olup periodontal ligament, dişi alveol kemiğe bağlar ve diş kökü ile alveolar kemik arasında kalan periodontal aralığı doldurur.\nDamarlar, sinirler ve hücreler ihtiva eder.",
              "Periodontal ligamentin kalınlığının bağlı olduğu etkenler":"Peirodontal ligamentin kalınlığı;\nYaşa,|nDişin sürme aşamasına,|nVe fonksiyonel karakteristiğine\n\ngöre 0.1-0.25 mm arası değişik gösterir.",
              "Periodontal ligamentin fonksiyonları":"1-Destekleici\n2-Koruyucu\n3-Yapılandırıcı\n4-Besleyici\n5-Duyum",
              "Sharpey fibrilleri":"Periodontal ligamnetin esas fibrilleri sement ve alveolar kemik içine göüldüklerinde mineralizasyon gösterirler ve sharpey lifleri adını alırlar.",
              "Periodontal ligamentte damarların bulunduğu yerler":"-Kök ucu damarları\n-İnterseptal arterler\n-Marginal grup arterler",
              }
keys_1 = list(dictinoary.keys())
print("""

Peridontoloji tekrar zekası

1- Uzaktan tekrarlayalım

2- Yüzyüze tekrarlayalım



""")
rakam = 1
spe = int(input("Secim:"))
if spe == 1:
    while True:
        KEY = str(keys_1[random.randint(0, int(len(keys_1) - 1))])
        asd = random.randint(1, 9999)
        kamera_port = 0
        kamera = cv2.VideoCapture(kamera_port)
        time.sleep(0.2)
        return_value, image = kamera.read()
        cv2.imwrite("kameragoruntusu{}.png".format(asd), image)
        del (kamera)
        time.sleep(2)
        fromaddr = "zekaiyapay@gmail.com"
        toaddr = "nrbb@protonmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Evde hareketlilik algıladım"
        body = """{} saat boyunca evde yoktun. Gelen sen misin ?
                                                    Varış saati: {}:{}
                                                    """
        msg.attach(MIMEText(body, 'plain'))
        filename = "kameragoruntusu{}.png".format(asd)
        attachment = open(os.getcwd() + '/kameragoruntusu{}.png'.format(asd), "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "sakizsakiz1")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        print("Email send [+]")
elif spe == 2:
    while True:
        KEY = str(keys_1[random.randint(0, int(len(keys_1) - 1))])
        print("{} nedir ?".format(KEY))
        outasd = input("")
        print(dictinoary[KEY])
        asdasd = input("")
        os.system("cls")
else:
    print("Hatalı işlem")
