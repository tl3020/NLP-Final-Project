library(tidyverse)

#read the data
my_data <- read_csv("my_data.csv") 

#group the data by date

final_data <- my_data %>% group_by(date) %>% summarise(simple_score = mean(simple_senti, na.rm = TRUE),
                                                       vader_score = mean(vader_senti, na.rm = TRUE)) 
#summarize sentiment scores by taking average of sentiment score of all tweets on that day. 

#filter financial data
begin_date <- as.Date("2020-03-29") #29th March
end_date <- as.Date("2020-05-14") #14th May

SP_financial_data <- read_csv("PerformanceGraphExport.csv", col_types = 
                             cols(
                               `Effective date` = col_date(format = "%d/%m/%Y"),
                               `S&P 500` = col_double(),
                               change = col_double(),
                               `percentage change` = col_double(),
                               `Gain (Binary)` = col_double()
                             ))

SP_financial_data <- SP_financial_data %>% filter(`Effective date` >= begin_date &
                                              `Effective date` <= end_date)

dow30 <- read_csv("dow30.csv", col_types = 
                    cols(
                      `Date` = col_date(format = "%d/%m/%Y"),
                      `Close.` = col_double(),
                      `change` = col_double(),
                      `percentage change` = col_double(),
                      `Gain (Binary)` = col_integer()
                      ))


complete_data <- cbind(final_data, financial_data)

model_1 <- lm(score ~ change, data = complete_data)

model_2 <- glm(score ~ `Gain (Binary)`, data = complete_data)

exp(coef(model_2)) # exponentiate to get the odds of the stock going up if sentiment score goes up by 1 

write.csv(complete_data,"complete_data.csv", row.names = FALSE) 
