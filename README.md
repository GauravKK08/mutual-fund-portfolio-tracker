# mutual-fund-portfolio-tracker
About: Helpful script to track a person's mutual fund portfolio

This is a very old script written back in 2013/2014 , i recently ported it to Python3 and decided to share with all.
This script downloads the latest NAV's of all the mutual funds from SEBI AMFI's website and multiplies it against the units you have for each of your investment.
Your investment records need to be maintained in a CSV, with format like below:

```
scheme_code,no_of_units,folio_number
112323,969,1234567890
```

The script should be executed on python3 shell and script would ask the user to select the portfolio, one can have multiple portfolios like your personal portflio, family portfolio etc.

Once user selects the portfolio number, the latest NAV is downlaoded and current value of investments is shown to the user in an intelligible manner.

The `scheme_code` is to be taken from https://www.amfiindia.com/spages/NAVAll.txt.

The `no_of_units` is the no of units that you have purchased for the particular fund.

The `folio_number` is your investment folio number (although not required for the script processing as such, but good for tracking purposes.)
