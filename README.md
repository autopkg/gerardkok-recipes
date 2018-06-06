# autopkg-recipes

Recipes for AutoPkg (https://github.com/autopkg/autopkg).

## Scribus recipe

The recipe for Scribus is just a Munki importer for a download recipe by @hansen_m, so you'll have to add his autopkg repo (https://github.com/autopkg/hansen-m-recipes.git) to your autopkg repo list, before the Scribus munki recipe will work.

## DotNetCoreSDK recipe

The DotNetCoreSDK munki recipe depends on [@keeleysam](https://github.com/keeleysam)'s [MunkiPkginfoReceiptsEditor](https://github.com/autopkg/keeleysam-recipes/blob/master/GoogleTalkPlugin/MunkiPkginfoReceiptsEditor.py) to set 'com.microsoft.dotnet.sharedhost.component.osx.x64' to optional, because the installer sometimes contains multiple different versions of that package.

## GPGTools recipe

Work in progress. The recipe does not add an uninstall script to the munki pkgsinfo yet, and no verification that the download is legitimate is being done yet.
Downloading the suite doesn't work from time to time; trying again usually works for me.

## Python-package

Work in progress. These are generic recipes to include Python packages in your AutoPkg run. I'm not entirely convinced myself that this is the right way to handle Python packages, but so far it serves my needs.
The recipes require pypixmlrpc (`easy_install pypixmlrpc`). Creating an AutoPkg recipe for a Python package requires making an override, just like the AppStoreApp recipe by @nmcspadden (https://github.com/autopkg/nmcspadden-recipes.git).
Run `autopkg make-override Python-package.munki.recipe -n MyPythonPackage.munki`, then edit the NAME and the PYTHON_PKG_NAME input variables, and any other Munki pkginfo fields you wish to change (description, developer).

## Shared processors

### GPGSignatureVerifier

This processor verifies signatures of gpg-signed files against a gpg key. If gpg cannot be found at %gpg_path% (defaults to `/usr/local/bin/gpg`), this processor will silently succeed.
If will also succeed if the gpg executable can be found, the public key belonging to %public_key_id% can be imported, and gpg is able to verify
that the signature in %signature_file% matches that of %distribution_file%. It will throw a ProcessorError otherwise.

##### Example usage

```xml
<key>Processor</key>
<string>com.github.autopkg.gerardkok-recipes.SharedProcessors/GPGSignatureVerifier</string>
<key>Comment</key>
<string>verify gpg-signature of download</string>
<key>Arguments</key>
<dict>
    <key>public_key_id</key>
    <string>%KEYID%</string>
    <key>distribution_file</key>
    <string>%pathname%</string>
    <key>signature_file</key>
    <string>%RECIPE_CACHE_DIR%/downloads/%NAME%.dmg.asc</string>
</dict>
```

The public key id %KEYID% is an input variable, and can usually be found on the website of the developer of the application that's being packaged.
The signature is different for each download, use for example the URLDownloader processor to write it to a file. I think it's important that the name
of the signature file is just the name of the downloaded package with '.asc' appended.

Use with some care, because this is the first time I've programmed something against gpg.
