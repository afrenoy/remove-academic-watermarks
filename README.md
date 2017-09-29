Remove watermarks identifying who downloaded a pdf from a paywall
===

The only external dependency is `pdftk`

The script `cleanpdf.py` takes as inputs the source pdf, the destination pdf, and a list of text strings identifying watermarks to remove from the pdf

Classical watermarks used by many publishers indicate the name of the institution, the IP address, the date and time of download, and standard patterns text such as 'For personal use only'...

Example:

    ./cleanpdf.py input.pdf output.pdf 'My university' 'Downloaded from' 'Access provided' 'For personal use only' '129.000.000.001'

