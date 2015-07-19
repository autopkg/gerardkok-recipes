# autopkg-recipes

Recipes for AutoPkg (https://github.com/autopkg/autopkg).

## Keka and Scribus recipes

The recipes for Keka and Scribus are just Munki importers for download recipes by @hansen_m, so you'll have to add his autopkg repo (https://github.com/autopkg/hansen-m-recipes.git) to your autopkg repo list, before the munki recipes for Keka and Scribus will work.

## GPGTools recipe

Work in progress. The recipe does not add an uninstall script to the munki pkgsinfo yet, and no verification that the download is legitimate is being done yet.
Downloading the suite doesn't work from time to time; trying again usually works for me.

## Python-package

Work in progress. These are generic recipes to include Python packages in your AutoPkg run. I'm not entirely convinced myself that this is the right way to handle Python packages, but so far it serves my needs.
The recipes require pypixmlrpc (`easy_install pypixmlrpc`). Creating an AutoPkg recipe for a Python package requires making an override, just like the AppStoreApp recipe by @nmcspadden (https://github.com/autopkg/nmcspadden-recipes.git).
Run `autopkg make-override Python-package.munki.recipe -n MyPythonPackage.munki`, then edit the NAME and the PYTHON_PKG_NAME input variables, and any other Munki pkginfo fields you wish to change (description, developer).
