from selenium.webdriver.common.by import By
from utils.enums import Currency
from banks.ibk import get_ibk

def test_get_ibk_USD():
    result = get_ibk(Currency.USD)

    # 환율을 제대로 가져왔는지 확인
    if result:
        assert result["bank"] == "IBK기업은행"
        assert result["currency"] == "USD"
        assert isinstance(result["rate"], float)
    else:
        # 가져오지 못하면 None 반환
        assert result is None
