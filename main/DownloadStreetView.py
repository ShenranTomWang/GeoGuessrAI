from util.StreetViewDownloader import StreetViewDownloader

downloader = StreetViewDownloader(dataset_size=1)
downloader.generate_coordinates()
downloader.get_pano_ids_from_coordinates()
downloader.download_random_street_view_images()