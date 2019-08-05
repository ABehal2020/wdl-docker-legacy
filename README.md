# wdl-docker
Part of the dockerized CHiP-Seq visualization tool for ENCODE data for successful testing/validation purposes 

Note: Because this application is dockerized and references a docker built and pushed to Docker Hub, you don't need to download the bigwig files or anything else oustide of cromwell.jar, wdltool.jar, and wdl-scripts with their associated JSON files. If you want to explore the bigwig files and their directories as referenced in the code, you can download the bigwig files as specified in this document.

Calling the visualization tool docker image, the WDL script tests 3 parts of the tool (which all pass the test) to ensure proper data and calculation integry throughout.
1) Passing JSON metadata of experimental data from ENCODE server and getting s3_urls for bigwig files
2) Passing the s3_urls for bigwig files (output from first part) and getting the contents of the bigwig files
3) Passing the contents of the bigwig files (output from the second part) and getting the correlation scores

After cloning this repository, make sure to have cromwell.jar and wdltool.jar installed directly under wdl-docker directory.

Also, download these 3 files (reference bigwig files) in the same directory:

https://encode-public.s3.amazonaws.com/2018/03/06/c2206997-d760-4f5a-a403-175e7779e2ed/ENCFF075MCN.bigWig - this should be called "1.bigwig"

https://encode-public.s3.amazonaws.com/2018/03/06/a9864011-80d2-4141-b103-651330ad2e63/ENCFF231NTN.bigWig - this should be called "2.bigwig"

https://encode-public.s3.amazonaws.com/2018/03/06/32417a7e-b149-40b5-a4c0-facbabddc17e/ENCFF415GFH.bigWig - this should be called "3.bigwig"

Then, run this command to see the workflow testing: java -jar cromwell.jar run runScripts.wdl -i runScripts_inputs.json

For unit testing of correlate, navigate to the test/test-data directory and copy the 3 downloaded bigwig files there and rename them:
"1.bigwig" should be renamed to "ENCFF075MCN.bigwig"
"2.bigwig" should be renamed to "ENCFF231NTN.bigwig"
"3.bigwig" should be renamed to "ENCFF415GFH.bigwig"

# parse unit test
java -jar ../../cromwell.jar run test-parse.wdl -i test-parse_inputs.json

# download unit test
java -jar ../../cromwell.jar run test-download.wdl -i test-download_inputs.json

# correlate unit test
java -jar ../../cromwell.jar run test-correlate.wdl -i test-correlate_inputs.json
