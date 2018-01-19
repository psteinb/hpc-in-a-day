#!/usr/bin/env Rscript
library(ggplot2)
library(dplyr)
library(scales)

expons = 0:10

s_values = 2^expons
p_values = c(0.5,.75,.9,.95,.99)

amdahl_df = data.frame(p_values=p_values)

amdahl_df = expand.grid(p_values=p_values,s_values=s_values) %>%
    mutate( S = 1/(1 - p_values + (p_values/s_values))  ) %>%
    tbl_df



plt = ggplot(amdahl_df,aes(s_values, S, color=as.factor(p_values)))
plt = plt + theme_bw()
plt = plt + geom_line()
plt = plt + xlab("speed-up of serial section, s")
plt = plt + ylab("theoretical speed-up, S")
plt = plt + scale_y_continuous(trans=log2_trans(), breaks=2^(0:14))
plt = plt + scale_x_continuous(trans=log2_trans(), breaks=2^(seq(0,13,1)))
plt = plt + scale_color_discrete(name="portion p of code to parallelize")

ggsave("amdahls_law.svg",plt,width=32,height=18,unit="cm")
ggsave("amdahls_law.png",plt,width=32,height=18,unit="cm")
