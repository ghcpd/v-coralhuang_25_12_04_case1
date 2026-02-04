from user_display.validation.default import DefaultValidator
from user_display.errors import ValidationError


def test_default_validator_fills_missing_fields():
    v = DefaultValidator(strict=False)
    user = {"id": 1, "name": "A"}
    out = v.validate(user)
    assert out["email"] == ""
    assert "_last_login_ts" in out


def test_default_validator_strict_mode():
    v = DefaultValidator(strict=True)
    try:
        v.validate({"id": 1})
    except ValidationError:
        pass
    else:
        assert False, "Expected ValidationError"
