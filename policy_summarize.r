#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=T)
if (length(args) < 1) {
  print("Please pass the path to the directory containing the CSV files as a command line argument.")
  quit()
}

f2si2 <- function (number, rounding=F, sep=" ", fmt="%3.0f") {
  lut <- c(1e-24, 1e-21, 1e-18, 1e-15, 1e-12, 1e-09, 1e-06, 
      0.001, 1, 1000, 1e+06, 1e+09, 1e+12, 1e+15, 1e+18, 1e+21, 
      1e+24)
  pre <- c("y", "z", "a", "f", "p", "n", "u", "m", "", "K", 
      "M", "G", "T", "P", "E", "Z", "Y")
  ix <- findInterval(number, lut)
  if (ix>0 && lut[ix]!=1) {
    if (rounding==T) {
      sistring <- paste(sprintf(fmt, round(number/lut[ix], 1)), pre[ix], sep=sep)
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
  fname <- file.path(args[1], gsub("FID", fid, "policy-summary-FID-lineplot.png"))
  print(fname)

  png(fname, height=400, width=600, pointsize=18)

  ypos <- pretty(c(0, max(combined[[field]])), n=10)
  ylb <- lapply(ypos, f2si2, rounding=T, sep="")
  xlb <- profiles[[1]][["policy"]]

#  par(mar=c(4,4,1,1)+0.1)
  par(mar=c(4,3,1,1)+0.1, mgp=c(1.5,0.5,0), lwd=2)

  plot(profiles[[1]][[field]], type="n", xaxt="n", yaxt="n", ylab=ylabel, xlab="", ylim=c(0, max(ypos)))
  for(i in 1:length(profiles)) {
    lines(profiles[[i]][[field]], type='b', pch=symbols[i], col=cols[i])
  }
  #axis(1, at=c(1:length(xlb)), labels=xlb, las=3)
  axis(2, at=ypos, labels=ylb)
  title(xlab="Profile Policies", mgp=c(2.8, 0.5, 0))
  par(family='mono', font.axis=2, font=2)
  axis(1, at=c(1:length(xlb)), labels=xlb, las=3)
  par(cex=0.8)
  legend("topleft", inset=0.01, y.intersp=0.8, title="UKWA CDX Collection", pch=c(NA, symbols), col=c(NA, cols), legend=c("Year CDX_Size URI-R_Count URI-M/R", proflegs))

  dev.off()
}

correlate <- function (fldnames=c(), fid="all") {
  fields <- tolower(gsub("\\W", "", gsub(" ", "_", fldnames)))
  fname <- file.path(args[1], gsub("FID", fid, "policy-correlation-FID-lineplot.png"))
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
    axis(1, at=c(1:length(xlb)), labels=xlb, tck=-0.02, mgp=c(1, 0.3, 0))
    axis(2, at=c(0:4)/4, labels=c(0:4)/4, tck=-0.02, mgp=c(1, 0.3, 0))
    text(1.5, 0.9, hps[[i]][["policy"]][[1]], cex=1.2)

    for(j in 1:length(fields)) {
      lines(hps[[i]][[fields[j]]]/max(hps[[i]][[fields[j]]]), type='b', pch=symbols[j], col=cols[j])
    }
  }

  dev.off()
}

growth <- function (xfld, yfld, xlabel="", ylabel="") {
  xfid <- gsub("[^a-zA-Z0-9]+", "-", xfld)
  yfid <- gsub("[^a-zA-Z0-9]+", "-", yfld)
  fname <- file.path(args[1], gsub("YFID", yfid, gsub("XFID", xfid, "policy-growth-XFID-vs-YFID-fit-lineplot.png")))
  print(fname)

  png(fname, height=400, width=600, pointsize=18)

  ypos <- pretty(c(0, max(combined[[yfld]])), n=10)
  ylb <- lapply(ypos, f2si2, rounding=T, sep="")
  xpos <- pretty(c(0, max(combined[[xfld]])), n=10)
  xlb <- lapply(xpos, f2si2, rounding=T, sep="")
  gcol <- rainbow(length(hps))
  gpch <- c(0:(length(hps)-1))

#  par(mar=c(4,4,1,1)+0.1)
  par(mar=c(3,3,1,1)+0.1, mgp=c(1.5,0.5,0), lwd=2)

  plot(hps[[1]][[xfld]], hps[[1]][[yfld]], type="n", xaxt="n", yaxt="n", ylab=ylabel, xlab=xlabel, ylim=c(0, max(ypos)))
  axis(1, at=xpos, labels=xlb)
  axis(2, at=ypos, labels=ylb)

  profnames <- names(hps)

  for(i in 1:length(hps)) {
    x <- hps[[i]][[xfld]]
    y <- hps[[i]][[yfld]]
    fit <- lm(y~x)
    lines(hps[[i]][[xfld]], hps[[i]][[yfld]], type='p', pch=gpch[i], col=gcol[i])
    lines(xpos, predict(fit, data.frame(x=xpos)), lty=1, col=gcol[i])
    #print(summary(fit))
    #print(coef(fit)["(Intercept)"])
    #print(profnames[[i]])
    print(paste(profnames[[i]], "x:", round(coef(fit)["x"], 8)))
  }

  par(family='mono', cex=0.8, font=2)
  legend("topleft", inset=0.01, title="Profile Policies", pch=gpch, col=gcol, ncol=4, legend=profiles[[1]][["policy"]])

  dev.off()
}

relate <- function (xfld, yfld, xlabel="", ylabel="") {
  xfid <- gsub("[^a-zA-Z0-9]+", "-", xfld)
  yfid <- gsub("[^a-zA-Z0-9]+", "-", yfld)
  fname <- file.path(args[1], gsub("YFID", yfid, gsub("XFID", xfid, "policy-relate-XFID-vs-YFID-lineplot.png")))
  print(fname)

  png(fname, height=400, width=600, pointsize=18)

  ypos <- pretty(c(0, max(combined[[yfld]])), n=5)
  ylb <- lapply(ypos, f2si2, rounding=T, sep="")
  xpos <- pretty(c(0, max(combined[[xfld]])), n=5)
  xlb <- lapply(xpos, f2si2, rounding=T, sep="")

#  par(mar=c(4,4,1,1)+0.1)
  par(mar=c(3,3,1,1)+0.1, mgp=c(1.5,0.5,0), lwd=2)

  x <- hps[[1]][[xfld]]
  y <- hps[[1]][[yfld]]
  fit <- lm(y~x)

  plot(x, y, type="p", xaxt="n", yaxt="n", pch=0, col="red", ylab=ylabel, xlab=xlabel, ylim=c(0, max(ypos)))
  lines(xpos, predict(fit, data.frame(x=xpos)), lty=1, col="red")
  axis(1, at=xpos, labels=xlb)
  axis(2, at=ypos, labels=ylb)

  dev.off()
}

files <- list.files(path=args[1], pattern="summary-.*.csv$", full.names=T, recursive=F)
profiles <- lapply(files, read.csv, header=T)
#profiles <- lapply(profiles, function(df){df[order(df$keys_count),]})
profiles <- lapply(profiles, transform, urim_urir_ratio=urim_count/urir_count)
names(profiles) <- gsub("^.*summary-|\\.csv$", "", files)
combined <- do.call("rbind", profiles)
combined$policy <- factor(combined$policy, levels=unique(combined$policy))
hps <- split(combined, f=combined$policy)
cols <- rainbow(length(profiles))
symbols <- c(0:(length(profiles)-1))
hpref <- hps[[1]]
proflegs <- paste(substr(hpref$collection, 7, 11), " ", f2si2(hpref$cdx_size, rounding=T, sep="", fmt="%5.1f"), "    ", f2si2(hpref$urir_count, rounding=T, sep="", fmt="%5.1f"), " ", round(hpref$urim_urir_ratio, 3), sep=" ")

summarize("keys_count", "Number of Keys")
summarize("profile_size", "Profile Size")
summarize("profile_size_compressed", "Profile Size (Compressed)")
# summarize("profiling_time", "Profiling Time (Seconds)")

# growth("cdx_size", "keys_count", "CDX Size", "Number of Keys")
growth("urir_count", "keys_count", "URI-R Count", "Number of Keys")
growth("urim_count", "profiling_time", "URI-M Count", "Profiling Time (Seconds)")

# relate("cdx_size", "urir_count", "CDX Size", "URI-R Count")
relate("cdx_size", "urim_count", "CDX Size", "URI-M Count")
relate("urim_count", "urir_count", "URI-M Count", "URI-R Count")
# 
# correlate(c("URI-R Count",
#             "URI-M Count",
#             "URI-M URI-R Ratio",
#             "Sub-URI Keys",
#             "Profile Size",
#             "Profile Size Compressed",
#             "Key Generation Time",
#             "Profile Generation Time",
#             "Profiling Time",
#             "CDX Size",
#             "Extract Size"),
#           "all")
# correlate(c("CDX Size",
#             "Profile Size",
#             "Profile Size Compressed"),
#           "sizes")

#print(hps)
