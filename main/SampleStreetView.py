from util.StreetViewSampler import StreetViewSampler
import util.StreetViewSamplerConstants as constants
import util.DirUtil as DirUtil

downloader = StreetViewSampler(100, constants.API_KEY)
downloader.sample_coordinates()
downloader.get_pano_ids_from_coordinates()
downloader.download_street_view_images(DirUtil.get_image_dir())
downloader.save_street_view_metadata(DirUtil.get_image_dir())