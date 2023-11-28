import uuid
from util.db import run_query
from model.models import Category, ShippingOption, Banner, Product, ProductImage, User
from sqlalchemy import insert, select

def populate_data():
    insert_category_product()
    insert_shipping_option()
    insert_admin()
    insert_banner()

def check_if_category_exists(Table) -> bool:
    data = run_query(select(Table))
    return True if data else False

def insert_category_product():

    if check_if_category_exists(Category):
        return

    categories_id = []
    for idx in range(11):
        categories_id.append(uuid.uuid4())
        
    categories = [
        {
            "id": categories_id[0],
            "category_name": "Tshirt top",
        },
        {
            "id": categories_id[1],
            "category_name": "Trouser",
        },
        {
            "id": categories_id[2],
            "category_name": "Pullover",
        },
        {
            "id": categories_id[3],
            "category_name": "Dress",
        },
        {
            "id": categories_id[4],
            "category_name": "Coat",
        },
        {
            "id": categories_id[5],
            "category_name": "Sandal",
        },
        {
            "id": categories_id[6],
            "category_name": "Shirt",
        },
        {
            "id": categories_id[7],
            "category_name": "Sneaker",
        },
        {
            "id": categories_id[8],
            "category_name": "Bag",
        },
        {
            "id": categories_id[9],
            "category_name": "Ankle Boot",
        },
    ]

    run_query(insert(Category).values(categories), commit=True)
    
    product_id = []
    for idx in range(30):
        product_id.append(uuid.uuid4())
    
    product_data = [
        {
            "id": product_id[0],
            "category_id": categories_id[0],
            "product_name": "KAOS CROP TOP OVERSIZE WANITA LGN PENDEK",
            "description": "SPESIFIKASI : - Bahan 100% cotton 20s combed soft - Sablon plastisol dry process - Benang jahit full cotton - oversized crop top fit   KUALITAS PRODUK : - Bahan nyaman dipakai, tebal dan adem - Sablonan halus dan rapih - Tersedia ukuran S - M - L - XL - Jahitan rapih standard produk department store.   UKURAN BAJU (LEBAR x PANJANG) DALAM Cm : - SMALL 50 x 44 cm - MEDIUM 52 x 46 cm - LARGE 54 x 48 cm - XTRA LARGE 56 x 50 cm",
            "condition": "used",
            "price": 50000
        },
        {
            "id": product_id[1],
            "category_id": categories_id[0],
            "product_name": "Crop Top Wanita - Alternative Culture CROP - Hitam",
            "description": "Ukuran: CROP TOP ALLSIZE - Lingkar dada: 86 cm - Panjang: 40 cm - Bahan : Cotton Combed 30s  CROP TOP OVERSIZE - Lingkar dada: 96 cm - Panjang: 47 cm - Bahan : Cotton Combed 30s",
            "condition": "new",
            "price": 32000
        },
        {
            "id": product_id[2],
            "category_id": categories_id[0],
            "product_name": "JINISO Crop Top Oversize Tee Basic T-Shirt",
            "description": "Wajib punya, must have item buat ootd dan bergerak seharian! Crop Top Basic Oversize Tee dari JINISO dengan bahan real cotton combed yang adem, nyaman, dan tentunya bebas bergerak! Kaos Crop Top oversized JINISO lebih longgar & lebih besar (Tidak Ketat) ",
            "condition": "used",
            "price": 40000
        },
        {
            "id": product_id[3],
            "category_id": categories_id[1],
            "product_name": "Matisse Pants | Cullote Loose Pants - Trousers Pants - Celana Panjang",
            "description": "Material: Polyester Premium Detail ukuran: Lingkar pinggang 60-74cm Lingkar pinggul 128cm Lingkar paha 82cm Panjang 100cm Pisak 36cm Lebar kaki 24cm",
            "condition": "used",
            "price": 85000
        },
        {
            "id": product_id[4],
            "category_id": categories_id[1],
            "product_name": "Celana Bahan formal Kerja pria Slim fit abu medium pants trouser",
            "description": "Deskripsi : - Celana panjang bahan formal slim fit, - bahan ini dapat sedikit melar, sehingga menambah kenyamanan ketika di pakai sehari- hari., - Warna : Medium Grey /abu abu muda (bahan TIDAK MENGKILAT), - bahan : Semi Wool, - cutting : Slim Fit, - Kancing dan Resleting depan, - 2 Kantong belakang celana, - Packaging : Bubble wrap & plastic bag packaging",
            "condition": "new",
            "price": 175000
        },
        {
            "id": product_id[5],
            "category_id": categories_id[1],
            "product_name": "Celana Bahan Formal Kantor Panjang Pria SLIMFIT Big Size Hitam Trouser",
            "description": "Materials : - Premium Semi Wool, - Tekstur bahan Tebal, Adem, Lentur & Anti Kusut, - Resleting YKK Original, lebih awet dan tidak gampang dol, - Tidak panas walaupun cuaca ekstrim, - Tidak mudah kusut, - Jahitan Rapi, - Nyaman di pakai, - Full paping, jahitan kuat, - Tidak mudah berbulu",
            "condition": "new",
            "price": 162000
        },
        {
            "id": product_id[6],
            "category_id": categories_id[2],
            "product_name": "Screamous Sweater Pullover Hoodie DUMONT - FOREST GREEN",
            "description": "Bahan : 100% Cotton Fleece (Ketebalan Medium, handfeel lembut, dengan detail Grafis Embroidery bertekstur halus,  memiliki drawcord untuk mengatur hooded, terdapat saku pada bagian depan dan nyaman digunakan untuk sehari-hari).",
            "condition": "used",
            "price": 105000
        },
        {
            "id": product_id[7],
            "category_id": categories_id[2],
            "product_name": "Okechuku FIDEL Crewneck Polos Pullover Sweater Oversize Switer Sweter",
            "description": "Sweater polos OVERSIZE model terbaru dari Okechuku, model polos, simple, basic, tapi tetap fashion, badan bawah dan ujung tangan dilengkapi dengan rib karet. Terbuat dari bahan BABY TERRY yang halus dan lembut, nyaman dipakai. Cocok untuk keseharian kamu guys. Pola/pattern dibuat unisex sehingga bisa dipakai pria maupun wanita.",
            "condition": "new",
            "price": 55000
        },
        {
            "id": product_id[8],
            "category_id": categories_id[2],
            "product_name": "Nautica Crewneck Pullover Original Sweater Sweatshirt Long Sleeve",
            "description": "Kelengkapan : Crewneck + Full Tag, Kondisi : New Original 100%, Made in Bangladesh, , Size Chart Basic :, S : Lebar 57 cm x Panjang 68 cm, M : Lebar 59 cm x Panjang 70 cm, L : Lebar 62 cm x Panjang 72 cm",
            "condition": "used",
            "price": 130000
        },
        {
            "id": product_id[9],
            "category_id": categories_id[3],
            "product_name": "Alena Dress - Premium HK Linen Dress Big Size Fashion Terbaru",
            "description": "Bahan utama: Katun + Linen (Tipis/Summer)  Tema: Retro  Size(cm): XL ld 102 panjang 112 Jenis Baju: Dress Usia cocok: 30-50 Tahun",
            "condition": "used",
            "price": 200000
        },
        {
            "id": product_id[10],
            "category_id": categories_id[3],
            "product_name": "vSamantha - Home Dress Polos Kancing Sachie",
            "description": "Detail Ukuran :  Lingkar dada : 120cm (Kurang lebih) Lingkar lengan : 40 cm (Kurang lebih) Panjang baju : 105cm (Kurang lebih) Berat : 210 gram Bahan : Rayon Fit to xxl ( Busui friendy )",
            "condition": "used",
            "price": 50000
        },
        {
            "id": product_id[11],
            "category_id": categories_id[3],
            "product_name": "HANNAH MIDI DRESS MINT",
            "description": "Midi dress dilengkapi detail cantik yang melalui proses PLEATS pada bagian dada. Dengan proses chemical pleats sehingga detail aksen akan tahan lama dan tidak akan hilang setelah di cuci. Terdapat kancing pada bagian depan sehingga busui friendly. Dilengkapi kantong kanan dan kiri serta kancing pada lengan yang wudhu friendly.",
            "condition": "used",
            "price": 210000
        },
        {
            "id": product_id[12],
            "category_id": categories_id[4],
            "product_name": "POCKET LONG COAT BLAZER KOREA/CARDIGAN WANITA SCUBA PREMIUM/NIKITA",
            "description": "Gaes kami keluarin model long coat ala2 korea gitu.Mewah bgt dipakenya, buat ngantor,ootd,jalan2 bahan scuba super adem dan lembut DIJAMIN BAGOESS!!!ADA HARGA ADA KUALITAS!!",
            "condition": "new",
            "price": 100000
        },
        {
            "id": product_id[13],
            "category_id": categories_id[4],
            "product_name": "jaket long coat pria/jaket musim dingin/jaket tebal/jaket winter pria",
            "description": "- Bahan Utama GN Premium  - Karakter Bahan Yang digunakan Lembut dan Nyaman dipakai  - Resleting Anti air  - Bahan dalam Satin dilapisi Dakron 0,6 mm  -Nyaman dipakai Saat Suhu Dingin maupun Saat Berkendara  - Varian Ukuran : S M L XL XXL",
            "condition": "used",
            "price": 300000
        },
        {
            "id": product_id[14],
            "category_id": categories_id[4],
            "product_name": "jaket long coat pria/jaket musim semi outerwear pria",
            "description": "BAHAN n AKSESORIS - Bahan luar : American drill - bahan lapisan : katun motif kotak - model penutup : kancing - memiliki 3 kantong 2 kantong luar 1 kntong dalam di dada sebelah kiri",
            "condition": "used",
            "price": 165000
        },
        {
            "id": product_id[15],
            "category_id": categories_id[5],
            "product_name": "Sandal Slides Rumah Hotel Sendal Karet Motif Lucu Empuk Anti Slip",
            "description": "Sandal dengan design bebek lucu ini dapat dipakai oleh pria dan wanita sesuai pilihan warna dan size. Cocok dipakai di outdoor maupun indoor karena design yang yang simple dan bahannya yang nyaman. Cocok juga dipakai dapur dan toilet karena bahannya yang mudah dicuci dan super anti licin , cocok banget untuk sekeuarga.",
            "condition": "new",
            "price": 30000
        },
        {
            "id": product_id[16],
            "category_id": categories_id[5],
            "product_name": "Sandal Jepit Sandal Pria Sandal Flip Flop CAMOU",
            "description": "Artikel : WR Warna : Sol biru navy & tali coklat karamel Category: FlipFlops Bahan: Full Karet  Ukuran tersedia: 39-44",
            "condition": "new",
            "price": 85000
        },
        {
            "id": product_id[17],
            "category_id": categories_id[5],
            "product_name": "SATUAN Sandal Jepit / Sendal Jepit Sun Swallow Evolve",
            "description": "Sun Swallow Evolve merupakan kreasi terbaru dari Sun Swallow. Dengan warna warna yang trendy, membuat Anda tampak keren.",
            "condition": "used",
            "price": 15000
        },
        {
            "id": product_id[18],
            "category_id": categories_id[6],
            "product_name": "VENGOZ Kemeja Pria",
            "description": "Kualitas bahan dan kerapihan jahitan setara dengan brand2 dept store Kami menggunakan vendor konveksi yang sudah berpengalaman di brand2 international  Kemeja Pria VENGOZ Kode : KMSS111 Size Yang Tersedia Sesuai Variasi  - Cotton Viscose - Original 100% - Model Slim Fit - Size Lokal - Nyaman Dipakai  size Lebar dada x panjang M = 51x70 cm L = 53x73 cm XL = 56x75 cm",
            "condition": "new",
            "price": 130000
        },
        {
            "id": product_id[19],
            "category_id": categories_id[6],
            "product_name": "Baju Kemeja Pria Hawai Pantai Size Jumbo Terbaru / Kemeja Cowok Bali",
            "description": "Jika anda sedang mencari Kemeja Hawai yang cocok untuk Pria maupun Wanita berarti anda sangat tepat melihat produk ini.  Kemeja Hawai ini sangat cocok untuk menemani aktifitas anda mulai hangout, mantai, nongkrong, ngopi, bersantai, jalan-jalan ataupun kegiatan sehari-hari lainya.  Kemeja ini dibuat dari Bahan Rayon Premium yang memiliki keunggulan:  - Halus - Lembut - Ringan (tekstur bahan tidak tebal & tidak tipis) - Loose wear (dipakainya jatuh di badan) - Tidak Panas - Sangat menyerap keringat.",
            "condition": "used",
            "price": 110000
        },
        {
            "id": product_id[20],
            "category_id": categories_id[6],
            "product_name": "Kemeja Pria Lengan Pendek Cowok Motif Surfing Baju Pantai Hawai Bunga",
            "description": "ESTIMASI SIZE : TOLERANSI / MUNGKIN ADA SEDIKIT PERBEDAAN UKURAN SEKITAR 1-2 CM !!!  - Model REGULAR - UKURAN NORMAL DAN BESAR BUKAN UKURAN KECIL SEPERTI YG BEREDAR DI PASARAN. - UKURAN XL YG BEREDAR SETARA UKURAN M DI TOKO KAMI. - HARGA MURAH KARENA PRODUKSI SENDIRI (KONFEKSI) - KUALITAS DI JAMIN PREMIUM 100% - Bahan : 100% Kain Baloteli LICIN ADEM | Woolpech (bahan tebal, Adem, Halus, berserat seperti canvas) - Cuttingan Lengan Tidak Gombrong - BAHAN ADEM, TEBAL, TIDAK SEPERTI BAHAN MURAH YA KAK, TIDAK KASAR - Model Pakai Size L - Tinggi & Berat Model : 170 cm & 70 kg - Dapat dipakai untuk tampilan casual ataupun formal - Kualitas jahitan rapi dan kokoh.",
            "condition": "new",
            "price": 35000
        },
        {
            "id": product_id[21],
            "category_id": categories_id[7],
            "product_name": "Sepatu Sneakers Macbeth Vegan Grey List Black1:1 Original Quality",
            "description": "Product : BNIB (Brand New In Box) Type : Macbeth Vegan Grey List Black Kualitas : 1:1 Original Quality Bahan : Suede, Canvas, Rubber Sole kelengkapan dan Bonus : 1. Box 2. Sticker 3. Kaos Kaki 4. Tot Bag",
            "condition": "new",
            "price": 230000
        },
        {
            "id": product_id[22],
            "category_id": categories_id[7],
            "product_name": "Declan Sneaker Sport Rovic",
            "description": "Declan Sneaker Sport Rovic 01-028 adalah sepatu sneakers modern pria dengan variasi bahan dan warna monochrome yang stylish dan modern. Dengan detail material, warna senada dan design sol yang sangat baik, bahan mesh yang dipadukan dengan detail karet senada yang berkesan elegan. Material insole kualitas terbaik yang super empuk sehingga nyaman waktu digunakan. ",
            "condition": "new",
            "price": 210000
        },
        {
            "id": product_id[23],
            "category_id": categories_id[7],
            "product_name": "Sepatu Pria Wanita Sneakers Import Outxide Korean Style Breatheable",
            "description": "KEUNGGULAN PRODUK KAMI : Cocok untuk pria dan wanita. Dijamin nyaman dipakai. Awet dan tahan lama. Menggunakan material pilihan terbaik.  MATERIAL YANG DIGUNAKAN : Upper : Kain kanvas dengan ketebalan 12os. Foxyng : Karet ukuran 30 dengan ketebalan 2,5ml. Sol : Karet (Anti licin dan tahan lama).",
            "condition": "used",
            "price": 50000
        },
        {
            "id": product_id[24],
            "category_id": categories_id[8],
            "product_name": "Tas Selempang Pria Cordura Waistbag Pria Slingbag Pria Tas Pria Simple",
            "description": "Sebuah tas messenger (juga disebut tas kurir) adalah jenis tas, biasanya terbuat dari beberapa jenis kain (sintetik alami atau), yang dikenakan di atas satu bahu dengan tali yang melintasi dada dan menyambung kembali dengan tas di bawah. Tas messenger biasanya digunakan oleh kurir, tas messenger sekarang juga merupakan ikon fashion perkotaan. Beberapa jenis tas messenger disebut carryalls. Sebuah versi yang lebih kecil sering disebut tas sling.",
            "condition": "new",
            "price": 20000
        },
        {
            "id": product_id[25],
            "category_id": categories_id[8],
            "product_name": "HANA Eloise Sling Tweed Bag M3004-C",
            "description": "Bahan : Kulit Sintetis dan Tweed dengan kualitas 100% IMPORT. Dimensi (P x L x T cm) = 22 cm x 11 cm x 20 cm *Toleransi ukuran 1-3 cm dikarenakan pengukuran dilakukan secara manual. *Warna pada gambar dapat sedikit berbeda dengan warna asli akibat pencahayaan saat proses photoshoot",
            "condition": "new",
            "price": 310000
        },
        {
            "id": product_id[26],
            "category_id": categories_id[8],
            "product_name": "Techdoo Tas Selempang Pria Keren Multifungsi USB Charge Fashion",
            "description": "Bisa dijadiin Ransel dan Selempang Fungsi : Tas Anti Air & Anti Maling Model : Waist Bag Casual Pembukaan : Ritsleting  Bahan : Nilon Ukuran : 18cm x 11cm x 31cm Warna : Hitam, Abu, Biru & Gold  Tas Pria Tas Selempang Multifungsi Waistbag Fashion Premium Quality Crossbody Bags Men - Tas Selempang 100% Import High Quality  Tas Model selempang versi Crossbody Sling Bags adalah tas exclusive khusus traveler dengan model selempang agar nyaman dalam berpergian tanpa harus takut oleh kemungkinan pencurian dan ketika hujan. ",
            "condition": "used",
            "price": 50000
        },
        {
            "id": product_id[27],
            "category_id": categories_id[9],
            "product_name": "Ankle Boot wanita, waterproof boot stylish woman 20 cm Nordic shape",
            "description": "Sepatu ini bisa dipakai untuk tenaga medis yang ingin tampil stylish tapi tetap terlindungi, menemani pergi berbelanja, bekerja di rumah makan,perkebunan,dan sangat cocok untuk menerjang hujan.",
            "condition": "new",
            "price": 250000
        },
        {
            "id": product_id[28],
            "category_id": categories_id[9],
            "product_name": "Sepatu Wanita Hak Tinggi Ankle Boots Fashion Import",
            "description": "Tinggi Hak 8.5 cm * Berat 800 gram",
            "condition": "new",
            "price": 300000
        },
        {
            "id": product_id[29],
            "category_id": categories_id[9],
            "product_name": "DR OSHA SAFETY SHOE COBRA ANKLE BOOT S2 9269 COMP TOE",
            "description": "Heavy Duty Boot Dengan bahan yang sangat kuat dan anti jamur, dengan Baja Toe Cap dengan Kekuatan 200 J & 15.000N yang dapat melindungi kaki anda dengan sempurna, Sepatu Safety ini juga dilengkapi dengan anti dust dan juga Deluxe Padded Collar yang akan membuat Kaki anda tetap nyaman saat pengunaan dalam waktu yang lama.",
            "condition": "used",
            "price": 499000
        }
    ]
    
    run_query(insert(Product).values(product_data), commit=True)
    
    image_data = []
    for idx in range(30):
        data = {
            "id": uuid.uuid4(),
            "product_id": product_id[idx],
            "image": f"/image/product-{idx+1}.jpg"
        }
        image_data.append(data)

    run_query(insert(ProductImage).values(image_data), commit=True)

