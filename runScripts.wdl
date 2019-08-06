# can have docker.json file to specify docker runtime for each task
# workflow options (-o)

# take ENCSR json metadata and return bigwig urls
task parse_json {
	File json
	command {
		python /usr/src/app/parse.py ${json}
	}
	output {
		File urls = 'exp1.txt'
		File downloadMeta = 'download-meta.txt'
	}
	runtime {
	    # docker: 'wdl-docker:v25'
		docker: 'cherry101/wdl-docker@sha256:ffe1bf2428d11f28168f05b4384d03e7b9d49c3ee8ee2e6a0e66a905c4e44a25'
	}
}

task md5parse_json {
	File inputFile
	File refFile
	command {
		md5sum ${inputFile} ${refFile} > md5urlcompare.txt
	}
}

task download {
	File downloadInfo
	command {
		python /usr/src/app/download.py ${downloadInfo}
	}
	output {
		# File bigwig1 = 'ENCFF075MCN.bigwig'
		# File bigwig2 = 'ENCFF231NTN.bigwig'
		# File bigwig3 = 'ENCFF415GFH.bigwig'
		File bigwig1 = glob('*.bigwig')[0]
		File bigwig2 = glob('*.bigwig')[1]
		File bigwig3 = glob('*.bigwig')[2]
	}

	# for docker image v13 where test file is being downloaded using requests api in python - fails when output section is specified
	# note that the file does not show up in the execution directory in the cromwell-executions folder
	# output {
		# File sample = 'instructions'
	# }
	runtime {
	    # docker: 'wdl-docker:v25'
		docker: 'cherry101/wdl-docker@sha256:ffe1bf2428d11f28168f05b4384d03e7b9d49c3ee8ee2e6a0e66a905c4e44a25'
	}
}

task md5download {
	File inputbw1
	File inputbw2
	File inputbw3
	File refbw1
	File refbw2
	File refbw3
	command {
		md5sum ${inputbw1} ${refbw1} > md5bw1compare.txt
		md5sum ${inputbw2} ${refbw2} > md5bw2compare.txt
		md5sum ${inputbw3} ${refbw3} > md5bw3compare.txt
	}
}

task computeCorr {
    File bigwig1
    File bigwig2
    File bigwig3
    command {
        python /usr/src/app/correlate.py ${bigwig1} ${bigwig2} ${bigwig3}
    }
    output {
        File corrScores = "corrScores.txt"
    }
    runtime {
        # docker: 'wdl-docker:v25'
        docker: 'cherry101/wdl-docker@sha256:ffe1bf2428d11f28168f05b4384d03e7b9d49c3ee8ee2e6a0e66a905c4e44a25'
    }
}

task md5computeCorr {
    File corrScores
    File refScores
    command {
		md5sum ${corrScores} ${refScores} > md5scores.txt
	}
}

workflow main {
	File jsonMain
	File jsonRefMain
	File refbw1main
	File refbw2main
	File refbw3main
	File refScoresMain
	call parse_json {
		input: json = jsonMain
	}
	# call md5parse_json {
		# input: inputFile = parse_json.urls, refFile = jsonRefMain
	# }
	call download {
		input: downloadInfo = parse_json.downloadMeta
	}
	# call md5download {
		# input: inputbw1 = download.bigwig1, inputbw2 = download.bigwig2, inputbw3 = download.bigwig3, refbw1 = refbw1main, refbw2 = refbw2main, refbw3 = refbw3main
	# }
	call computeCorr {
	    input: bigwig1 = download.bigwig1, bigwig2 = download.bigwig2, bigwig3 = download.bigwig3
	}
	# call md5computeCorr {
	    # input: corrScores = computeCorr.corrScores, refScores = refScoresMain
	# }
	output {
		File urls = parse_json.urls
		File downloadMeta = parse_json.downloadMeta
		File bigwig1 = download.bigwig1
		File bigwig2 = download.bigwig2
		File bigwig3 = download.bigwig3
		File corrScores = computeCorr.corrScores
	}
}

