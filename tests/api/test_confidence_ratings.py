from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
)
from tests.conftest import HPOTTER_CREDENTIALS


def test_confidence_ratings_endpoint_returns_200(
    client, student_abc_config, abc_patched_client, confidence_rating_factory
):
    confidence_rating_factory.create(username="hpotter", year="2526")
    with abc_patched_client(student_abc_config) as client:
        res = client.get(
            "me/2526/personal-confidence-ratings",
            params={"module_codes": ["60001", "60002"]},
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == HTTP_200_OK


def test_confidence_ratings_response_contains_expected_fields(
    client, student_abc_config, abc_patched_client, confidence_rating_factory
):
    confidence_rating_factory.create(username="hpotter", year="2526")
    with abc_patched_client(student_abc_config) as client:
        res = client.get(
            "me/2526/personal-confidence-ratings",
            params={"module_codes": ["60001", "60002"]},
            auth=HPOTTER_CREDENTIALS,
        )
    expected_fields = {"id", "year", "username", "module_ratings"}
    assert expected_fields.issubset(res.json().keys())


def test_confidence_ratings_response_only_contains_ratings_for_user_and_year(
    client, student_abc_config, abc_patched_client, confidence_rating_factory
):
    confidence_rating_factory.create(username="hpotter", year="2425")
    confidence_rating_factory.create(username="hgranger", year="2425")
    confidence_rating_factory.create(username="hpotter", year="2526")
    confidence_rating_factory.create(username="hgranger", year="2526")
    with abc_patched_client(student_abc_config) as client:
        res = client.get(
            "me/2526/personal-confidence-ratings",
            params={"module_codes": ["60001", "60002"]},
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == HTTP_200_OK
    confidence_rating = res.json()
    assert confidence_rating["username"] == "hpotter"
    assert confidence_rating["year"] == "2526"


def test_module_rating_contains_expected_fields(
    client,
    student_abc_config,
    abc_patched_client,
    confidence_rating_factory,
    module_rating_factory,
):
    confidence_rating = confidence_rating_factory.create(
        username="hpotter", year="2526"
    )
    module_rating_factory.create(
        confidence_rating=confidence_rating, module_code="60001"
    )
    with abc_patched_client(student_abc_config) as client:
        res = client.get(
            "me/2526/personal-confidence-ratings",
            params={"module_codes": ["60001"]},
            auth=HPOTTER_CREDENTIALS,
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
        f"me/2526/personal-confidence-ratings/modules/{module_rating.id}",
        json={"rating": 5},
        auth=HPOTTER_CREDENTIALS,
    )

    if res.status_code != HTTP_200_OK:
        print(f"Response: {res.json()}")
        print(f"Module rating ID: {module_rating.id}")

    assert res.status_code == HTTP_200_OK
    assert res.json()["rating"] == 5


def test_update_nonexistent_module_rating_returns_404(client):
    res = client.patch(
        "me/2526/personal-confidence-ratings/modules/9999",
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
        f"me/2526/personal-confidence-ratings/modules/{module_rating.id}",
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
        f"me/2526/personal-confidence-ratings/modules/{module_rating.id}",
        json={"rating": 6},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == HTTP_406_NOT_ACCEPTABLE
    assert res.json()["detail"] == "Rating must be between 1 and 5."
