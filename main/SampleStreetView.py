from util.StreetViewSampler import StreetViewSampler
import util.StreetViewSamplerConstants as constants
import util.DirUtil as DirUtil

downloader = StreetViewSampler(1, constants.API_KEY)
downloader.sample_coordinates()
downloader.get_pano_ids_from_coordinates()
downloader.download_panoramas(DirUtil.get_image_dir())
downloader.save_sampler_status_metadata(DirUtil.get_image_dir())