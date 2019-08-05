import "../../runScripts.wdl" as runScripts

workflow main {
    File jsonMain
    call runScripts.parse_json as parsing {
        input: json = jsonMain
    }
    output {
        File urls = parse_json.urls
	File downloadMeta = parse_json.downloadMeta
	# File urls = 'exp1.txt'
	# File downloadMeta = 'download-meta.txt'
    }
}
