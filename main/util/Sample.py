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