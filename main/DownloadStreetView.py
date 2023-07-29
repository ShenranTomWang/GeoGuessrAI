from util.StreetViewDownloader import StreetViewDownloader

downloader = StreetViewDownloader(dataset_size=1)
downloader.download_random_street_view_images()