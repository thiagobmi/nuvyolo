import requests
from typing import Dict, Any, Optional
from app.utils.logging_utils import setup_logger
from app.config import settings
from app.api.models.camera import CameraInfo
from app.external.nuv_api_wrapper import NuvAPIWrapper


logger = setup_logger("nuv_api")

def initialize_nuv_api():
    # Setting basic environment variables
    NuvAPIWrapper.origin_ip = "192.168.123.30"
    NuvAPIWrapper.origin_username = "nuv"
    NuvAPIWrapper.origin_password = "nuv"
    NuvAPIWrapper.edge_ip = "192.168.123.31"
    NuvAPIWrapper.org_username = "apple"
    NuvAPIWrapper.org_password = "apple"
    NuvAPIWrapper.org_name = "Main"
    NuvAPIWrapper.org_domain = "main.org"
    NuvAPIWrapper.requests_response_times = []
    
    # Initialize API wrapper
    # TODO: Getting camera info without NuvAPIWrapper?
    return NuvAPIWrapper.run_request(method_name="get_manager_token")


def get_camera_info_api(camera_id:int):
    return NuvAPIWrapper.run_request(method_name="get_camera", method_parameters={"camera_id": camera_id})

# def get_camera_info_api(cam_id: int) -> Dict[str, Any]:
#     """
#     Obtém informações da câmera através da API do NUV.
#
#     Args:
#         cam_id: ID da câmera a ser consultada.
#
#     Returns:
#         Dicionário com as informações da câmera ou mensagem de erro.
#     """
#     try:
#         logger.info(f"Consultando informações da câmera {cam_id} via API NUV")
#
#         # Retorno mockado 
#         return {
#             "id": cam_id,
#             "stream_url": f"rtmp://{{domain}}/{cam_id}",
#             "is_active": True
#         }
#
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Erro ao obter informações da câmera {cam_id}: {e}")
#         return {"detail": f"Erro ao consultar a câmera: {str(e)}"}
#     except Exception as e:
#         logger.error(f"Erro inesperado ao consultar a câmera {cam_id}: {e}")
#         return {"detail": f"Erro inesperado: {str(e)}"}

async def get_camera_info(cam_id: int) -> Optional[CameraInfo]:
    """
    Usa a API do NUV para recuperar informações de uma câmera.
    
    Args:
        cam_id: ID da câmera para recuperar informações.
        
    Returns:
        Objeto CameraInfo com detalhes da câmera, se encontrada, None caso contrário.
    """
    # Para desenvolvimento/testes
    # if settings.DEBUG:
    #     return CameraInfo(
    #         camera_id=cam_id, 
    #         url=f"rtmp://localhost/stream/{cam_id}", 
    #         active=True
    #     )
    
    # Integração real com a API
    response = get_camera_info_api(cam_id)
    
    if "detail" in response:
        return None
    
    stream_url = response["stream_url"].replace("{domain}", settings.DOMAIN)
    logger.info(f"URL: {stream_url}")
    
    return CameraInfo(
        camera_id=response["id"],
        url=stream_url,
        active=response["is_active"],
    )









