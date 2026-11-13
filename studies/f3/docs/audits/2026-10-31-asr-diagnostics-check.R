# Run from models/pilot-asr with the locked R environment; summaries only, no mapping rerun.
.libPaths(c(Sys.glob("renv/library/*/R-*/*"), .libPaths()))
suppressPackageStartupMessages(library(coda))
suppressPackageStartupMessages(library(jsonlite))
fns <- c('out/diagnostics_maps.csv','out/diagnostics_maps_ext_b10000_s100.csv')
all_results <- list()
for (fn in fns) {
  tag <- sub('out/diagnostics_maps','',sub('\\.csv$','',fn))
  receipt <- fromJSON(paste0('out/diagnostics_receipt',tag,'.json'))
  hashes <- tools::sha256sum(names(receipt$outputs))
  stopifnot(all(unname(hashes) == unlist(receipt$outputs)))
  d <- read.csv(fn)
  stopifnot(!anyNA(d),all(d$persist <= d$start),all(d$q3_per_myr > 0),
            all(d$departures >= 0),all(d$entries >= d$reentries),
            all((d$persist == 1) == (d$start == 1 & d$departures == 0)))
  groups <- split(d,list(d$tree,d$chain),drop=TRUE)
  stopifnot(all(vapply(groups,function(z) nrow(z)==1000 && identical(z$map,1:1000) && length(unique(z$seed))==1,FALSE)))
  saved <- read.csv(paste0('out/diagnostics_summary',tag,'.csv'))
  for (tn in unique(d$tree)) {
    s <- subset(d,tree==tn)
    cs <- split(s,s$chain)
    qs <- mcmc.list(lapply(cs,function(c) mcmc(c$q3_per_myr)))
    p <- sum(s$persist)/sum(s$start)
    z <- lapply(cs,function(c) (c$persist-p*c$start)/mean(s$start))
    vz <- vapply(z,var,0.0)
    es <- vapply(z,function(v) if(var(v)==0) NA_real_ else as.numeric(effectiveSize(v)),0.0)
    spectral <- vapply(z,function(v) if(var(v)==0) 0.0 else spectrum0.ar(v)$spec,0.0)
    mcse_old <- sd(unlist(z))/sqrt(sum(es,na.rm=TRUE))
    mcse_sumvar <- sqrt(sum(vz/es*1000^2,na.rm=TRUE))/4000
    mcse_spectral <- sqrt(sum(spectral*1000))/4000
    pc <- vapply(cs,function(c) sum(c$persist)/sum(c$start),0.0)
    rh <- as.numeric(gelman.diag(qs,autoburnin=FALSE)$psrf[1,1])
    eq <- as.numeric(effectiveSize(qs))
    got <- data.frame(run=if(tag=='')'Hooper' else 'long',tree=tn,n=nrow(s),starts=sum(s$start),departures=sum(s$start-s$persist),p=p,rhat=rh,ess=eq,mcse_saved=mcse_old,mcse_independent_chains=mcse_sumvar,mcse_spectral=mcse_spectral,mcse_chain_means=sd(pc)/sqrt(4),pmin=min(pc),pmax=max(pc))
    row <- subset(saved,tree==tn)
    stopifnot(abs(row$p_persist_given_start-p)<1e-14,abs(row$rhat_q3-rh)<1e-12,abs(row$ess_q3-eq)<1e-8,abs(row$mcse_given_start-mcse_old)<1e-14)
    all_results[[length(all_results)+1]] <- got
    cat('\n',fn,tn,'\n')
    print(data.frame(chain=names(cs),starts=vapply(cs,function(c)sum(c$start),0.0),departures=vapply(cs,function(c)sum(c$start-c$persist),0.0),variance_z=vz,ess_z=es,spectral_z=spectral,p=pc),digits=8)
  }
}
results <- do.call(rbind,all_results)
print(results,digits=10,row.names=FALSE)
args <- commandArgs(trailingOnly = TRUE)
if (length(args)) write.csv(results, args[1], row.names = FALSE)
r <- read.csv('out/retention_chains.csv')
mx <- 0
for (i in seq_len(nrow(r))) {
  d <- subset(read.csv(r$source[i]),tree==r$tree[i])
  v <- exp(-d$q3_per_myr*(r$origin_ma[i]-r$tau_ma[i]))
  actual <- c(median(v),quantile(v,c(.025,.975)),median(d$q3_per_myr))
  recorded <- unlist(r[i,c('R_median','R_lo','R_hi','q3_median_per_myr')])
  mx <- max(mx,abs(actual-recorded))
}
cat('\nRETENTION_MAX_ABS_ERROR',format(mx,digits=16),'\n')
cat('CHECKS_OK\n')
