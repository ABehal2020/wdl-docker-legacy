# wdl-docker
Dockerized CHiP-Seq visualization tool for ENCODE data 

Calling the visualization tool docker image, the WDL script tests 2 parts of the tool (both parts successfully pass the test): 
1) Passing JSON metadata of experimental data from ENCODE server and getting s3_urls for bigwig files
2) Passing the s3_urls for bigwig files (output from first part) and getting the contents of the bigwig files

Make sure to have cromwell.jar and wdltool.jar installed. After navigating to the directory with those two files and this cloned github directory, run this command: java -jar cromwell.jar run runScripts.wdl -i runScripts_inputs.json

Also, download these 3 files (reference bigwig files) in the same directory:

https://encode-public.s3.amazonaws.com/2018/03/06/c2206997-d760-4f5a-a403-175e7779e2ed/ENCFF075MCN.bigWig - this should be called "1.bigwig"

https://encode-public.s3.amazonaws.com/2018/03/06/a9864011-80d2-4141-b103-651330ad2e63/ENCFF231NTN.bigWig - this should be called "2.bigwig"

https://encode-public.s3.amazonaws.com/2018/03/06/32417a7e-b149-40b5-a4c0-facbabddc17e/ENCFF415GFH.bigWig - this should be called "3.bigwig"

