# wdl-docker
CHiP-Seq visualization tool for ENCODE data 

The WDL script tests 2 parts of the tool (both parts successfully pass the test): 
1) Passing JSON metadata of experimental data from ENCODE server and getting s3_urls for bigwig files
2) Passing the s3_urls for bigwig files (output from first part) and getting the contents of the bigwig files

Make sure to have cromwell.jar and wdltool.jar installed. After navigating to the directory with those two files and this cloned github directory, run this command: java -jar cromwell.jar run runScripts.wdl -i runScripts_inputs.json


