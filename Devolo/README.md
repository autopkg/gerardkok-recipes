# Signature verification fails for Cockpit 4.4.0

Signatuer verification for Cockpit version 4.4.0 appears to fail. Mimicking CodeSignatureVerifier on the command line gives:
```shell
$ codesign --verify --verbose=1 /opt/devolo/share/devolonetsvc/updates/install/cockpit-installation.app
/opt/devolo/share/devolonetsvc/updates/install/cockpit-installation.app: CSSMERR_TP_CERT_EXPIRED
In architecture: x86_64
```
I don't think this can be fixed by passing certain flags to the `codesign` command, but that the signature has to be fixed instead.

If you want to run the recipe before Devolo has fixed this, you'll have to set the variable `DISABLE_CODE_SIGNATURE_VERIFICATION` to a non-empty value to skip signature verification (for more information see https://github.com/autopkg/autopkg/wiki/Using-CodeSignatureVerification#disabling-codesignatureverification-in-an-existing-recipe).