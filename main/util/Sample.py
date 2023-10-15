from . import StreetViewSamplerConstants as constants
import requests

class Sample:
    """Class abstracting a sample
    """
    def __init__(self, pano_id:str, coordinates:list, prompt:str) -> None:
        """
        Args:
            pano_id (str): panorama id of this sample
            coordinates (list): coordinates of sample, 0 for lat, 1 for lon
            prompt (str): prompt that generated this sample
        """
        self.pano_id = pano_id
        self.coordinates = coordinates
        self.prompt = prompt
        
    def get_street_view_image(self, image_size:str, api_key:str, heading:int=90) -> bytes:
        """Returns street view image of this sample

        Args:
            image_size (str): size of each image that assembles the panorama, in format {int}x{int}
            api_key (str): your api key
            heading (int, optional): heading of image. Defaults to 90.

        Raises:
            Exception: raised when responded with error status code

        Returns:
            bytes: image content in bytes
        """
        url = f'https://maps.googleapis.com/maps/api/streetview?size={image_size}&heading={heading}&pano={self.pano_id}&key={api_key}&return_error_code=true'
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(response.reason)
        
    def get_panorama(self, image_size:str, api_key:str) -> list:
        """Returns panorama of this sample

        Args:
            image_size (str): size of each image  that assembles the panorama, in format {int}x{int}
            api_key (str): your api key

        Returns:
            list: list of bytes of images
        """
        image_data = []
        for heading in constants.DEFAULT_HEADINGS:
            content = None
            try:
                content = self.get_street_view_image(image_size, api_key, heading=heading)
            except Exception as e:
                print(f'Error {e} occurred while getting panorama id {self.pano_id} at heading {heading}')
            if content != None:
                image_data.append(content)
        return image_data
        
    def to_json(obj:'Sample') -> dict:
        """JSON encoder for Sample

        Args:
            obj (Sample):

        Returns:
            dict: encoded dictionary object
        """
        return {
            "pano_id": obj.pano_id,
            "coordinates": obj.coordinates,
            "prompt": obj.prompt
        }
        
    @classmethod
    def from_json(cls, json_data:dict) -> 'Sample':
        """load from json data

        Args:
            json_data (dict):

        Returns:
            Sample
        """
        return cls(json_data['pano_id'], json_data['coordinates'], json_data['prompt'])
    
    def __eq__(self, __value: object) -> bool:
        return self.coordinates == __value.coordinates and self.pano_id == __value.pano_id
    
    def __hash__(self) -> int:
        return hash((self.coordinates[0], self.coordinates[1]))