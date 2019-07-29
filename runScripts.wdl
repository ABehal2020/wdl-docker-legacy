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
		# docker: 'cherry101/wdl-docker@sha256:4efef9d1cbf3e877d6426ec3269efdd6602cda12d6ccc4a7c617bb2484748e48'
		# docker: 'wdl-docker:v12'
		docker: 'cherry101/wdl-docker@sha256:9f946f91a8ecb808c16a62089eb38fd92a91267b63cbccd246656667b37f5ea8'
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
		ls
		pwd
		python /usr/src/app/download.py ${downloadInfo}
		ls
		pwd
	}
	output {
		# File bigwig1 = 'ENCFF075MCN'
		# File bigwig2 = 'ENCFF231NTN'
		# File bigwig3 = 'ENCFF415GFH'
		File bigwig1 = glob('/usr/src/app/ENC*')[0]
		File bigwig2 = glob('/usr/src/app/ENC*')[0]
		File bigwig3 = glob('/usr/src/app/ENC*')[0]
	}

	# for docker image v13 where test file is being downloaded using requests api in python - fails when output section is specified
	# note that the file does not show up in the execution directory in the cromwell-executions folder
	# output {
		# File sample = 'instructions'
	# }
	runtime {
		# docker: 'cherry101/wdl-docker@sha256:4efef9d1cbf3e877d6426ec3269efdd6602cda12d6ccc4a7c617bb2484748e48'
		# docker: 'wdl-docker:v12'
		docker: 'cherry101/wdl-docker@sha256:9f946f91a8ecb808c16a62089eb38fd92a91267b63cbccd246656667b37f5ea8'
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
		md5sum ${inputbw1} ${refbw1} > md5bwcompare.txt
		md5sum ${inputbw2} ${refbw2} > md5bwcompare.txt
		md5sum ${inputbw3} ${refbw3} > md5bwcompare.txt
	}
}

workflow main {
	File jsonMain
	File refMain
	File refbw1main
	File refbw2main
	File refbw3main
	call parse_json {
		input: json = jsonMain
	}
	call md5parse_json {
		input: inputFile = parse_json.urls, refFile = refMain
	}
	call download {
		input: downloadInfo = parse_json.downloadMeta
	}
	call md5download as md5download {
		input: inputbw1 = download.bigwig1, inputbw2 = download.bigwig2, inputbw3 = download.bigwig3, refbw1 = refbw1main, refbw2 = refbw2main, refbw3 = refbw3main
	}
}

