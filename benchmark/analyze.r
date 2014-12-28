#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=T)
if (length(args) < 1) {
  print("Please pass the CSV file as a command line argument.")
  quit()
}
fpath <- gsub("summary-|.csv$", "", args[1])

profiles <- read.csv(args[1], header=T)

print(profiles)

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
kpos <- pretty(c(0, max(profiles$suburi_keys)), n=10)
klb <- sapply(kpos, FUN=f2si2, rounding=T, sep="")
spos <- pretty(c(0, max(profiles$profile_size)), n=10)
slb <- sapply(spos, FUN=f2si2, rounding=T, sep="")
tpos <- pretty(c(0, max(profiles$profiling_time/60)), n=10)
tlb <- sapply(tpos, FUN=f2si2, rounding=T, sep="")

keybar <- paste(fpath, "-keys-barplot.png", sep="")
png(keybar, height=500, width=800, pointsize=18)

par(mar=c(5,9,2,2)+0.1)
bplt <- barplot(profiles$suburi_keys, names.arg=profiles$profile_id, horiz=T, las=2, axes=F, xlim=c(0, max(kpos)))#
axis(1, at=kpos, labels=klb)
text(x=profiles$suburi_keys, y=bplt, labels=sapply(profiles$suburi_keys, FUN=f2si2, rounding=T, sep=""), pos=4, offset=0.2, xpd=T)
title(xlab="Number of Sub-URI Keys")

dev.off()


keyline <- paste(fpath, "-keys-lineplot.png", sep="")
png(keyline, height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(profiles$suburi_keys, type='b', xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, max(kpos)))
axis(1, at=c(1:12), labels=xlb)
axis(2, at=kpos, labels=klb)
title(ylab="Number of Sub-URI Keys", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()


sizeline <- paste(fpath, "-filesize-lineplot.png", sep="")
png(sizeline, height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(profiles$profile_size, type='b', xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, max(spos)))
axis(1, at=c(1:12), labels=xlb)
axis(2, at=spos, labels=slb)
title(ylab="Profile size", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()


timeline <- paste(fpath, "-time-lineplot.png", sep="")
png(timeline, height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(profiles$profiling_time/60, type='b', xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, max(tpos)))
axis(1, at=c(1:12), labels=xlb)
axis(2, at=tpos, labels=tlb)
title(ylab="Profiling time (minutes)", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()
