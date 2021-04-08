library (rvest)
webpage <- read_html('https://finance.yahoo.com/quote/%5EDJI/history?period1=1585267200&period2=1589500800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')

tbl <- html_node(webpage, 'table') %>% html_table()

dow30 <- as.data.frame(tbl)

dow30$Date <- as.Date(dow30$Date, format = "%b %d, %Y")

dow30 <- select(dow30, c("Date", "Close*"))

dow30 <- rename(dow30, "dow30" = "Close*")

dow30 <- dow30[-dim(dow30)[1], ]

dow30 <- arrange(dow30, Date)

write.csv(dow30, "dow30.csv", row.names = FALSE)