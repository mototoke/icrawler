from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
import sys
import os
from pathlib import Path
import argparse
import base64
from icrawler import ImageDownloader
from six.moves.urllib.parse import urlparse


class PrefixNameGoogleDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameGoogleDownloader, self).get_filename(
            task, default_ext)
        return 'google_' + filename


class PrefixNameBingDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameBingDownloader, self).get_filename(
            task, default_ext)
        return 'bing_' + filename


class PrefixNameBaiduDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameBaiduDownloader, self).get_filename(
            task, default_ext)
        return 'baidu_' + filename


def get_args():
    """
    実行時引数の解釈メソッド
    :return: 実行時引数
    """
    # オブジェクト作成
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # 引数設定
    # (必須)
    # 検索キーワード
    parser.add_argument('-k', '--keyword', required=True, help='検索するキーワードを指定します(必須)')

    # 画像ライセンス
    parser.add_argument('-l', '--license',
                        required=True,
                        type=str,
                        choices=['noncommercial', 'commercial', 'noncommercial,modify', 'commercial,modify'],
                        help='ライセンスを指定します(営利、非営利)')

    # (任意)
    # 画像のダウンロード場所
    parser.add_argument('-d', '--dict', default='images', help='ダウンロード画像の配置場所を指定します')

    # 最大ダウンロード数
    parser.add_argument('-m', '--max', type=int, default=100, help='ダウンロードする数を指定します')

    # 任意で基本的に指定しない引数
    # ダウンロード画像の種類
    parser.add_argument('-t', '--type',
                        choices=['photo', 'face', 'clipart', 'linedrawing', 'animated'],
                        help='画像の種類を指定します')

    # ダウンロード画像の色
    parser.add_argument('-c', '--color',
                        choices=['color', 'blackandwhite', 'transparent', 'red', 'orange',
                                'yellow', 'green', 'blue', 'purple', 'pink', 'white',
                                'gray', 'black', 'brown'],
                        help='画像の種類を指定します')

    # 結果を返却
    return parser.parse_args()


def make_folder(args):
    """
    ダウンロードフォルダがない場合に作成します
    :param args:
    :return:
    """
    p = Path(sys.argv[0])
    p_dir = Path(p.parent) / Path(f'{args.dict}')
    if not p_dir.exists():
        os.makedirs(str(p_dir))

    p_keyword = Path(p.parent) / Path(f'{args.dict}') / Path(f'{args.keyword}')
    if not p_keyword.exists():
        os.makedirs(str(p_keyword))

    p_dir_google = Path(p.parent) / Path(f'{args.dict}') / Path(f'{args.keyword}') / Path('google')
    if not p_dir_google.exists():
        os.makedirs(str(p_dir_google))

    p_dir_bing = Path(p.parent) / Path(f'{args.dict}') / Path(f'{args.keyword}') / Path('bing')
    if not p_dir_bing.exists():
        os.makedirs(str(p_dir_bing))

    p_dir_baidu = Path(p.parent) / Path(f'{args.dict}') / Path(f'{args.keyword}') / Path('baidu')
    if not p_dir_baidu.exists():
        os.makedirs(str(p_dir_baidu))


def exe_crawl(arg):
    google_crawler = GoogleImageCrawler(
        downloader_cls=PrefixNameGoogleDownloader,
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=4,
        storage={'root_dir': f'{arg.dict}/{arg.keyword}/google'})
    filters = dict(
        license=f'{arg.license}')
    google_crawler.crawl(keyword=f'{arg.keyword}', filters=filters, offset=0, max_num=arg.max, file_idx_offset=0)

    bing_crawler = BingImageCrawler(
        downloader_cls=PrefixNameBingDownloader,
        downloader_threads=4,
        storage={'root_dir': f'{arg.dict}/{arg.keyword}/bing'})
    bing_crawler.crawl(keyword=f'{arg.keyword}', filters=filters, offset=0, max_num=arg.max)

    baidu_crawler = BaiduImageCrawler(
        downloader_cls=PrefixNameBaiduDownloader,
        storage={'root_dir': f'{arg.dict}/{arg.keyword}/baidu'})
    baidu_crawler.crawl(keyword=f'{arg.keyword}', offset=0, max_num=arg.max)


if __name__ == '__main__':
    args = get_args()

    make_folder(args)

    exe_crawl(args)

