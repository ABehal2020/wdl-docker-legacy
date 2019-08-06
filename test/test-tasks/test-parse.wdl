import "../../runScripts.wdl" as runScripts

workflow mainParse {
    File jsonMain
    call runScripts.parse_json as parsing {
        input: json = jsonMain
    }
    output {
        File urls = parsing.urls
	File downloadMeta = parsing.downloadMeta
	# File urls = 'exp1.txt'
	# File downloadMeta = 'download-meta.txt'
    }
}
