import os
import requests


class DartAPI:
    BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(self):
        self.api_key = os.getenv("DART_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "DART_API_KEY가 설정되지 않았습니다. "
                "GitHub Secrets 또는 환경변수를 확인하세요."
            )

    def get_corp_code(self, corp_name: str):
        """
        DART 기업고유번호(corp_code)를 조회합니다.

        참고:
        OpenDART의 기업개황/고유번호 데이터를 이용하기 위해
        corpCode.xml을 다운로드하는 방식으로 처리합니다.
        """

        url = f"{self.BASE_URL}/corpCode.xml"

        response = requests.get(
            url,
            params={"crtfc_key": self.api_key},
            timeout=30,
        )

        response.raise_for_status()

        if response.status_code != 200:
            raise RuntimeError(
                f"DART API 요청 실패: HTTP {response.status_code}"
            )

        return response.content

    def get_financial_statements(
        self,
        corp_code: str,
        bsns_year: int,
        reprt_code: str = "11011",
        fs_div: str = "CFS",
    ):
        """
        단일회사 전체 재무제표를 조회합니다.

        reprt_code
        11011 = 사업보고서
        11012 = 반기보고서
        11013 = 1분기보고서
        11014 = 3분기보고서

        fs_div
        CFS = 연결재무제표
        OFS = 별도재무제표
        """

        url = f"{self.BASE_URL}/fnlttSinglAcntAll.json"

        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": str(bsns_year),
            "reprt_code": reprt_code,
            "fs_div": fs_div,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "000":
            raise RuntimeError(
                f"DART API 오류: "
                f"{data.get('status')} - {data.get('message')}"
            )

        return data

    def get_financial_indicators(
        self,
        corp_code: str,
        bsns_year: int,
        reprt_code: str = "11011",
        idx_cl_code: str = "M",
    ):
        """
        주요 재무지표를 조회합니다.
        """

        url = f"{self.BASE_URL}/fnlttSinglIndx.json"

        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": str(bsns_year),
            "reprt_code": reprt_code,
            "idx_cl_code": idx_cl_code,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "000":
            raise RuntimeError(
                f"DART API 오류: "
                f"{data.get('status')} - {data.get('message')}"
            )

        return data