def insert_shipping_option():

    if check_if_category_exists(ShippingOption):
        return

    shipping_options = [
        {
            "id": uuid.uuid4(),
            "name": "regular",
        },
        {
            "id": uuid.uuid4(),
            "name": "next day",
        }
    ]

    run_query(insert(ShippingOption).values(shipping_options), commit=True)
    
def insert_banner():

    if check_if_category_exists(Banner):
        return

    banner_data = [
        {
            "id": uuid.uuid4(),
            "title": "Fashion Campus- EightWeeks Team",
            "image": "/image/banner-1.jpg"
        },
        {
            "id": uuid.uuid4(),
            "title": "Tampat belanja Fashion Terkece",
            "image": "/image/banner-2.jpg"
        },
        {
            "id": uuid.uuid4(),
            "title": "Penawaran Diskon 50% All Products!!",
            "image": "/image/banner-3.jpg"
        }
    ]

    run_query(insert(Banner).values(banner_data), commit=True)
    
    
def insert_admin():
    if check_if_category_exists(User):
        return
    # Pass : Admin123
    admin_data = {
        "id": uuid.uuid4(),
        "name": "Admin",
        "email": "admin@eightweeks.com",
        "phone_number": "08888888888",
        "password": "e64b78fc3bc91bcbc7dc232ba8ec59e0",
        "type": "seller"
    }
    # Pass : Demo1234
    user_data = {
        "id": uuid.uuid4(),
        "name": "Demo",
        "email": "demo@eightweeks.com",
        "phone_number": "081111111111",
        "password": "fd6138204c4eb1dd19e63896c1557e27",
        "type": "buyer"
    }
    run_query(insert(User).values([admin_data, user_data]), commit=True)
