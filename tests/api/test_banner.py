from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from tests.conftest import HPOTTER_CREDENTIALS
from freezegun import freeze_time


def test_get_daily_banner_returns_200(client, banner_factory):
    banner_factory.create(username="hpotter", year="2526")
    res = client.get("me/2526/banner", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK


def test_get_daily_banner_contains_expected_fields(client, banner_factory):
    banner_factory.create(username="hpotter", year="2526")
    res = client.get("me/2526/banner", auth=HPOTTER_CREDENTIALS)
    banner = res.json()
    expected_fields = {"id", "year", "username", "date", "banner_type", "display_text"}
    assert expected_fields.issubset(banner.keys())


def test_get_daily_banner_only_contains_banner_for_user_and_year(
    client, banner_factory
):
    banner_factory.create(username="hpotter", year="2526")
    banner_factory.create(username="hgranger", year="2526")
    res = client.get("me/2526/banner", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK
    banner = res.json()
    assert banner["username"] == "hpotter", "Response contains banner for other user"
    assert banner["year"] == "2526", "Response contains banner for other year"


@freeze_time("2026-01-02")
def test_get_daily_banner_new_date_returns_new_banner(client, banner_factory):
    banner_factory.create(
        username="hpotter",
        year="2526",
        date="2026-01-01",
        banner_type="excuse",
        display_text="Test Quote",
    )
    res1 = client.get("me/2526/banner", auth=HPOTTER_CREDENTIALS)

    assert res1.status_code == HTTP_200_OK
    banner1 = res1.json()
    assert (
        banner1["date"] == "2026-01-02"
    ), "Banner date should be updated to current date"
    assert (
        banner1["banner_type"] == "quote"
    ), "Banner type should be reset to quote for new date"


def test_update_banner_with_quote_type_resets_display_text(client, banner_factory):
    banner_factory.create(
        username="hpotter",
        year="2526",
        banner_type="excuse",
        display_text="Test Excuse",
    )
    new_banner = {"banner_type": "quote"}

    res = client.patch("me/2526/banner", json=new_banner, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK
    updated_banner = res.json()
    assert (
        updated_banner["banner_type"] == "quote"
    ), "Banner type should be updated to quote"
    assert (
        updated_banner["display_text"] != "Test Excuse"
    ), "Banner display text should be updated from previous excuse text"


def test_update_banner_with_excuse_type(client, banner_factory):
    banner_factory.create(
        username="hpotter",
        year="2526",
        banner_type="quote",
        display_text="Test Quote",
    )
    new_banner = {"banner_type": "excuse"}

    res = client.patch("me/2526/banner", json=new_banner, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK
    updated_banner = res.json()
    assert (
        updated_banner["banner_type"] == "excuse"
    ), "Banner type should be updated to excuse"
    assert (
        updated_banner["display_text"] != "Test Quote"
    ), "Banner display text should be updated from previous quote text"


def test_update_banner_with_custom(client, banner_factory):
    banner_factory.create(username="hpotter", year="2526", banner_type="excuse")
    new_banner = {
        "banner_type": "custom",
        "display_text": "This is a custom banner",
    }

    res = client.patch("me/2526/banner", json=new_banner, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == HTTP_200_OK
    updated_banner = res.json()
    assert (
        updated_banner["banner_type"] == "custom"
    ), "Banner type should be updated to custom"
    assert (
        updated_banner["display_text"] == "This is a custom banner"
    ), "Banner display text should be updated to new value"


def test_update_banner_with_invalid_user_or_year_returns_404(client):
    res = client.patch(
        "me/2526/banner",
        json={"banner_type": "custom", "display_text": "Test"},
        auth=HPOTTER_CREDENTIALS,
    )
    assert (
        res.status_code == HTTP_404_NOT_FOUND
    ), "Should return 404 for non-existent banner"


def test_update_banner_with_missing_data_returns_400(client, banner_factory):
    banner_factory.create(username="hpotter", year="2526")
    res = client.patch(
        "me/2526/banner",
        json={"banner_type": "custom"},
        auth=HPOTTER_CREDENTIALS,
    )
    assert (
        res.status_code == HTTP_400_BAD_REQUEST
    ), "Should return 400 for missing display_text for custom banner"
