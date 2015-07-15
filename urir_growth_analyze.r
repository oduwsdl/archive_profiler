#!/usr/bin/env Rscript

f2si2 <- function (number, rounding=F, sep=" ") {
  lut <- c(1e-24, 1e-21, 1e-18, 1e-15, 1e-12, 1e-09, 1e-06, 
      0.001, 1, 1000, 1e+06, 1e+09, 1e+12, 1e+15, 1e+18, 1e+21, 
      1e+24)
  pre <- c("y", "z", "a", "f", "p", "n", "u", "m", "", "k", 
      "M", "B", "T", "P", "E", "Z", "Y")
  ix <- findInterval(number, lut)
  if (ix>0 && lut[ix]!=1) {
    if (rounding==T) {
      sistring <- paste(round(number/lut[ix], 1), pre[ix], sep=sep)
    } else {
      sistring <- paste(number/lut[ix], pre[ix], sep=sep)
    }
  } else {
    sistring <- as.character(number)
  }
  return(sistring)
}

urirdf <- read.csv("benchmark/urir-growth.csv", header=T)

print(urirdf)

png("benchmark/urir-growth.png", height=400, width=600, pointsize=18)

x <- urirdf$accumulated_urim_count
y <- urirdf$accumulated_urir_count
df <- data.frame(x, y)
s <- seq(from=0, to=max(x), length=500)

ypos <- pretty(c(0, max(y)), n=3)
ylb <- lapply(ypos, f2si2, rounding=T, sep="")
xpos <- pretty(c(0, max(x)), n=4)
xlb <- lapply(xpos, f2si2, rounding=T, sep="")

#par(mar=c(4,4,1,1)+0.1)
par(mar=c(3,3,1,1)+0.1, mgp=c(1.5,0.5,0), lwd=2)

plot(x, y, type="p", xaxt="n", yaxt="n", pch=0, col="red", ylab="URI-R Count", xlab="URI-M Count", ylim=c(0, max(y)))
axis(1, at=xpos, labels=xlb)
axis(2, at=ypos, labels=ylb)

m <- nls(y~I(K*x^beta), data=df, start=list(beta=1, K=1), trace=T)
lines(s, predict(m, list(x=s)), col="red")

summary(m)


x <- urirdf$urim_count
y <- urirdf$urir_count
m <- lm(y~x)

lines(x, y, type="p", col="blue")
lines(s, predict(m, list(x=s)), col="blue")

legend("topleft", inset=0.01, title="Collection", pch=c(1,0), col=c("blue", "red"), legend=c("Individual", "Accumulated"))

dev.off()


png("benchmark/relate-cdx-size-vs-urim-count-lineplot.png", height=400, width=600, pointsize=18)

x <- urirdf$cdx_size
y <- urirdf$urim_count
df <- data.frame(x, y)
s <- seq(from=0, to=max(x), length=500)

ypos <- pretty(c(0, max(y)), n=3)
ylb <- lapply(ypos, f2si2, rounding=T, sep="")
xpos <- pretty(c(0, max(x)), n=4)
xlb <- lapply(xpos, f2si2, rounding=T, sep="")

#par(mar=c(4,4,1,1)+0.1)
par(mar=c(3,3,1,1)+0.1, mgp=c(1.5,0.5,0), lwd=2)

plot(x, y, type="p", xaxt="n", yaxt="n", pch=0, col="red", ylab="URI-M Count", xlab="CDX Size", ylim=c(0, max(y)))
axis(1, at=xpos, labels=xlb)
axis(2, at=ypos, labels=ylb)

m <- lm(y~x)

lines(s, predict(m, list(x=s)), col="red")


dev.off()
