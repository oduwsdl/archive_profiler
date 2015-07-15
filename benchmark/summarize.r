#!/usr/bin/env Rscript

fpath <- "benchmark/archiveit/"

p00 <- read.csv("benchmark/archiveit/summary-ukwa-2000.csv", header=T)
p01 <- read.csv("benchmark/archiveit/summary-ukwa-2001.csv", header=T)

print(p00)
print(p01)

#quit()

f2si2<-function (number, rounding=F, sep=" ") 
{
    lut <- c(1e-24, 1e-21, 1e-18, 1e-15, 1e-12, 1e-09, 1e-06, 
        0.001, 1, 1000, 1e+06, 1e+09, 1e+12, 1e+15, 1e+18, 1e+21, 
        1e+24)
    pre <- c("y", "z", "a", "f", "p", "n", "u", "m", "", "k", 
        "M", "G", "T", "P", "E", "Z", "Y")
    ix <- findInterval(number, lut)
    if (ix>0 && lut[ix]!=1) {
        if (rounding==T) {
         sistring <- paste(round(number/lut[ix]), pre[ix], sep=sep)
        }
        else {
         sistring <- paste(number/lut[ix], pre[ix], sep=sep)
        }
    }
    else {
        sistring <- as.character(number)
    }
    return(sistring)
}


xlb <- c("H1", "H2", "H3", "H4", "H5", "Hx", "P1", "P2", "P3", "P4", "P5", "Px")
kpos <- pretty(c(0, max(p01$suburi_keys, p00$suburi_keys)), n=10)
klb <- sapply(kpos, FUN=f2si2, rounding=T, sep="")
spos <- pretty(c(0, max(p01$profile_size, p00$profile_size)), n=10)
slb <- sapply(spos, FUN=f2si2, rounding=T, sep="")
tpos <- pretty(c(0, max(p01$profiling_time/60, p00$profiling_time/60)), n=10)
tlb <- sapply(tpos, FUN=f2si2, rounding=T, sep="")


keyline <- paste(fpath, "summary-keys-lineplot.png", sep="")
png(keyline, height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(p01$suburi_keys, type='b', col="red", xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, max(kpos)))
lines(p00$suburi_keys, type='b', col="blue", pch=0)
axis(1, at=c(1:12), labels=xlb)
axis(2, at=kpos, labels=klb)
title(ylab="Number of Sub-URI Keys", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()


sizeline <- paste(fpath, "summary-filesize-lineplot.png", sep="")
png(sizeline, height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(p01$profile_size, type='b', col="red", xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, max(spos)))
lines(p00$profile_size, type='b', col="blue", pch=0)
axis(1, at=c(1:12), labels=xlb)
axis(2, at=spos, labels=slb)
title(ylab="Profile size", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()


timeline <- paste(fpath, "summary-time-lineplot.png", sep="")
png(timeline, height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(p01$profiling_time/60, type='b', col="red", xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, max(tpos)))
lines(p00$profiling_time/60, type='b', col="blue", pch=0)
axis(1, at=c(1:12), labels=xlb)
axis(2, at=tpos, labels=tlb)
title(ylab="Profiling time (minutes)", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()
