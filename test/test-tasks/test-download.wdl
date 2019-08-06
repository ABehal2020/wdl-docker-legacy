import "../../runScripts.wdl" as runScripts

workflow downloadbwMain {
    File downloadMain
    call runScripts.download as downloading {
		input: downloadInfo = downloadMain
	}
	output {
	    # File bigwig1 = 'ENCFF075MCN.bigwig'
		# File bigwig2 = 'ENCFF231NTN.bigwig'
		# File bigwig3 = 'ENCFF415GFH.bigwig'
		File bigwig1 = downloading.bigwig1
		File bigwig2 = downloading.bigwig2
		File bigwig3 = downloading.bigwig3
	}
}