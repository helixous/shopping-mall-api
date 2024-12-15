from typing import Optional, Dict, Any

from rest_framework.response import Response


def api_response(
        status_code: int,
        message: str,
        data: Optional[Any] = None,
) -> Response:
    """
    API 응답 정형화 함수
    :param status_code: HTTP 상태 코드
    :param message: 응답 메시지
    :param data: 응답 데이터 (Optional)
    :return: Response 객체
    """
    response_body: Dict[str, Any] = {
        "status": status_code,
        "message": message,
        "data": data,
    }

    return Response(
        response_body,
        status=status_code
    )
