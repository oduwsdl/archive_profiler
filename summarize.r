#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=T)
if (length(args) < 1) {
  print("Please pass the path to the directory containing the CSV files as a command line argument.")
  quit()
}

f2si2 <- function (number, rounding=F, sep=" ") {
  lut <- c(1e-24, 1e-21, 1e-18, 1e-15, 1e-12, 1e-09, 1e-06, 
      0.001, 1, 1000, 1e+06, 1e+09, 1e+12, 1e+15, 1e+18, 1e+21, 
      1e+24)
  pre <- c("y", "z", "a", "f", "p", "n", "u", "m", "", "k", 
      "M", "G", "T", "P", "E", "Z", "Y")
  ix <- findInterval(number, lut)
  if (ix>0 && lut[ix]!=1) {
    if (rounding==T) {
      sistring <- paste(round(number/lut[ix]), pre[ix], sep=sep)
    } else {
      sistring <- paste(number/lut[ix], pre[ix], sep=sep)
    }
  } else {
    sistring <- as.character(number)
  }
  return(sistring)
}

summarize <- function (field, ylabel="") {
  fid <- gsub("[^a-zA-Z0-9]+", "-", field)
  fname <- file.path(args[1], gsub("FID", fid, "summary-FID-lineplot.png"))
  print(fname)

  png(fname, height=600, width=800, pointsize=18)

  ypos <- pretty(c(0, max(combined[[field]])), n=10)
  ylb <- lapply(ypos, f2si2, rounding=T, sep="")
  xlb <- profiles[[1]][["profile_id"]]

  par(mar=c(4,4,1,1)+0.1)

  plot(profiles[[1]][[field]], type="n", xaxt="n", yaxt="n", ylab=ylabel, xlab="Max segments (H: Host, P: Path)", ylim=c(0, max(ypos)))
  axis(1, at=c(1:length(xlb)), labels=xlb, las=3)
  axis(2, at=ypos, labels=ylb)
  par(family='mono')
  legend("topleft", inset=0.01, title="CDX Collection", pch=symbols, col=cols, cex=0.6, bty="n", legend=proflegs)

  for(i in 1:length(profiles)) {
    lines(profiles[[i]][[field]], type='b', pch=symbols[i], col=cols[i])
  }

  dev.off()
}

correlate <- function (fldnames=c(), fid="all") {
  fields <- tolower(gsub("\\W", "", gsub(" ", "_", fldnames)))
  fname <- file.path(args[1], gsub("FID", fid, "correlation-FID-lineplot.png"))
  print(fname)

  png(fname, height=1000, width=800, pointsize=16)

  xlb <- gsub("[^0-9]", "", hps[[1]][["collection"]])
  cols <- rainbow(length(fields))
  symbols <- c(0:(length(fields)-1))
  par(mar=c(1.2,1.2,0.3,0.3)+0.1, mfrow=c(6,3))

  plot(rep(1, each=length(xlb)), type="n", xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, 1))
  legend("topleft", inset=0.01, title="Normalized Measures", pch=symbols, col=cols, cex=0.9, bty="n", ncol=2, legend=fldnames)

  for(i in 1:length(hps)) {
    plot(rep(1, each=length(xlb)), type="n", xaxt="n", yaxt="n", ylab="", xlab="", ylim=c(0, 1))
    axis(1, at=c(1:length(xlb)), labels=xlb, tck=-0.03, mgp=c(1, 0.3, 0))
    axis(2, at=c(0:4)/4, labels=c(0:4)/4, tck=-0.03, mgp=c(1, 0.3, 0))
    text(1.5, 0.9, hps[[i]][["profile_id"]][[1]], cex=1.2)

    for(j in 1:length(fields)) {
      lines(hps[[i]][[fields[j]]]/max(hps[[i]][[fields[j]]]), type='b', pch=symbols[j], col=cols[j])
    }
  }

  dev.off()
}

files <- list.files(path=args[1], pattern="*.csv", full.names=T, recursive=F)
profiles <- lapply(files, read.csv, header=T)
profiles <- lapply(profiles, transform, urim_urir_ratio=urim_count/urir_count)
names(profiles) <- gsub("^.*summary-|\\.csv$", "", files)
combined <- do.call("rbind", profiles)
hps <- split(combined, f=combined$profile_id)
cols <- rainbow(length(profiles))
symbols <- c(0:(length(profiles)-1))
hpref <- hps[[1]]
proflegs <- paste(hpref$collection, " URI-R: ", format(hpref$urir_count, big.mark=","), " CDX: ", f2si2(hpref$cdx_size, rounding=T, sep=""), sep="")

summarize("suburi_keys", "Number of Sub-URI Keys")
summarize("profile_size", "Profile size")
summarize("profile_size_compressed", "Profile size (compressed)")
summarize("profiling_time", "Profiling time (seconds)")

correlate(c("URI-R Count", "URI-M Count", "URI-M URI-R Ratio", "Sub-URI Keys", "Profile Size", "Profile Size Compressed", "CDX Processing Time", "Stats Calculation Time", "Profiling Time", "CDX Size", "CDX Lines Total"))
