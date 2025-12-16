Title: A TOTP implementation
Date: 2024-09-02 11:14
Modified: 2025-12-16 13:21
Category: Coding
Slug: totp-implementation
Status: published

Here's a TOTP ([RFC 6238](https://www.rfc-editor.org/rfc/rfc6238)) implementation I submitted to a library. The PR was rejected because the maintainer considered it out of scope, but the implementation is fine.

I'll be deleting the branch, but I figured I'd might as well store it here for posterity.

```python
import base64
import hmac
import secrets
import struct
import time as _time
import typing as t
import urllib.parse as _parse


_allowed_hashes = ["sha1", "sha256", "sha512"]

_pack_uint64 = struct.Struct(">Q").pack
_unpack_uint32 = struct.Struct(">I").unpack


class UnknownHashAlgorithmError(Exception):
    """Raised if the named hash algorithm was not recognised."""

    def __init__(self, alg: str):
        """
        Args:
            alg: Hash algorithm name given
        """
        self.alg = alg
        message = f"'{alg}' is not a supported TOTP hash algorithm"
        super().__init__(message)


class TOTP:
    """An implementation of TOTP (RFC 6238)."""

    def __init__(
        self,
        key: t.Optional[bytes] = None,
        *,
        alg: str = "sha1",
        digits: int = 6,
        period: int = 30,
        key_size: int = 16,
    ) -> None:
        """
        Args:
            key: A buffer of random bytes acting as a key. Will be generated if None.
            alg: Hash algorithm to use for the OTP. Defaults to "sha1", but supports sha256 and sha512.
            digits: Length of the OTP. Defaults to 6 digits.
            period: Validity period in seconds of the OTP. Defaults to 30.
            key_size: If no key is given, the length in bytes of the key go generate. Default to 16.

        Raises:
            UnknownHashAlgorithmError: If the hash algorithm given is not recognised.
        """
        if alg not in _allowed_hashes:
            raise UnknownHashAlgorithmError(alg)
        if key is None:
            key = secrets.token_bytes(key_size)
        self.alg = alg
        self.key = key
        self.digits = digits
        self.period = period

    def to_dict(self) -> dict:
        """Write the state to a dictionary for serialisation."""
        return {
            "alg": self.alg,
            "key": base64.b64encode(self.key).decode("ascii"),
            "digits": self.digits,
            "period": self.period,
        }

    @classmethod
    def from_dict(cls, src: dict) -> "TOTP":
        """Extract the state from a dictionary."""
        return cls(
            alg=src["alg"],
            key=base64.b64decode(src["key"].encode("ascii")),
            digits=src["digits"],
            period=src["period"],
        )

    def to_url(self, account_name: str, issuer: t.Optional[str] = None) -> str:
        """Convert the object to a Google Authenticator key URI.

        Args:
            account_name: The user's account name.
            issuer: The name of the issuer.

        Returns:
            An OTP key URI.
        """
        result = ["otpauth://totp/"]
        params = {
            "secret": base64.b32encode(self.key).decode("ascii").rstrip("="),
            "algorithm": self.alg.upper(),
            "digits": self.digits,
            "period": self.period,
        }
        if issuer is not None:
            result.append(_parse.quote(issuer) + ":")
            params["issuer"] = issuer
        result.append(_parse.quote(account_name) + "?")
        result.append(_parse.urlencode(params))
        return "".join(result)

    def _normalise(self, now: int) -> int:
        return now // self.period

    def _generate(self, now: int) -> str:
        packed = _pack_uint64(now)
        digest = hmac.new(
            key=self.key,
            msg=packed,
            digestmod=self.alg,
        ).digest()
        offset = digest[-1] & 0xF
        value = _unpack_uint32(digest[offset : offset + 4])[0] & 0x7FFFFFFF
        return f"{value:0>{self.digits}}"[-self.digits :]

    def generate(self, now: t.Optional[int] = None) -> str:
        """Generate a TOTP.

        Args:
            now: A Unix timestamp. Defaults to the current time.

        Returns:
            The TOTP.
        """
        if now is None:
            now = int(_time.time())
        return self._generate(self._normalise(now))

    def check(self, otp: str, *, window: int = 2, now: t.Optional[int] = None) -> bool:
        """Check a TOTP against the current expected TOTP and the previous one.

        Args:
            otp: OTP to check.
            window: Number of windows back in time to use when checking checking the OTP.
            now: A Unix timestamp. Defaults to the current time.

        Returns:
            True if the OTP matched, False otherwise.
        """
        if now is None:
            now = int(_time.time())
        normalised_now = self._normalise(now)
        for i in range(0, window):
            if secrets.compare_digest(otp, self._generate(normalised_now - i)):
                return True
        return False
```

The reason I wrote this is that [passlib](https://pypi.org/project/passlib/) looks to be effectively dead and combination of a lack of maintenance over the past four years and dependencies on long-deprecated features (such as `pkg_resources`) means it's increasingly unfit for purpose.

Update (2025-12-16): I [merged this into my adjunct library](https://github.com/kgaughan/adjunct/pull/25) about a month ago, so you'll find a maintained version of it there with tests and documentation.
