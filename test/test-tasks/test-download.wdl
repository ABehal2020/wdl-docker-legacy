import "../../runScripts.wdl" as runScripts

workflow main {
    File downloadMain
    call runScripts.download as downloading {
		input: downloadInfo = downloadMain
	}
	output {
	    File bigwig1 = 'ENCFF075MCN.bigwig'
		File bigwig2 = 'ENCFF231NTN.bigwig'
		File bigwig3 = 'ENCFF415GFH.bigwig'
	}
}