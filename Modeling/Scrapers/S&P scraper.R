library (rvest)
library(tidyverse)
webpage <- read_html('https://finance.yahoo.com/quote/%5EGSPC/history?period1=1585180800&period2=1589500800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')

tbl <- html_node(webpage, 'table') %>% html_table()

SP500 <- as.data.frame(tbl)

SP500$Date <- as.Date(SP500$Date, format = "%b %d, %Y")

SP500 <- select(SP500, c("Date", "Close*"))

SP500 <- rename(SP500, "SP500" = "Close*")

SP500 <- SP500[-dim(SP500)[1], ]

SP500 <- arrange(SP500, Date)

write.csv(SP500, "SP500.csv", row.names = FALSE)