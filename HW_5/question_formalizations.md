**Task 1: Noise**

Version 1: The Mayor's question -- Are noise complaints due to different causes throughout the year?

Version 2: Of the complaints that have complaint type pertaining to "Noise", do their descriptions differ with respect to a trend in time of year?

Version 3: Of the complaints in the NYC 311 Dataset for the year 2020, what are the most frequent descriptions for the various "Noise" complaint types, for each month?

**Version 4: Of the complaints in the NYC 311 Dataset for the year 2020, for every month (Jan, Feb, ..., Dec), what are the frequencies of each descriptor for complaints of the type "Noise - [...]"?**

----


*Note that for simplicity we're treating all complaint types starting with "Noise" as the same rather than differentiating "Residential" from "Street/Sidewalk", etc.*

*Implementation Strategy: Note that Version 4's question can be answered directly by parsing through the dataset and creating a map with key (month, [descriptor that correspond to complaint type "Noise..."]) and incrementing a counter for each descriptor every time its encountered for each given month.*

*Then, we can create a bar chart where we we have the frequency of each noise descriptor (loud party, etc.) displayed for each month.  Perhaps order the bars for each month, for each descriptor, and color code the bars by month. Then we can visually see the monthly change of each subtype of noise complaint.*

----

**Task 2: Urban Rodents**

Version 1: The Departments of Sanitation and Health's question -- Where in NYC are rats most likely to create sanitization issues?

Version 2: What types of structures, buildings, and properties in NYC are rats most likely to create sanitization issues?

*Note: In Version 3, we drop "create sanitization issues" since we're making the educated assumption that a rat's presence / sighting is enough to indicate a sanitization issue, or risk thereof.*

Version 3: Of the complaints in the NYC 311 Dataset for the year 2020, what location types -- structures, buildings, and properties in NYC were most frequently associated with the complaint type "Rodent" and the descriptor "Rat Sighting"?

**Version 4:  Of the complaints in the NYC 311 Dataset for the year 2020, what are the frequencies for the complaint type "Rodent" and descriptor "Rat Sighting" of each location type (structures, buildings, and properties) in NYC?**

----

*Implementation Strategy: Version 4's question involves parsing through the dataset and finding all rows where the complaint type is Rodent, the descriptor is Rat Sighting, and then keying the location type into the map, and incrementing for each location type when it is encountered in the data set.*

*Then, we can create a bar chart where we have the frequency of each location type's rat sightings.  Color coding is not so critical here since our x axis only needs to represent one dimension of information (the location).*

*Note: In Task 1, we had to represent both every type of noise descriptor and every month, but just have the x axis, hence color coding by month (the legend is consistent for each descriptor) was the "extra visual dimension" needed to do so.*