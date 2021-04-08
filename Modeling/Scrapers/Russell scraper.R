library (rvest)
library(tidyverse)
webpage <- read_html('https://finance.yahoo.com/quote/%5ERUA/history?period1=1585180800&period2=1589500800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')

tbl <- html_node(webpage, 'table') %>% html_table()

russell <- as.data.frame(tbl)

russell$Date <- as.Date(russell$Date, format = "%b %d, %Y")

russell <- select(russell, c("Date", "Close*"))

russell <- rename(russell, "russell" = "Close*")

russell <- russell[-dim(russell)[1], ]

russell <- arrange(russell, Date)

write.csv(russell, "russell.csv", row.names = FALSE)