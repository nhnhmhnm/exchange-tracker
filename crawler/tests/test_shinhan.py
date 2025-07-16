from banks.shinhan import get_shinhan
from utils.enums import Currency

def test_get_shinhan_USD():
    result = get_shinhan(Currency.JPY)

    if result:
        assert result["bank"] == "SHINHAN"
        assert result["currency"] == "JPY"
        assert isinstance(result["rate"], float)
    else:
        assert result is None
