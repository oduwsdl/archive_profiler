#!/usr/bin/env Rscript

tms <- read.csv("benchmark/uri_counting_time.csv", header=T)
x <- tms$size
y <- tms$time/60
fit <- lm(y~x)
xx <- seq(0,260, length=100)

png("benchmark/cdx-transformation-analysis.png", height=600, width=800, pointsize=18)

plot(x,y, xlim=c(0, 260), ylim=c(0, 500), ylab="Time (Minutes)", xlab="CDX Size (GB)")
lines(xx, predict(fit, data.frame(x=xx)), col="red")

dev.off()

print(summary(fit))
