from fastapi import HTTPException

class SpotAttributeNotFound(HTTPException):
    def __init__(self, spot_attribute_id: int):
        super().__init__(
            status_code=404,
            detail=f"Spot attribute with id {spot_attribute_id} not found")
        
    
class SpotAttributeExist(HTTPException):
    def __init__(self, spot_id : int, name : str):
        super().__init__(
            status_code=400,
            detail=f"Spot attribute with spot_id = {spot_id} name = {name} already exists")