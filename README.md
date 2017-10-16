# wo_desc_analysis
These scripts run a series of regular expressions through wo descriptions to categorize service center calls

It takes an excel file with phrases typed out by a user, and "regex_creator" reads that file and creates a
regular expression for each series and phrases. It also reverses the order to explore more possible mathces.

You can then run "word_analysis" to scan the service call descriptions for any matches in the regex list.
