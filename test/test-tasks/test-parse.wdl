import "../../runScripts.wdl" as runScripts

workflow main {
    File jsonMain
    call runScripts.parse_json as parsing {
        input: json = jsonMain
    }
    output {
        File urls = 'exp1.txt'
		File downloadMeta = 'download-meta.txt'
    }
}