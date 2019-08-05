import "../../runScripts.wdl" as runScripts

workflow main {
    File inputbw1main
    File inputbw2main
    File inputbw3main
    call runScripts.computeCorr as computingCorr {
		input: bigwig1 = inputbw1main, bigwig2 = inputbw2main, bigwig3 = inputbw3main
	}
	output {
        File corrScores = "corrScores.txt"
    }
}