profiles <- read.csv("summary.csv", header=T)

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


png("profile-keys-analysis.png", height=500, width=800, pointsize=18)

par(mar=c(5,9,2,2)+0.1)
bplt <- barplot(profiles$suburi_keys, names.arg=profiles$profile_id, horiz=T, las=2, xlim=c(0, 500000), axes=F)
axis(1, at=c(0:10)*50000, labels=sapply(c(0:10)*50000, FUN=f2si2, rounding=T, sep=""))
text(x=profiles$suburi_keys, y=bplt, labels=sapply(profiles$suburi_keys, FUN=f2si2, rounding=T, sep=""), pos=4, offset=0.2, xpd=T)
title(xlab="Number of Sub-URI Keys")

dev.off()

xlb <- c("H1", "H2", "H3", "H4", "H5", "Hx", "P1", "P2", "P3", "P4", "P5", "Px")

png("profile-keys-line-analysis.png", height=500, width=800, pointsize=18)

par(mar=c(4,4,2,2)+0.1)
plot(profiles$suburi_keys, type='b', xaxt="n", yaxt="n", ylab="", xlab="")
axis(1, at=c(1:12), labels=xlb)
axis(2, at=c(0:10)*50000, labels=sapply(c(0:10)*50000, FUN=f2si2, rounding=T, sep=""))
title(ylab="Number of Sub-URI Keys", xlab="Max segments (H: Host segments, P: Path segments)")

dev.off()
