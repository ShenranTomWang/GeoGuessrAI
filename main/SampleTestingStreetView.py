import os
from util.StreetViewSampler import StreetViewSampler
import util.StreetViewSamplerConstants as constants
import util.DirUtil as DirUtil

sampler = None
sample_size = 200

if os.path.exists(f'{DirUtil.get_testing_image_dir()}/metadata.json'):
    sampler = StreetViewSampler.from_json(DirUtil.get_testing_image_dir(), sample_size, constants.API_KEY)
else:
    sampler = StreetViewSampler(sample_size, constants.API_KEY, prompts=constants.TESTINGSET_PROMPTS)
    
sampler.sample(size_per_prompt=10)
sampler.download_panoramas(DirUtil.get_testing_image_dir())
sampler.save_sampler_status_metadata(DirUtil.get_testing_image_dir())
sampler.draw_samples()