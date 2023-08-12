import os
from util.StreetViewSampler import StreetViewSampler
import util.StreetViewSamplerConstants as constants
import util.DirUtil as DirUtil

sampler = None
sample_size = 100

if os.path.exists(f'{DirUtil.get_image_dir()}/metadata.json'):
    sampler = StreetViewSampler.from_json(DirUtil.get_image_dir(), sample_size, constants.API_KEY)
else:
    sampler = StreetViewSampler(sample_size, constants.API_KEY)
    
sampler.sample(size_per_prompt=10)
sampler.remove_duplicate()
sampler.download_panoramas(DirUtil.get_image_dir())
sampler.save_sampler_status_metadata(DirUtil.get_image_dir())