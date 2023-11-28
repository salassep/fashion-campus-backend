from io import BytesIO
from flask import Blueprint, send_file, abort
from service.image_service import ImageService
from util.response import response

universal_bp = Blueprint("universal", __name__, url_prefix="")

@universal_bp.route("/", methods=["GET"])
def hello():
    return response(200, msg='Hallo, selamat datang di API Fashion Campus, hubungi kami di cs@eightweeks.com jika tertarik dengan API ini.\nPENDAHULUAN\nPerusahaan fashion ecommerce dengan pangsa pasar "Indonesian Young Urbans" -- pemuda-pemudi dengan rentang umur 15-35 tahun -- berdiri di Indonesia sejak awal tahun 2016 dengan nama Fashion Campus. Perusahaan ini menyajikan katalog brand-brand lokal hingga internasional yang digandrungi anak muda. Oleh karena banyak bekerja sama dengan brand lokal, setelah beroperasi selama satu tahun lebih, mereka berhasil memperoleh cukup banyak return customers dengan pengguna aktif 10.000 per Bulan Juni 2022 dan menerima lebih dari 100.000 pesanan setiap bulannya.\nSejak pandemi menyerang pada tahun 2020, Fashion Campus melihat potensi pada perkembangan belanja digital karena lebih banyak waktu bagi masyarakat dalam mengakses internet. Lisna dan Wira, sebagai salah satu Tim Marketing, diminta untuk melakukan riset pasar. Hasilnya, mereka menemukan bahwa selama pandemi ini juga muncul tren baru di kalangan target market Fashion Campus. Ternyata, "Indonesian Young Urbans" mulai banyak melakukan praktik thrifting atau jual beli pakaian bekas. Dari penemuan ini, Lisna dan Wira mengajukan usulan ke bagian Tim Business Development untuk mengembangkan bisnis model penjualan pakaian bekas yang masih layak pakai.\nPengembangan bisnis model oleh tim Business Development ini nantinya akan dibantu oleh empat tim, yaitu tim Data Science, Tim UI/UX, Tim Artificial Intelligence dan Tim Backend. Lisna dan Wira juga sudah menyampaikan ke tim yang terlibat bahwa waktu pengembangan tidak banyak. Seluruh tim diharapkan dapat mempresentasikan hasil temuannya kepada jajaran petinggi Fashion Campus sesuai dengan timeline yang diberikan.')
        
@universal_bp.route("/image/<name>", methods=["GET"])
def get_image(name):
    try:
        result = ImageService().get_image(name)

        if not result :
            raise Exception()

        return send_file(
            BytesIO(result['blob']),
            mimetype=result['contentType'],
        )

    except:
        abort(404, 'error, Image not found')
