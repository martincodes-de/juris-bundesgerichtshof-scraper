# juris-bundesgerichtshof-scraper
Scraper to download judgments as structured PDF files

## How to use it
1. Visit https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en
2. Fill out the left form with search data & click "Suchen"
3. Copy the `sid` from result url (e.g. `https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en&sid=7d109c9352b24f64971653903997ea0c` would have sid `7d109c9352b24f64971653903997ea0c`)
4. run script and enter sid
_(By default, only judgments published by the 1-6th Criminal Senate are downloaded. If you don't like this, you can simply change it.)_
5. Files are structured / downloaded like this:

```
 Download/
 ├─ searchSubject/
 │  ├─ searchFileId/
 │  │  ├─ searchDate/
 │  │  │  ├─ 1 StR 412_02.pdf
 main.py
```
