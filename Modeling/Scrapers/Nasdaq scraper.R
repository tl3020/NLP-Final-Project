library (rvest)
library(tidyverse)
webpage <- read_html('https://finance.yahoo.com/quote/%5EIXIC/history?period1=1585180800&period2=1589500800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')

tbl <- html_node(webpage, 'table') %>% html_table()

nasdaq <- as.data.frame(tbl)

nasdaq$Date <- as.Date(nasdaq$Date, format = "%b %d, %Y")

nasdaq <- select(nasdaq, c("Date", "Close*"))

nasdaq <- rename(nasdaq, "nasdaq" = "Close*")

nasdaq <- nasdaq[-dim(nasdaq)[1], ]

nasdaq <- arrange(nasdaq, Date)

write.csv(nasdaq, "nasdaq.csv", row.names = FALSE)