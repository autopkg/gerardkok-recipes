# autopkg-recipes

Recipes for AutoPkg (https://github.com/autopkg/autopkg).

## Keka and Scribus recipes

The recipes for Keka and Scribus are just Munki importers for download recipes by @hansen_m, so you'll have to add his autopkg repo (https://github.com/autopkg/hansen-m-recipes.git) to your autopkg repo list, before the munki recipes for Keka and Scribus will work.

## GPGTools recipe

Work in progress. The recipe does not add an uninstall script to the munki pkgsinfo yet, and no verification that the download is legititmate is being done yet.

## SharedProcessors

Work in progress. I'm not entirely convinced myself that this is the right way to handle Python packages, but so far it serves my needs. The PyPIInfoProvider requires pypixmlrpc to work (`easy_install pypixmlrpc`).