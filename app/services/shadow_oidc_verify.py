"""Stub for environments without shadow_oidc_verify package installed."""


class _ShadowOidcVerify:
    validate_token_middleware = None
    validate_claims_middleware = None


shadow_oidc_verify = _ShadowOidcVerify()
