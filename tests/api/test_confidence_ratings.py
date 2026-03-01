from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE

from tests.conftest import HPOTTER_CREDENTIALS


def test_confidence_ratings_endpoint_returns_200(client, confidence_rating_factory):
    confidence_rating_factory.create(username="hpotter", year="2526")
    res = client.get(
        "/2526/hpotter/personal-confidence-ratings", auth=HPOTTER_CREDENTIALS
    )
    assert res.status_code == HTTP_200_OK


def test_get_confidence_ratings_returns_404_when_not_found(client):
    res = client.get(
        "/2526/hpotter/personal-confidence-ratings", auth=HPOTTER_CREDENTIALS
    )
    assert res.status_code == HTTP_404_NOT_FOUND


def test_confidence_ratings_response_contains_expected_fields(
    client, confidence_rating_factory
):
    confidence_rating_factory.create(username="hpotter", year="2526")
    res = client.get(
        "/2526/hpotter/personal-confidence-ratings", auth=HPOTTER_CREDENTIALS
    )
    confidence_rating = res.json()
    expected_fields = {
        "id",
        "year",
        "username",
        "module_ratings",
    }
    assert expected_fields.issubset(confidence_rating.keys())


def test_confidence_ratings_response_only_contains_ratings_for_user_and_year(
    client, confidence_rating_factory
):
    confidence_rating_factory.create(username="hpotter", year="2425")
    confidence_rating_factory.create(username="hgranger", year="2425")
    confidence_rating_factory.create(username="hpotter", year="2526")
    confidence_rating_factory.create(username="hgranger", year="2526")

    res = client.get(
        "/2526/hpotter/personal-confidence-ratings", auth=HPOTTER_CREDENTIALS
    )

    assert res.status_code == HTTP_200_OK
    confidence_rating = res.json()

    assert (
        confidence_rating["username"] == "hpotter"
    ), "Response contains ratings for other users"
    assert (
        confidence_rating["year"] == "2526"
    ), "Response contains ratings for other years"


def test_module_rating_contains_expected_fields(
    client, confidence_rating_factory, module_rating_factory
):
    confidence_rating = confidence_rating_factory.create(
        username="hpotter", year="2526"
    )
    module_rating_factory.create(confidence_rating=confidence_rating)

    res = client.get(
        "/2526/hpotter/personal-confidence-ratings", auth=HPOTTER_CREDENTIALS
    )

    module_ratings = res.json()["module_ratings"]
    assert len(module_ratings) > 0

    expected_fields = {"id", "module_code", "rating", "term_week"}
    assert expected_fields.issubset(module_ratings[0].keys())


def test_update_module_rating(client, confidence_rating_factory, module_rating_factory):
    confidence_rating = confidence_rating_factory.create(
        username="hpotter", year="2526"
    )
    module_rating = module_rating_factory.create(
        confidence_rating=confidence_rating, rating=3
    )

    res = client.patch(
        f"/2526/hpotter/personal-confidence-ratings/modules/{module_rating.id}",
        json={"rating": 5},
        auth=HPOTTER_CREDENTIALS,
    )

    if res.status_code != 200:
        print(f"Response: {res.json()}")
        print(f"Module rating ID: {module_rating.id}")

    assert res.status_code == 200
    assert res.json()["rating"] == 5


def test_update_nonexistent_module_rating_returns_404(client):
    res = client.patch(
        "/2526/hpotter/personal-confidence-ratings/modules/9999",
        json={"rating": 5},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_404_NOT_FOUND


def test_cannot_update_other_users_module_rating(
    client, confidence_rating_factory, module_rating_factory
):
    confidence_rating = confidence_rating_factory.create(
        username="hgranger", year="2526"
    )
    module_rating = module_rating_factory.create(confidence_rating=confidence_rating)

    res = client.patch(
        f"/2526/hpotter/personal-confidence-ratings/modules/{module_rating.id}",
        json={"rating": 5},
        auth=HPOTTER_CREDENTIALS,
    )

    assert res.status_code == HTTP_401_UNAUTHORIZED


def test_update_module_rating_with_invalid_rating_returns_406(
    client, confidence_rating_factory, module_rating_factory
):
    confidence_rating = confidence_rating_factory.create(
        username="hpotter", year="2526"
    )
    module_rating = module_rating_factory.create(
        confidence_rating=confidence_rating, rating=3
    )

    res = client.patch(
        f"/2526/hpotter/personal-confidence-ratings/modules/{module_rating.id}",
        json={"rating": 6},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_406_NOT_ACCEPTABLE
    assert res.json()["detail"] == "Rating must be between 1 and 5."
